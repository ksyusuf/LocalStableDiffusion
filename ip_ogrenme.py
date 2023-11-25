import os
import socket


def get_ip_address():
    # Socket oluştur
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Google'ın DNS sunucusuna bağlan
        s.connect(('8.8.8.8', 80))
        ip_address = s.getsockname()[0]
    except socket.error:
        ip_address = '127.0.0.1'  # Eğer bağlantı kurulamazsa varsayılan IP adresi

    finally:
        s.close()

    return ip_address


def get_port():
    port = int(os.environ.get('PORT', 8000))
    return port


ip_address = get_ip_address()
port = get_port()

print(f"Sunucu IP adresi: {ip_address}")
print(f"Kullanılan port: {port}")
