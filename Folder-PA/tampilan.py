import os
import random
import penyimpanan
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
    anime = random.sample(penyimpanan.data_anime, k=min(4, len(penyimpanan.data_anime))) if penyimpanan.data_anime else []
    print("\n🎯 Rekomendasi hari ini:")
    for a in anime:
        print(f"- {a['judul']}")


def tonton_anime(user_role):
    data = penyimpanan.data_anime[:]  # Copy data
    halaman = 1
    per_halaman = 5
    keyword = ""

    while True:
        # FILTER SEARCH
        if keyword:
            tampil = [a for a in data if keyword.lower() in a["judul"].lower()]
        else:
            tampil = data

        # HITUNG PAGINATION
        total = len(tampil)
        total_halaman = (total + per_halaman - 1) // per_halaman

        if halaman < 1:
            halaman = 1
        if halaman > total_halaman:
            halaman = total_halaman

        start = (halaman - 1) * per_halaman
        end = start + per_halaman

        print("\n=== LIST ANIME ===")
        print(f"Halaman {halaman}/{total_halaman} | Total: {total} anime")
        print(f"Search: '{keyword}'\n")

        # TAMPILKAN DATA SESUAI PAGINATION
        for a in tampil[start:end]:
            print(f"{a['id']}. {a['judul']} ({a['genre']}) - Rating {a['rating']}")

        print("\n(N) Next | (P) Prev | (S) Search | (Q) Kembali")
        print("(ID) Pilih anime untuk ditonton")

        pilih = input("→ ").strip().lower()

        # --- NAVIGASI PAGINATION ---
        if pilih == "n":
            halaman += 1
        elif pilih == "p":
            halaman -= 1

        # --- MENU SEARCH REAL-TIME ---
        elif pilih == "s":
            keyword = input("Masukkan kata pencarian: ").strip()
            halaman = 1  # Reset ke halaman pertama saat search

        # --- KELUAR ---
        elif pilih == "q":
            break

        # --- PILIH ANIME ---
        elif pilih.isdigit():
            pilih = int(pilih)
            anime = next((a for a in tampil if a["id"] == pilih), None)
            
            if not anime:
                print("❌ Anime tidak ditemukan dalam hasil.")
                continue

            print(f"\n🎬 {anime['judul']}")
            for i, ep in enumerate(anime.get("episodes", []), start=1):
                if ep.get("akses") == "premium" and user_role != "pro":
                    print(f"{i}. {ep['judul']} (Terkunci 🔒)")
                else:
                    print(f"{i}. {ep['judul']}")
            print()
            input("Tekan Enter untuk kembali...")
        else:
            print("❌ Input tidak valid.")




