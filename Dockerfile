# Gunakan image Python resmi sebagai dasar
FROM python:3.11-slim

# Install dependensi sistem yang dibutuhkan MonaWatch
RUN apt-get update && apt-get install -y \
    nmap \
    smbclient \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Tentukan direktori kerja di dalam container
WORKDIR /app

# Salin file requirements dulu untuk optimasi cache
COPY requirements.txt .

# Install dependensi Python
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh kode aplikasi kita ke dalam container
COPY . .

# Buat folder log dan file yang dibutuhkan agar tidak error
RUN touch audit_report.txt sentry_logs.txt known_devices.json health_history.json brain_notes.json && \
    chmod 777 audit_report.txt sentry_logs.txt known_devices.json health_history.json brain_notes.json

# Port standar untuk Hugging Face Spaces
EXPOSE 7860

# Jalankan aplikasi menggunakan gunicorn agar lebih profesional dan stabil
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "--workers", "1", "--threads", "8", "app:app"]
