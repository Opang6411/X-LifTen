import penyimpanan
import tampilan

def tampilkan_akun():
    try:
        if not penyimpanan.akun:
            print("Tidak ada akun.\n")
            tampilan.pause(2, "Kembali ke menu sebelumnya...")
            return

        for i, a in enumerate(penyimpanan.akun, start=1):
            username = a.get("username", "(nama tidak valid)")
            role = a.get("role", "user")
            print(f"{i}. {username} — Role: {role}")
        print("")

    except Exception as e:
        print(f"❌ Kesalahan saat menampilkan akun: {e}")
        print("Pastikan `penyimpanan.akun` diinisialisasi dengan benar.")
        tampilan.pause(3)

def ubah_role_akun():
    try:
        if not penyimpanan.akun:
            print("Tidak ada akun.\n")
            tampilan.pause(2, "Kembali ke menu sebelumnya...")
            return

        tampilkan_akun()

        try:
            pilih = int(input("Masukkan nomor akun yang ingin diubah role-nya (ketik 0 untuk batal): "))
            if pilih == 0:
                return
            if not (1 <= pilih <= len(penyimpanan.akun)):
                print("Nomor akun tidak valid.\n")
                tampilan.pause(2, "Kembali ke menu sebelumnya...")
                return
        except ValueError:
            print("Input tidak valid. Masukkan angka.\n")
            tampilan.pause(2, "Kembali ke menu sebelumnya...")
            return

        user = penyimpanan.akun[pilih - 1]

        if user.get("role") == "admin":
            print("Admin tidak bisa diubah role-nya.\n")
            tampilan.pause(2, "Kembali ke menu sebelumnya...")
            return

        while True:
            role_baru = input("Role baru (user/pro): ").lower().strip()
            if role_baru in ["user", "pro"]:
                break
            print("Input tidak valid. Hanya 'user' atau 'pro'.\n")
            tampilan.pause(2, "Coba lagi...")

        user["role"] = role_baru
        penyimpanan.save_akun()

        print(f"Role akun '{user.get('username')}' berhasil diubah menjadi {role_baru}.\n")
        tampilan.pause(2, "Kembali ke menu sebelumnya...")

    except KeyboardInterrupt:
        print("\nOperasi dibatalkan oleh pengguna.\n")
        tampilan.pause(2)
        return
    except Exception as e:
        print(f"❌ Kesalahan saat mengubah role akun: {e}")
        print("Periksa hak akses file dan struktur data akun.")
        tampilan.pause(3)


def hapus_akun():
    try:
        if not penyimpanan.akun:
            print("Tidak ada akun.\n")
            tampilan.pause(2, "Kembali ke menu sebelumnya...")
            return

        non_admin = [a for a in penyimpanan.akun if a.get("role") != "admin"]
        if not non_admin:
            print("Tidak ada akun selain admin yang bisa dihapus.\n")
            tampilan.pause(2, "Kembali ke menu sebelumnya...")
            return

        tampilkan_akun()

        try:
            pilih = int(input("Masukkan nomor akun yang ingin dihapus (ketik 0 untuk batal): "))
            if pilih == 0:
                return
            if not (1 <= pilih <= len(penyimpanan.akun)):
                print("Nomor akun tidak valid.\n")
                tampilan.pause(2, "Kembali ke menu sebelumnya...")
                return
        except ValueError:
            print("Input tidak valid. Masukkan angka.\n")
            tampilan.pause(2, "Kembali ke menu sebelumnya...")
            return

        user = penyimpanan.akun[pilih - 1]

        if user.get("role") == "admin":
            print("Admin tidak bisa dihapus.\n")
            tampilan.pause(2, "Kembali ke menu sebelumnya...")
            return

        konfirmasi = input(f"Yakin ingin menghapus akun '{user.get('username')}'? (y/n): ").lower()
        if konfirmasi == "y":
            penyimpanan.akun.remove(user)
            penyimpanan.save_akun()
            print(f"Akun '{user.get('username')}' telah dihapus!\n")
        elif konfirmasi == 'n':
            print("Penghapusan dibatalkan.\n")
        else:
            print("Input tidak valid. Penghapusan dibatalkan.\n")
            
        tampilan.pause(2, "Kembali ke menu sebelumnya...")
        
    except KeyboardInterrupt:
        print("\nOperasi dibatalkan oleh pengguna.\n")
        tampilan.pause(2)
        return
    except Exception as e:
        print(f"❌ Kesalahan saat menghapus akun: {e}")
        print("Periksa hak akses file dan struktur data akun.")
        tampilan.pause(3)