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

## 🛠️ Installation & Usage

### Prerequisites
- Python 3.x
- A terminal (PowerShell, CMD, or Linux Terminal)

### 1. Clone the project and install dependencies
```bash
git clone [https://github.com/VicThor13/Micro_IDS.git](https://github.com/VicThor13/Micro_IDS.git)
cd Micro_IDS
pip install -r requirements.txt

###2 Lauch the Micro-IDS
python micro_ids.py

###3 Simulate Attacks
Open a second terminal and use the following commands to test the detection engines:

# Test 1: Standard legitimate traffic
curl.exe -s [http://127.0.0.1:8080/accueil](http://127.0.0.1:8080/accueil)

# Test 2: Path Traversal Attack (Red Alert)
curl.exe -s "[http://127.0.0.1:8080/download?file=../../../../etc/passwd](http://127.0.0.1:8080/download?file=../../../../etc/passwd)"

# Test 3: Brute-Force Attack (Orange Warning)
for ($i=1; $i -le 7; $i++) { curl.exe -s [http://127.0.0.1:8080/test](http://127.0.0.1:8080/test) }

```

🧠 Cyber Skills Validated by this Project

- Network Programming: Handling TCP sockets in Python.
- Detection Engineering: Creating payload inspection rules and time-based correlation logic.
- False Positive Reduction: Setting up threshold baselines to differentiate between human error and malicious brute-forcing.
- SOC Visualization: Designing a clear monitoring dashboard prioritized by event severity.

