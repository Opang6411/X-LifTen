import os
import random
import penyimpanan
import anime_crud
import account_crud
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
import time

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_admin():
    while True:
        clear()
        pilihan = inquirer.select(
            message="=== MENU ADMIN ===",
            choices=[
                "Tampilkan semua anime",
                "Update anime (episode & akses)",
                "Tambah anime baru",
                "Hapus anime",
                "Menu akun",
                "Logout"
            ],
            default=None
        ).execute()

        if pilihan == "Tampilkan semua anime":
            admin_lihat_anime()
        elif pilihan == "Update anime (episode & akses)":
            anime_crud.update_anime()
        elif pilihan == "Tambah anime baru":
            anime_crud.tambah_anime()
        elif pilihan == "Hapus anime":
            anime_crud.hapus_anime()
        elif pilihan == "Menu akun":
            menu_admin_akun()
        elif pilihan == "Logout":
            break


def menu_admin_akun():
    while True:
        clear()
        pilihan = inquirer.select(
            message="=== MENU AKUN ===",
            choices=[
                "Tampilkan semua akun",
                "Ubah role akun",
                "Hapus akun",
                "Kembali"
            ]
        ).execute()
        if pilihan == "Tampilkan semua akun":
            account_crud.tampilkan_akun()
        elif pilihan == "Ubah role akun":
            account_crud.ubah_role_akun()
        elif pilihan == "Hapus akun":
            account_crud.hapus_akun()
        elif pilihan == "Kembali":
            break

def menu_user(user):
    while True:
        clear()
        print("\n=== MENU USER ===")
        rekomendasi_hari_ini()  
        pilihan = inquirer.select(
            message="Pilih menu:",
            choices=[
                "Mau nonton anime",
                "Riwayat tontonan",
                "Logout"
            ]
        ).execute()
        if pilihan == "Mau nonton anime":
            tonton_anime(user)
        elif pilihan == "Riwayat tontonan":
            tampilkan_riwayat(user)
        elif pilihan == "Logout":
            break

def rekomendasi_hari_ini():
    anime = random.sample(penyimpanan.data_anime, k=min(4, len(penyimpanan.data_anime))) if penyimpanan.data_anime else []
    print("\nRekomendasi hari ini:")
    for a in anime:
        print(f"- {a['judul']}")

def menu_tampil_anime(data):
    halaman = 1
    keyword = ""
    per_halaman=5
    while True:
        if keyword:
            tampil = [a for a in data if keyword.lower() in a["judul"].lower()]
        else:
            tampil = data
        total = len(tampil)
        if total == 0:
            print("\nTidak ada anime yang cocok dengan pencarian.\n")
            keyword = ""
            halaman = 1
            continue
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
        for a in tampil[start:end]:
            print(f"{a['id']}. {a['judul']} ({a['genre']}) - Rating {a['rating']}")
        print("\n(N) Next | (P) Prev | (S) Search | (Q) Kembali")
        print("Pilih Anime (Masukkan ID Anime)")
        pilih = input(": ").strip().lower()
        if pilih == "n":
            halaman += 1
        elif pilih == "p":
            halaman -= 1
        elif pilih == "s":
            keyword = input("Masukkan kata pencarian: ").strip()
            halaman = 1
        elif pilih == "q":
            return None
        elif pilih.isdigit():
            pilih_id = int(pilih)
            if any(a["id"] == pilih_id for a in tampil):
                return pilih_id
            else:
                print("Anime tidak ditemukan dalam hasil.")
        else:
            print("Input tidak valid.")

def tonton_anime(user):
    while True:
        anime_id = menu_tampil_anime(penyimpanan.data_anime)
        if anime_id is None:
            break
        anime = next(a for a in penyimpanan.data_anime if a["id"] == anime_id)
        print(f"\n{anime['judul']}")
        for i, ep in enumerate(anime.get("episodes", []), start=1):
            if ep.get("akses") == "premium" and user.get("role") != "pro":
                print(f"{i}. {ep['judul']} (Terkunci 🔒)")
            else:
                print(f"{i}. {ep['judul']}")
        try:
            pilih_ep = int(input("Pilih episode yang ingin ditonton (0 untuk kembali): "))
        except ValueError:
            print("Input tidak valid.\n")
            continue
        if pilih_ep == 0:
            continue
        if not (1 <= pilih_ep <= len(anime.get("episodes", []))):
            print("Episode tidak ditemukan.\n")
            continue
        episode = anime["episodes"][pilih_ep - 1]
        if episode.get("akses") == "premium" and user.get("role") != "pro":
            print("Episode ini terkunci. Upgrade ke Pro untuk menonton episode premium.\n")
            continue
        clear()
        print(f"\nMenonton {anime['judul']} - {episode['judul']}...\n")
        for i in range(5, 0, -1):
            print(f"Video akan habis dalam {i} detik...", end="\r")
            time.sleep(1)
        print("Video selesai ditonton!                      \n")
        user["history"].append({
            "anime": anime["judul"],
            "episode": episode["judul"]
        })
        penyimpanan.save_akun()
        if not anime_crud.mau_lagi():
            break

def tampilkan_riwayat(user):
    clear()
    print(f"\n=== Riwayat tontonan {user.get('username')} ===\n")
    history = user.get("history", [])
    if not history:
        print("Riwayat tontonan masih kosong.\n")
    else:
        for i, h in enumerate(history, start=1):
            print(f"{i}. {h['anime']} - {h['episode']}")
    input("\nTekan Enter untuk kembali...")

def admin_lihat_anime():
    while True:
        anime_id = menu_tampil_anime(penyimpanan.data_anime)
        if anime_id is None: 
            break
        anime = next(a for a in penyimpanan.data_anime if a["id"] == anime_id)
        print(f"\n{anime['judul']} ({anime['genre']}) - Rating {anime['rating']}")
        if anime.get("episodes"):
            for i, ep in enumerate(anime["episodes"], start=1):
                print(f"{i}. {ep['judul']} ({ep['akses']})")
        else:
            print("Anime ini belum memiliki episode.")
        input("\nTekan Enter untuk kembali...")