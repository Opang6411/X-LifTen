import penyimpanan
import tampilan

def login():
    tampilan.clear()
    
    try:
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
        for a in penyimpanan.akun:
            if a.get("username") == username and a.get("password") == password:
                print(f"\nLogin berhasil! Selamat datang, {username} ({a.get('role')})\n")
                tampilan.pause(2, "Melanjutkan...")
                return a
        
        print("Username atau password salah!\n")
        tampilan.pause(2, "Coba lagi...")
        return None
        
    except Exception as e:
        print(f"❌ Kesalahan saat mencoba login: {e}")
        print("Pastikan data akun telah dimuat dengan benar.")
        tampilan.pause(3, "Kembali ke menu utama...")
        return None

def register():
    while True:
        tampilan.clear()
        username = input("Username baru: ").strip()

        try:
            if not username:
                print("Username tidak boleh kosong.\n")
            elif " " in username:
                print("Username tidak boleh mengandung spasi.\n")
            elif username.lower() == "admin":
                print("Username 'admin' tidak diperbolehkan.\n")
            elif any(a.get("username", "").lower() == username.lower() for a in penyimpanan.akun):
                print("Username sudah digunakan!\n")
            else:
                break
                
        except Exception as e:
            print(f"❌ Kesalahan akses data saat pengecekan username: {e}")
            tampilan.pause(3, "Coba lagi nanti...")
            return

        tampilan.pause(2, "Coba lagi...")
        continue

    while True:
        password = input("Password baru: ").strip()
        if len(password) < 3:
            print("Password minimal 3 karakter.\n")
            tampilan.pause(2, "Coba lagi...")
            continue
        break

    while True:
        langganan = input("Apakah ingin berlangganan Pro? (y/n): ").lower().strip()
        if langganan == "y":
            role = "pro"
            break
        elif langganan == "n":
            role = "user"
            break
        print("Input tidak valid. Masukkan 'y' atau 'n'.\n")
        tampilan.pause(2, "Coba lagi...")
        
    try:
        penyimpanan.akun.append({
            "username": username,
            "password": password,
            "role": role,
            "history": []
        })
        penyimpanan.save_akun()

        print(f"Akun '{username}' berhasil dibuat dengan role '{role}'!\n")
        tampilan.pause(2, "Melanjutkan...")

    except Exception as e:
        print(f"❌ GAGAL menyimpan akun '{username}'. Terjadi kesalahan I/O: {e}")
        tampilan.pause(3, "Kembali ke menu utama...")