import auth
import ui


def main():
    while True:
        print("=== X-LifTen Anime Streaming ===")
        print("1. Login")
        print("2. Register")
        print("3. Keluar")

        pilihan = input("Masukkan pilihanmu ⟶ ")

        if pilihan == "1":
            user = auth.login()
            if not user:
                continue
            if user.get("role") == "admin":
                ui.menu_admin()
            else:
                ui.menu_user(user)

        elif pilihan == "2":
            auth.register()

        elif pilihan == "3":
            print("👋 Terima kasih telah menggunakan X-LifTen!")
            break

        else:
            print("❌ Pilihan tidak valid!\n")


if __name__ == '__main__':
    main()


