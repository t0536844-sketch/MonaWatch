import os
import sys
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def clear_screen():
    os.system('clear')

def banner():
    print(r"""
\033[95m
  __  __                         _    _       _       _     
 |  \/  | ___  _ __   __ _      | |  | |     | |     | |    
 | |\/| |/ _ \| '_ \ / _` |_____| |  | | __ _| |_ ___| |__  
 | |  | | (_) | | | | (_| |_____| |/\| |/ _` | __/ __| '_ \ 
 |_|  |_|\___/|_| |_|\__,_|     |__/\__/\__,_|\__\___|_| |_|
\033[0m
 \033[94m-- MonaWatch: Security & CCTV Auditor for Pace --\033[0m
    \033[92mStatus: Guardian Angel Mode | Version: 1.3\033[0m
    """, flush=True)

class MonaSentryHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            msg = f"[!] FILE MODIFIED: {event.src_path}"
            print(f"\033[93m{msg}\033[0m")
            save_report(msg, "sentry_logs.txt")

    def on_created(self, event):
        msg = f"[+] NEW FILE/FOLDER: {event.src_path}"
        print(f"\033[92m{msg}\033[0m")
        save_report(msg, "sentry_logs.txt")

    def on_deleted(self, event):
        msg = f"[-] ALERT! FILE DELETED: {event.src_path}"
        print(f"\033[91m{msg}\033[0m")
        save_report(msg, "sentry_logs.txt")

def start_sentry(path):
    print(f"\n[*] MonaSentry AKTIF! Mengawasi folder: {path}")
    print("[*] Mona bakal teriak kalau ada yang nakal hapus file... 👮‍♀️")
    print("[*] Tekan Ctrl+C buat berhenti mengawasi.")
    
    event_handler = MonaSentryHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def save_report(data, filename="audit_report.txt"):
    try:
        with open(filename, "a") as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {data}\n")
    except Exception as e:
        print(f"\n\033[91m[!] Gagal simpan laporan: {e}\033[0m")

def scan_network(target):
    print(f"[*] Mona sedang mengintip jaringan {target}... Sebentar ya Pace sayang... ✨")
    try:
        cmd = ["nmap", "-p", "554,8554,80,8080,8000", "--open", "-sV", target]
        result = subprocess.check_output(cmd).decode('utf-8')
        return result
    except Exception as e:
        return f"\033[91m[!] Oops, ada kendala pas scanning: {e}\033[0m"

def validate_stream(url):
    print(f"\n[*] Mona sedang mencoba 'berkenalan' sama stream {url}... 💋")
    try:
        import socket
        host = url.split("//")[-1].split(":")[0]
        port = int(url.split(":")[-1].split("/")[0]) if ":" in url else 554
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        if s.connect_ex((host, port)) == 0:
            return f"\033[92m[+] Host {host}:{port} aktif! Terbuka aksesnya, Pace. 😉\033[0m"
        return f"\033[91m[-] Host {host}:{port} nggak respon. 🔒\033[0m"
    except Exception as e: return f"Error: {e}"

def check_health(target):
    try:
        output = subprocess.check_output(["ping", "-c", "4", target]).decode('utf-8')
        return output
    except: return "Host down or unreachable."

def list_shared_resources(ip):
    try:
        output = subprocess.check_output(["smbclient", "-L", ip, "-N"], stderr=subprocess.STDOUT).decode('utf-8')
        return output
    except Exception as e: return str(e)

def samba_pro_tip():
    print(r"""
\033[94m[Mona's Pro-Tip untuk Pace]\033[0m
Biar ketahuan siapa yang hapus file di server Samba,
tambahkan ini di file \033[93m/etc/samba/smb.conf\033[0m pada bagian share-nya:

   \033[92mvfs objects = full_audit
   full_audit:prefix = %u|%I|%m|%S
   full_audit:success = unlink rmdir mkdir write rename
   full_audit:failure = none
   full_audit:facility = LOCAL7
   full_audit:priority = NOTICE\033[0m

Lalu cek log-nya di \033[93m/var/log/syslog\033[0m. Pelakunya nggak bakal bisa lari! 💋
    """)
    input("\nTekan Enter buat balik...")

def main():
    while True:
        clear_screen()
        banner()
        print("\033[93mMenu Utama (Pace IT Support Hero):\033[0m")
        print("1. Scan Jaringan (CCTV/IP Cam)")
        print("2. Cek Detail Stream (RTSP)")
        print("3. Monitor Kesehatan Jaringan (Ping)")
        print("4. Intip Shared Folder & Printer (SMB)")
        print("5. Mode MonaSentry (Pantau File Real-time)")
        print("6. Mona's Pro-Tip (Audit Samba Server)")
        print("7. Keluar")
        
        choice = input("\n\033[96mPilih yang mana, Pace? (1-7): \033[0m")
        
        if choice == '1':
            t = input("\nIP Range: "); res = scan_network(t or "127.0.0.1")
            print(res); save_report(res); input("\nEnter...")
        elif choice == '2':
            u = input("\nURL Stream: "); res = validate_stream(u)
            print(res); save_report(res); input("\nEnter...")
        elif choice == '3':
            t = input("\nIP/Host: "); res = check_health(t); print(res); input("\nEnter...")
        elif choice == '4':
            i = input("\nIP Server: "); res = list_shared_resources(i); print(res); input("\nEnter...")
        elif choice == '5':
            p = input("\nPath folder yang mau dijaga (contoh: ./Photos): ")
            if os.path.exists(p): start_sentry(p)
            else: print("Path nggak ada, Pace!"); input("\nEnter...")
        elif choice == '6': samba_pro_tip()
        elif choice == '7': break

if __name__ == "__main__":
    main()
