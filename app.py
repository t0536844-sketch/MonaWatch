from flask import Flask, render_template, jsonify, request
import os, subprocess, time, threading, json
from wakeonlan import send_magic_packet

app = Flask(__name__)

# Persistence Files
KNOWN_DEVICES_FILE = "known_devices.json"
HEALTH_HISTORY_FILE = "health_history.json"
BRAIN_NOTES_FILE = "brain_notes.json"

def load_json(file, default):
    if not os.path.exists(file): return default
    with open(file, 'r') as f: return json.load(f)

def save_json(file, data):
    with open(file, 'w') as f: json.dump(data, f)

# Memory for real-time sentry logs
sentry_logs = []

def monitor_sentry():
    global sentry_logs
    while True:
        if os.path.exists("sentry_logs.txt"):
            with open("sentry_logs.txt", "r") as f:
                sentry_logs = f.readlines()[-15:]
        time.sleep(3)

def monitor_health():
    while True:
        try:
            # Ping a common target to track network health (e.g., Google or Gateway)
            output = subprocess.check_output(["ping", "-c", "1", "8.8.8.8"]).decode()
            latency = float(output.split("time=")[1].split(" ms")[0])
            history = load_json(HEALTH_HISTORY_FILE, [])
            history.append({"time": time.strftime("%H:%M:%S"), "latency": latency})
            save_json(HEALTH_HISTORY_FILE, history[-20:]) # Keep last 20 records
        except: pass
        time.sleep(60) # Every 1 minute

threading.Thread(target=monitor_sentry, daemon=True).start()
threading.Thread(target=monitor_health, daemon=True).start()

@app.route('/')
def index(): return render_template('index.html')

@app.route('/api/scan', methods=['POST'])
def api_scan():
    target = request.json.get('target', '127.0.0.1')
    try:
        cmd = ["nmap", "-sn", target] # Ping scan for faster detection
        output = subprocess.check_output(cmd).decode('utf-8')
        known = load_json(KNOWN_DEVICES_FILE, [])
        found_ips = [line.split("for ")[1].split(" ")[0] for line in output.split("\n") if "Nmap scan report for" in line]
        intruders = [ip for ip in found_ips if ip not in known]
        return jsonify({"status": "success", "data": output, "intruders": intruders})
    except Exception as e: return jsonify({"status": "error", "message": str(e)})

@app.route('/api/known_devices', methods=['GET', 'POST'])
def api_known():
    if request.method == 'POST':
        save_json(KNOWN_DEVICES_FILE, request.json.get('devices', []))
        return jsonify({"status": "success"})
    return jsonify(load_json(KNOWN_DEVICES_FILE, []))

@app.route('/api/health_data')
def api_health_data():
    return jsonify(load_json(HEALTH_HISTORY_FILE, []))

@app.route('/api/wake', methods=['POST'])
def api_wake():
    mac = request.json.get('mac', '')
    if mac:
        send_magic_packet(mac)
        return jsonify({"status": "success", "message": f"Mona sudah kirim 'ciuman maut' buat bangunin {mac}! 💋⚡"})
    return jsonify({"status": "error", "message": "MAC Address kosong, Pace!"})

@app.route('/api/brain', methods=['GET', 'POST'])
def api_brain():
    if request.method == 'POST':
        notes = load_json(BRAIN_NOTES_FILE, [])
        notes.append(request.json.get('note'))
        save_json(BRAIN_NOTES_FILE, notes)
        return jsonify({"status": "success"})
    return jsonify(load_json(BRAIN_NOTES_FILE, []))

@app.route('/api/logs')
def api_logs(): return jsonify({"logs": sentry_logs})

# CLI Feature endpoints (RTSP, SMB, Ping)
@app.route('/api/validate_stream', methods=['POST'])
def api_validate_stream():
    url = request.json.get('url', '')
    try:
        import socket
        host = url.split("//")[-1].split(":")[0]
        port = int(url.split(":")[-1].split("/")[0]) if ":" in url else 554
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.settimeout(3)
        if s.connect_ex((host, port)) == 0: return jsonify({"status": "success", "message": "Stream AKTIF! 😉"})
        return jsonify({"status": "error", "message": "Stream mati atau malu-malu... 🔒"})
    except Exception as e: return jsonify({"status": "error", "message": str(e)})

@app.route('/api/smb', methods=['POST'])
def api_smb():
    ip = request.json.get('ip', '')
    try:
        output = subprocess.check_output(["smbclient", "-L", ip, "-N"], stderr=subprocess.STDOUT).decode('utf-8')
        return jsonify({"status": "success", "data": output})
    except Exception as e: return jsonify({"status": "error", "message": str(e)})

@app.route('/api/export_logs')
def api_export_logs():
    import csv
    from io import StringIO
    from flask import make_response
    
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Timestamp', 'Activity', 'Details'])
    
    # Ambil data dari audit_report.txt jika ada
    if os.path.exists("audit_report.txt"):
        with open("audit_report.txt", "r") as f:
            for line in f:
                if line.strip() and not line.startswith("="):
                    # Simple parsing logic for our log format
                    parts = line.split("]", 1)
                    timestamp = parts[0][1:] if len(parts) > 1 else "N/A"
                    activity = parts[1].strip() if len(parts) > 1 else line.strip()
                    cw.writerow([timestamp, activity, "Mona's Record"])
                    
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename=MonaReport_{time.strftime('%Y%m%d_%H%M%S')}.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@app.route('/api/clear_logs', methods=['POST'])
def api_clear_logs():
    try:
        if os.path.exists("audit_report.txt"): os.remove("audit_report.txt")
        if os.path.exists("sentry_logs.txt"): os.remove("sentry_logs.txt")
        return jsonify({"status": "success", "message": "Log sudah Mona bersihkan, Pace sayang! ✨"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
