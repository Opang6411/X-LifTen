import os
import random
import time
import sys
from InquirerPy import inquirer

import penyimpanan
import anime_crud # Dipanggil di tonton_anime dan menu admin
import account_crud # Dipanggil di menu admin

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
    except Exception:
        pass

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

            choices = ["(N) Next", "(P) Prev", "(S) Search", "(Q) Kembali"]
            # Menambahkan ID Anime yang ditampilkan sebagai pilihan cepat
            choices.extend([f"ID: {a['id']} ({a['judul']})" for a in page_items])

            pilih = inquirer.select(
                message="\nNavigasi atau Pilih Anime:",
                choices=choices
            ).execute().lower()

            if pilih.startswith("(n)"):
                if halaman < total_halaman:
                    halaman += 1
                else:
                    print("Sudah di halaman terakhir.")
                    pause(1)
            elif pilih.startswith("(p)"):
                if halaman > 1:
                    halaman -= 1
                else:
                    print("Sudah di halaman pertama.")
                    pause(1)
            elif pilih.startswith("(s)"):
                keyword = input("Masukkan kata pencarian: ").strip()
                halaman = 1
            elif pilih.startswith("(q)"):
                return None
            elif pilih.startswith("id:"):
                pilih_id = int(pilih.split(":")[1].split("(")[0].strip())
                return pilih_id
            
        except KeyboardInterrupt:
            print("\nOperasi dibatalkan.\n")
            pause(2)
            return None
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
        try:
            anime_id = menu_tampil_anime(penyimpanan.data_anime)
            if anime_id is None:
                break
            
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
            
        except KeyboardInterrupt:
            print("\nOperasi dibatalkan.\n")
            pause(2)
            break
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

        choices_ep = []
        episodes = anime.get("episodes", [])
        
        for i, ep in enumerate(episodes, start=1):
            judul = ep.get('judul', 'Episode Tidak Diketahui')
            akses = ep.get('akses', 'gratis')
            
            if akses == "premium" and user.get("role") != "pro":
                choices_ep.append({"name": f"{i}. {judul} (Terkunci 🔒)", "value": i, "enabled": False})
            else:
                choices_ep.append({"name": f"{i}. {judul}", "value": i})

        choices_ep.append({"name": "Batal/Kembali", "value": 0})

        if not episodes:
            print("Anime ini belum memiliki episode yang bisa ditonton.\n")
            pause(2)
            continue

        try:
            pilih_ep_value = inquirer.select(
                message=f"Pilih episode {anime['judul']} ({len(episodes)} total):",
                choices=choices_ep
            ).execute()
        except KeyboardInterrupt:
            print("\nPemilihan dibatalkan.")
            pause(2)
            break

        if pilih_ep_value == 0:
            continue
        
        pilih_ep = int(pilih_ep_value)
        episode = episodes[pilih_ep - 1]

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
    print(f"\n=== Riwayat tontonan {user.get('username')} ({user.get('role').upper()}) ===\n")
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
                message=f"Halo {user.get('username')} ({user.get('role').upper()}). Pilih menu:",
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