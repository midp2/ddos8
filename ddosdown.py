import socket
import time

# Fungsi untuk mengirimkan packet
def send_packets(target, port=80, duration=10800):  # 10800 detik = 3 jam
    try:
        # Membuat socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)  # Timeout untuk menghindari hanging
        s.connect((target, port))  # Menghubungkan ke target
        
        total_packets = 0
        packets_per_notification = 1000000  # 1 juta packet per notifikasi
        start_time = time.time()  # Waktu mulai
        
        print(f"Starting packet sender to {target}...")
        print(f"Duration set to {duration} seconds (3 hours)")
        
        # Loop sampai durasi 3 jam tercapai
        while (time.time() - start_time) < duration:
            # Mengirimkan packet (data kecil untuk simulasi)
            s.send(b"GET / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n")
            total_packets += 1
            
            # Notifikasi setiap 1 juta packet
            if total_packets % packets_per_notification == 0:
                elapsed_time = time.time() - start_time
                print(f"Sent {total_packets:,} packets (Elapsed time: {int(elapsed_time)} seconds)")
        
        s.close()
        elapsed_time = time.time() - start_time
        print(f"Finished sending {total_packets:,} packets in {int(elapsed_time)} seconds")
        
    except Exception as e:
        print(f"Error occurred - {str(e)}")

# Contoh penggunaan
if __name__ == "__main__":
    # Ganti dengan IP atau domain target (gunakan server lokal untuk testing)
    target_website = "127.0.0.1"  # Contoh: localhost untuk testing
    port = 80  # Port default HTTP
    
    # Jalankan pengiriman packet selama 3 jam
    send_packets(target_website, port)