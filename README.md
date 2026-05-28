# 🛡️ Micro-IDS & SOC Dashboard

A lightweight, local Intrusion Detection System (IDS) and miniature SOC (Security Operations Center) dashboard developed in Python. This project simulates a honeypot (fake Web server) capable of analyzing network traffic in real time, detecting signature-based attacks, and identifying behavioral anomalies using time-window heuristics.

## 🚀 Cyber Features & Detection Logic

The project is structured around two main detection engines:

1. **Behavioral Analysis (Brute-Force Detection):**
   - Dynamic tracking of incoming requests per IP address.
   - Cleaning algorithm based on a sliding time-window (e.g., maximum 5 requests per 10-second interval).
   - Automatic state triggering when an IP exceeds the frequency threshold.

2. **Signature Analysis (HTTP Payload Inspection):**
   - **SQL Injection (SQLi):** Scans and detects malicious patterns and keywords (`SELECT...FROM`, `OR 1=1`).
   - **Path Traversal:** Blocks attempts to read local system files (`../`, `/etc/passwd`).
   - **Reconnaissance:** Identifies automated vulnerability scanners looking for sensitive directories (`.env`, `wp-admin`).

---

## 📊 Interface Overview (SOC Dashboard)

The interface leverages the `Rich` library to render a dynamic, clean, and interactive console layout tailored for security operators.

* **Live Traffic Feed and Real-Time Alerts:**
<img width="1115" height="628" alt="image" src="https://github.com/user-attachments/assets/5fb63019-3b1e-4e09-a971-960432c2c5fc" />

---

## 🛠️ Windows Installation, Usage & Attack Simulation (PowerShell)

### Prerequisites
- Python 3.x
- Windows PowerShell

### Terminal 1: Setup & Launch
Run these commands in your first PowerShell window to clone the project, install the required packages, and start the IDS server:
```powershell
git clone [https://github.com/VicThor13/Micro_IDS.git](https://github.com/VicThor13/Micro_IDS.git)
cd Micro_IDS
pip install -r requirements.txt
python micro_ids.py
```

### Terminal 2: Attack Simulation
Once the server is up and running in Terminal 1, **open a second PowerShell window** and copy-paste these commands to trigger the detection engines:
```powershell
curl.exe -s "[http://127.0.0.1:8080/accueil](http://127.0.0.1:8080/accueil)"
curl.exe -s "[http://127.0.0.1:8080/download?file=../../../../etc/passwd](http://127.0.0.1:8080/download?file=../../../../etc/passwd)"
for ($i=1; $i -le 7; $i++) { curl.exe -s "[http://127.0.0.1:8080/test](http://127.0.0.1:8080/test)" }
```

---

## 🐧 Linux Installation, Usage & Attack Simulation (Bash)

### Prerequisites
- Python 3.x & Git
- Linux Terminal (Bash)

### Terminal 1: Setup & Launch
Run these commands in your first terminal window to clone the project, install the required packages, and start the IDS server:
```bash
git clone [https://github.com/VicThor13/Micro_IDS.git](https://github.com/VicThor13/Micro_IDS.git)
cd Micro_IDS
pip install --break-system-packages -r requirements.txt
python3 micro_ids.py
```

### Terminal 2: Attack Simulation
Once the server is up and running in Terminal 1, **open a second terminal window** and copy-paste these commands to trigger the detection engines:
```bash
curl -s "[http://127.0.0.1:8080/accueil](http://127.0.0.1:8080/accueil)"
curl -s "[http://127.0.0.1:8080/download?file=../../../../etc/passwd](http://127.0.0.1:8080/download?file=../../../../etc/passwd)"
for i in {1..7}; do curl -s "[http://127.0.0.1:8080/test](http://127.0.0.1:8080/test)"; done
```

---

## 🧠 Cyber Skills Validated by this Project

* **Network Programming:** Handling TCP sockets in Python.
* **Detection Engineering:** Creating payload inspection rules and time-based correlation logic.
* **False Positive Reduction:** Setting up threshold baselines to differentiate between human error and malicious brute-forcing.
* **SOC Visualization:** Designing a clear monitoring dashboard prioritized by event severity.
