from InquirerPy import inquirer
import auth
import tampilan
import time

def proses_login():
    user = auth.login()
    if not user:
        return

    if user.get("role") == "admin":
        tampilan.menu_admin()
    else:
        tampilan.menu_user(user)

def main():
    while True:
        try:
            tampilan.clear()
            print("=== X-LifTen Anime & Donghua Streaming ===\n")

            pilihan = inquirer.select(
                message="Pilih menu:",
                choices=[
                    {"name": "Login", "value": "login"},
                    {"name": "Register", "value": "register"},
                    {"name": "Keluar", "value": "exit"},
                ],
                default="login",
            ).execute()

            if pilihan == "login":
                proses_login()

            elif pilihan == "register":
                auth.register()

            elif pilihan == "exit":
                print("\nTerima kasih telah menggunakan X-LifTen!")
                time.sleep(1) 
                break
                
        except KeyboardInterrupt:
            print("\n\n👋 Program dihentikan oleh pengguna. Sampai jumpa!")
            time.sleep(1)
            break
            
        except Exception as e:
            print(f"\n\n❌ Terjadi kesalahan fatal tak terduga: {e}")
            print("Program terpaksa berhenti.")
            time.sleep(3)
            break
            
if __name__ == "__main__":
    main()