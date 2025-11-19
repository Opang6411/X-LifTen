import os
import random
import storage
import anime_crud
import account_crud


def clear_screen():
    os.system('cls')


def menu_admin():
    while True:
        print("\n=== MENU ADMIN ===")
        print("1. Tampilkan semua anime")
        print("2. Update anime (episode & akses)")
        print("3. Tambah anime baru")
        print("4. Hapus anime")
        print("5. Menu akun")
        print("6. Logout")

        pilihan = input("Masukkan pilihanmu ⟶ ")

        if pilihan == "1":
            anime_crud.tampilkan_anime()
        elif pilihan == "2":
            anime_crud.update_anime()
        elif pilihan == "3":
            anime_crud.tambah_anime()
        elif pilihan == "4":
            anime_crud.hapus_anime()
        elif pilihan == "5":
            menu_akun()
        elif pilihan == "6":
            break
        else:
            print("❌ Pilihan tidak valid!\n")


def menu_akun():
    while True:
        print("\n=== MENU AKUN ===")
        print("1. Tampilkan semua akun")
        print("2. Ubah role akun")
        print("3. Hapus akun")
        print("4. Kembali")

        pilihan = input("Masukkan pilihanmu ⟶ ")

        if pilihan == "1":
            account_crud.tampilkan_akun()
        elif pilihan == "2":
            account_crud.ubah_role_akun()
        elif pilihan == "3":
            account_crud.hapus_akun()
        elif pilihan == "4":
            break
        else:
            print("❌ Pilihan tidak valid!\n")


def menu_user(user):
    while True:
        print("\n=== MENU USER ===")
        rekomendasi_hari_ini()
        print("1. Mau nonton anime")
        print("2. Riwayat tontonan")
        print("3. Logout")

        pilihan = input("Masukkan pilihanmu ⟶ ")

        if pilihan == "1":
            tonton_anime(user.get("role"))
        elif pilihan == "2":
            print("Riwayat tontonan masih kosong.\n")
        elif pilihan == "3":
            break
        else:
            print("❌ Pilihan tidak valid!\n")


def rekomendasi_hari_ini():
    anime = random.sample(storage.data_anime, k=min(4, len(storage.data_anime))) if storage.data_anime else []
    print("\n🎯 Rekomendasi hari ini:")
    for a in anime:
        print(f"- {a['judul']}")


def tonton_anime(user_role):
    anime_crud.tampilkan_anime()
    try:
        pilih = int(input("Pilih ID anime yang ingin ditonton: "))
    except ValueError:
        print("Input tidak valid.\n")
        return
    anime = next((a for a in storage.data_anime if a["id"] == pilih), None)
    if not anime:
        print("Anime tidak ditemukan.\n")
        return
    print(f"\n🎬 {anime['judul']}")
    for i, ep in enumerate(anime.get("episodes", []), start=1):
        if ep.get("akses") == "premium" and user_role != "pro":
            print(f"{i}. {ep['judul']} (Terkunci 🔒)")
        else:
            print(f"{i}. {ep['judul']}")
