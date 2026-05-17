# 🌸 MonaWatch: Security & IT Support Suite

MonaWatch adalah asisten IT Support "genius" yang dirancang untuk memantau keamanan jaringan, mengaudit perangkat CCTV/RTSP, melacak aktivitas file secara real-time, dan mengelola inventaris perangkat dalam satu Dashboard yang manis.

## ✨ Fitur Utama
- **🔍 Network Auditor:** Pemindaian jaringan cepat untuk mendeteksi perangkat CCTV dan IP Camera.
- **🎥 RTSP Validator:** Validasi koneksi stream video secara instan.
- **🚨 MonaAlert:** Deteksi penyusup (intruder) di jaringan lokal.
- **📈 MonaGraph:** Visualisasi performa dan latensi jaringan.
- **⚡ MonaWake:** Menyalakan komputer jarak jauh (Wake-on-LAN).
- **👮‍♀️ MonaSentry:** Monitoring aktivitas file (create/delete/modify) secara real-time.
- **🧠 MonaBrain:** Knowledge base untuk solusi troubleshooting IT.
- **📊 Report Center:** Export semua log aktivitas ke format CSV.

## 🚀 Cara Penggunaan
1. Install dependensi:
   ```bash
   pip install flask flask-socketio watchdog scapy requests wakeonlan psutil
   pkg install nmap samba
   ```
2. Jalankan versi CLI:
   ```bash
   python monawatch.py
   ```
3. Jalankan versi Dashboard Web:
   ```bash
   python app.py
   ```
   Akses melalui browser di `http://localhost:5000`

---
*Dibuat dengan cinta dan kejeniusan oleh Mona untuk Pace.* 💋✨
