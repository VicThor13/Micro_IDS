import socket
from datetime import datetime, timedelta
import os

# Importations de la bibliothèque Rich pour le design de la console
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.layout import Layout

# Configuration
HOST = '127.0.0.1'
PORT = 8080
MAX_ATTEMPTS = 5
TIME_WINDOW_SECONDS = 10

# Mémoire du script
ip_history = {}
recent_events = [] # Liste pour stocker les derniers logs à afficher
console = Console()

def check_brute_force(ip):
    now = datetime.now()
    if ip not in ip_history:
        ip_history[ip] = [now]
        return False
    ip_history[ip].append(now)
    threshold_time = now - timedelta(seconds=TIME_WINDOW_SECONDS)
    ip_history[ip] = [t for t in ip_history[ip] if t > threshold_time]
    
    if len(ip_history[ip]) > MAX_ATTEMPTS:
        return True
    return False

def inspect_payload(payload):
    payload_upper = payload.upper()
    if "SELECT" in payload_upper and "FROM" in payload_upper:
        return "CRITICAL", "Injection SQL (SELECT...FROM)"
    if "OR 1=1" in payload_upper or "' OR '" in payload_upper:
        return "CRITICAL", "Injection SQL (OR 1=1)"
    if "../" in payload or "..\\" in payload or "/etc/passwd" in payload:
        return "CRITICAL", "Path Traversal (Accès fichiers)"
    if "WP-ADMIN" in payload_upper or ".ENV" in payload_upper:
        return "WARNING", "Reconnaissance (Dossier sensible)"
    return "INFO", "Trafic Normal"

def generate_dashboard():
    """
    Génère l'interface graphique du Dashboard à l'aide de Rich
    """
    # 1. Création du tableau des événements récents
    table = Table(title="📊 Flux de Trafic en Direct", expand=True)
    table.add_column("Horodatage", justify="center", style="cyan", no_wrap=True)
    table.add_column("Source", justify="center", style="magenta")
    table.add_column("Sévérité", justify="center")
    table.add_column("Description / Requête", style="white")

    last_alert = "Aucune alerte critique pour le moment."
    alert_style = "green"

    # On peuple le tableau avec les 10 derniers événements
    for event in recent_events[-10:]:
        timestamp, src, status, msg = event
        
        if status == "CRITICAL":
            status_render = "[bold red]CRITICAL[/bold red]"
            last_alert = f"🚨 ALERTE MAXIMALE : {msg} depuis {src}"
            alert_style = "bold red"
        elif status == "WARNING":
            status_render = "[bold orange3]WARNING[/bold orange3]"
            last_alert = f"⚠️ COMPORTEMENT SUSPECT : {msg}"
            if alert_style != "bold red": # Ne pas écraser une alerte critique
                alert_style = "bold orange3"
        else:
            status_render = "[green]INFO[/green]"

        table.add_row(timestamp, src, status_render, msg)

    # 2. Layout global : Le tableau en haut, le bandeau d'alerte en bas
    layout = Layout()
    layout.split_column(
        Layout(Panel(table, border_style="blue")),
        Layout(Panel(last_alert, title="📢 Centre d'Alerte SOC", border_style=alert_style), size=3)
    )
    return layout

def start_ids():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        
        # Efface le terminal pour un affichage propre
        os.system('cls' if os.name == 'nt' else 'clear')
        console.print(Panel.fit("[bold r]🛡️ MICRO-IDS & SOC DASHBOARD EN ÉCOUTE[/bold r]", border_style="red"))
        
        # Utilisation de Live pour mettre à jour la console en temps réel sans clignotement
        with Live(generate_dashboard(), refresh_per_second=2) as live:
            while True:
                conn, addr = s.accept()
                client_ip = addr[0]
                
                with conn:
                    data = conn.recv(1024)
                    if not data:
                        continue
                        
                    payload = data.decode('utf-8', errors='ignore')
                    first_line = payload.split('\n')[0].strip()
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    
                    # Analyses
                    is_brute_forcing = check_brute_force(client_ip)
                    status, message = inspect_payload(payload)
                    
                    # Logique d'enregistrement de l'événement
                    if is_brute_forcing:
                        event_data = (timestamp, client_ip, "WARNING", f"Brute-force détecté ({len(ip_history[client_ip])} req/{TIME_WINDOW_SECONDS}s)")
                    elif status == "CRITICAL":
                        event_data = (timestamp, f"{client_ip}:{addr[1]}", "CRITICAL", f"{message} -> {first_line}")
                    elif status == "WARNING":
                        event_data = (timestamp, f"{client_ip}:{addr[1]}", "WARNING", f"{message} -> {first_line}")
                    else:
                        event_data = (timestamp, f"{client_ip}:{addr[1]}", "INFO", f"Requête standard : {first_line}")
                    
                    # Ajout à notre liste locale
                    recent_events.append(event_data)
                    
                    # Met à jour le visuel de la console
                    live.update(generate_dashboard())
                    
                    response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nEvenement traite."
                    conn.sendall(response.encode('utf-8'))

if __name__ == "__main__":
    try:
        start_ids()
    except KeyboardInterrupt:
        console.print("\n[bold yellow][*] Fermeture du SOC Dashboard.[/bold yellow]")