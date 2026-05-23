# 🛡️ Micro-IDS & SOC Dashboard

Un système local de détection d'intrusions (IDS) et un tableau de bord SOC (Security Operations Center) miniature développé en Python. Ce projet simule un honeypot (faux serveur Web) capable d'analyser le trafic réseau en temps réel, de détecter des attaques par signature et d'identifier des anomalies comportementales à l'aide de fenêtres temporelles.

## 🚀 Fonctionnalités & Logique Cyber

Le projet est articulé autour de deux moteurs de détection principaux :

1. **Analyse Comportementale (Détection de Brute-Force) :** - Suivi dynamique des requêtes par adresse IP.
   - Algorithme de nettoyage basé sur une fenêtre glissante temporelle (ex: max 5 requêtes par intervalle de 10 secondes).
   - Bascule automatique de l'état de l'IP en cas d'anomalie de fréquence.

2. **Analyse de Signatures (Inspection de Payload HTTP) :**
   - **Injection SQL (SQLi) :** Analyse et détection de patterns et mots-clés malveillants (`SELECT...FROM`, `OR 1=1`).
   - **Path Traversal :** Blocage des tentatives de lecture de fichiers système (`../`, `/etc/passwd`).
   - **Reconnaissance :** Identification des scans de vulnérabilités automatisés cherchant des dossiers sensibles (`.env`, `wp-admin`).

---

## 📊 Aperçu de l'Interface (Dashboard SOC)

L'interface utilise la bibliothèque `Rich` pour restituer une console dynamique, claire et exploitable par un opérateur de sécurité.

* **Trafic standard et alertes en direct :**
  *(Insérer ici ton screenshot ou GIF du dashboard en action)*

---

## 🛠️ Installation et Utilisation

### Prérequis
- Python 3.x
- Un terminal (PowerShell, CMD ou Linux Terminal)

### 1. Cloner le projet et installer les dépendances
```bash
git clone [https://github.com/VicThor13/Micro_IDS.git](https://github.com/VicThor13/Micro_IDS.git)
cd Micro_IDS
pip install -r requirements.txt
