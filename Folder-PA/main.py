import auth
import tampilan

def main():
    while True:
        tampilan.clear()
        print("=== X-LifTen Anime & Donghua Streaming ===")
        print("1. Login")
        print("2. Register")
        print("3. Keluar")
        pilihan = input("Masukkan pilihanmu : ")
        if pilihan == "1":
            user = auth.login()
            if not user:
                continue
            if user.get("role") == "admin":
                tampilan.menu_admin()
            else:
                tampilan.menu_user(user)
        elif pilihan == "2":
            auth.register()
        elif pilihan == "3":
            print("Terima kasih telah menggunakan X-LifTen!")
            input("Tekan Enter untuk keluar...")
            break
        else:
            print("Pilihan tidak valid!\n")
            print("coba ulangi lagi")

main()


