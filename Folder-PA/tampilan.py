import os
import random
import time
import sys
from InquirerPy import inquirer

import penyimpanan
import anime_crud
import account_crud

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause(durasi_detik, pesan="Kembali ke menu..."):
    try:
        waktu_mulai = time.time()
        durasi_target = durasi_detik
        
        print(f"\n{pesan}", end="", flush=True) 

        interval = 0.5
        while (time.time() - waktu_mulai) < durasi_target:
            sys.stdout.write(" .")
            sys.stdout.flush() 
            time.sleep(interval)
        
        print() 
        
    except KeyboardInterrupt:
        print("\n\nProses ditunda oleh pengguna.")
    except Exception as e:
        print(f"Kesalahan pada fungsi jeda: {e}")

def rekomendasi():
    try:
        anime_list = random.sample(penyimpanan.data_anime, k=min(4, len(penyimpanan.data_anime))) \
            if penyimpanan.data_anime else []
        
        print("\nRekomendasi hari ini:")
        for a in anime_list:
            print(f"- {a['judul']}")
            
    except KeyError:
        print("⚠️ Kesalahan Data: Struktur data anime tidak lengkap.")
    except ValueError:
        print("⚠️ Tidak dapat menampilkan rekomendasi.")

def menu_tampil_anime(data):
    halaman = 1
    keyword = ""
    per_halaman = 5
    
    while True:
        try:
            clear()
            if keyword:
                tampil = [a for a in data if keyword.lower() in a["judul"].lower()]
            else:
                tampil = data

            total = len(tampil)
            if total == 0:
                print("\nTidak ada anime yang cocok dengan pencarian.\n")
                pause(2, "Kembali ke daftar anime...")
                return None

            total_halaman = (total + per_halaman - 1) // per_halaman
            halaman = max(1, min(halaman, total_halaman))
            start = (halaman - 1) * per_halaman
            end = start + per_halaman

            page_items = tampil[start:end]

            print("\n=== LIST ANIME ===")
            print(f"Halaman {halaman}/{total_halaman} | Total: {total} anime")
            print(f"Search: '{keyword}'\n")

            for a in page_items:
                print(f"{a['id']}. {a['judul']} ({a['genre']}) - Rating {a['rating']}")

            print("\n(N) Next | (P) Prev | (S) Search | (Q) Kembali")
            print("Pilih Anime (Masukkan ID Anime)")

            pilih = input(": ").strip().lower()

            if pilih == "n":
                if halaman < total_halaman:
                    halaman += 1
                else:
                    print("Sudah di halaman terakhir.")
                    pause(2, "Kembali ke daftar anime...")
            elif pilih == "p":
                if halaman > 1:
                    halaman -= 1
                else:
                    print("Sudah di halaman pertama.")
                    pause(2, "Kembali ke daftar anime...")
            elif pilih == "s":
                keyword = input("Masukkan kata pencarian: ").strip()
                halaman = 1
            elif pilih == "q":
                return None
            elif pilih.isdigit():
                pilih_id = int(pilih)
                page_ids = [a["id"] for a in page_items]

                if pilih_id in page_ids:
                    return pilih_id
                else:
                    print("Anime tidak ada di halaman ini. Silakan pilih ID yang ditampilkan.")
                    pause(2, "Kembali ke daftar anime...")
            else:
                print("Input tidak valid.")
                pause(2, "Kembali ke daftar anime...")
                
        except ZeroDivisionError:
            print("❌ Kesalahan internal: Pembagian per halaman bermasalah.")
            pause(3, "Kembali...")
            return None
        except Exception as e:
            print(f"❌ Kesalahan tak terduga dalam menu tampil anime: {e}")
            pause(3, "Kembali...")
            return None

def admin_lihat_anime():
    while True:
        anime_id = menu_tampil_anime(penyimpanan.data_anime)
        if anime_id is None:
            break
        
        try:
            anime = next((a for a in penyimpanan.data_anime if a["id"] == anime_id), None)
            if anime is None:
                print("Anime tidak ditemukan.\n")
                continue
            print(f"\n{anime['judul']} ({anime['genre']}) - Rating {anime['rating']}")
            episodes = anime.get("episodes", [])
            if episodes:
                for i, ep in enumerate(episodes, start=1):
                    print(f"{i}. {ep['judul']} ({ep['akses']})")
            else:
                print("Anime ini belum memiliki episode.")
            
            pause(2, "Kembali ke daftar anime...")
        except Exception as e:
            print(f"❌ Kesalahan saat melihat detail anime: {e}")
            pause(3, "Kembali...")


def menu_admin():
    while True:
        try:
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
                ]
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
        except KeyboardInterrupt:
            print("\n👋 Program dihentikan. Logout otomatis...")
            pause(2)
            break
        except Exception as e:
            print(f"\nTerjadi kesalahan di menu admin: {e}\n")
            time.sleep(2)

def menu_admin_akun():
    while True:
        try:
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
                input("Tekan Enter untuk kembali...")
            elif pilihan == "Ubah role akun":
                account_crud.ubah_role_akun()
            elif pilihan == "Hapus akun":
                account_crud.hapus_akun()
            elif pilihan == "Kembali":
                break
        except KeyboardInterrupt:
            print("\n👋 Menu dihentikan. Kembali ke menu utama...")
            pause(2)
            break
        except Exception as e:
            print(f"Terjadi kesalahan di menu akun: {e}")
            time.sleep(2)

def tonton_anime(user):
    while True:
        try:
            anime_id = menu_tampil_anime(penyimpanan.data_anime)
        except Exception as e:
            print(f"❌ Kesalahan saat menampilkan daftar anime: {e}")
            time.sleep(2)
            break

        if anime_id is None:
            break

        anime = next((a for a in penyimpanan.data_anime if a["id"] == anime_id), None)
        if anime is None:
            print("Anime tidak ditemukan.\n")
            pause(2, "Kembali ke menu...")
            continue

        print(f"\n{anime['judul']}")
        for i, ep in enumerate(anime.get("episodes", []), start=1):
            if ep.get("akses") == "premium" and user.get("role") != "pro":
                print(f"{i}. {ep['judul']} (Terkunci 🔒)")
            else:
                print(f"{i}. {ep['judul']}")

        try:
            pilih_ep = int(input("Pilih episode yang ingin ditonton (0 untuk kembali): "))
        except ValueError:
            print("❌ Input tidak valid. Episode harus berupa angka.\n")
            pause(2, "Kembali ke menu...")
            continue

        if pilih_ep == 0:
            continue

        episodes = anime.get("episodes", [])
        if not (1 <= pilih_ep <= len(episodes)):
            print("Episode tidak ditemukan.\n")
            pause(2, "Kembali ke menu...")
            continue

        episode = episodes[pilih_ep - 1]
        if episode.get("akses") == "premium" and user.get("role") != "pro":
            print("Episode ini terkunci. Upgrade ke Pro untuk menonton episode premium.\n")
            pause(3, "Kembali ke menu...")
            continue

        clear()
        print(f"\nMenonton {anime['judul']} - {episode['judul']}...\n")
        
        for i in range(5, 0, -1):
            sys.stdout.write(f"Video akan habis dalam {i} detik... \r")
            sys.stdout.flush()
            time.sleep(1)
            
        print("Video selesai ditonton!                                 \n")

        try:
            user.setdefault("history", []).append({
                "anime": anime["judul"],
                "episode": episode["judul"]
            })
            penyimpanan.save_akun()
        except Exception as e:
            print(f"❌ Gagal menyimpan riwayat tontonan: {e}")
            pause(3)

        if not anime_crud.mau_lagi():
            break

def tampilkan_riwayat(user):
    clear()
    print(f"\n=== Riwayat tontonan {user.get('username')} ===\n")
    history = user.get("history", [])
    if not history:
        print("Riwayat tontonan masih kosong.\n")
    else:
        try:
            for i, h in enumerate(history, start=1):
                print(f"{i}. {h['anime']} - {h['episode']}")
        except KeyError as e:
            print(f"❌ Kesalahan data riwayat: Kunci {e} hilang.")
            
    pause(3, "Kembali ke menu...")

def menu_user(user):
    while True:
        try:
            clear()
            print("\n=== MENU USER ===")
            rekomendasi()
            print("\n")
            pilihan = inquirer.select(
                message="Pilih menu:",
                choices=[
                    "Nonton Anime",
                    "Riwayat tontonan",
                    "Logout"
                ]
            ).execute()

            if pilihan == "Nonton Anime":
                tonton_anime(user)
            elif pilihan == "Riwayat tontonan":
                tampilkan_riwayat(user)
            elif pilihan == "Logout":
                break
        except KeyboardInterrupt:
            print("\n👋 Program dihentikan. Logout otomatis...")
            pause(2)
            break
        except Exception as e:
            print(f"\nTerjadi kesalahan di menu user: {e}")
            time.sleep(2)