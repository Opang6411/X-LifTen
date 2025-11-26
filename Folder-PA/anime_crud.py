import penyimpanan
import tampilan
from InquirerPy import inquirer
import sys

def mau_lagi():
    try:
        pilihan = inquirer.select(
            message="Lakukan operasi ini lagi?",
            choices=["Ya", "Tidak"]
        ).execute()
        
        if pilihan == "Ya":
            return True
        elif pilihan == "Tidak":
            print("Kembali...\n")
            input("Tekan Enter untuk melanjutkan...")
            return False
            
    except KeyboardInterrupt:
        return False
    except Exception:
        return False

def tambah_anime():
    while True:
        try:
            tampilan.clear()
            print("=== Tambah Anime ===")

            judul = input("Judul anime (0 untuk kembali): ").strip()
            if judul == "0":
                return
            if judul == "":
                print("Judul tidak boleh kosong.\n")
                tampilan.pause(2, "Kembali ke menu sebelumnya...")
                continue

            judul_bersih = judul.lower()

            if any(a.get("judul", "").strip().lower() == judul_bersih for a in penyimpanan.data_anime):
                print("Anime dengan nama tersebut sudah ada.\n")
                tampilan.pause(2, "Kembali ke menu sebelumnya...")
                continue

            genre = input("Genre: ").strip()
            if genre == "":
                print("Genre tidak boleh kosong.\n")
                tampilan.pause(2, "Kembali ke menu sebelumnya...")
                continue

            while True:
                try:
                    rating = float(input("Rating anime (0-10): "))
                    if not (0 <= rating <= 10):
                        raise ValueError
                    break
                except ValueError:
                    print("Rating tidak valid. Masukkan angka antara 0-10.\n")
                    tampilan.pause(2, "Coba lagi...")

            new_id = max((a.get("id", 0) for a in penyimpanan.data_anime), default=0) + 1

            penyimpanan.data_anime.append({
                "id": new_id,
                "judul": judul.strip(),
                "genre": genre.strip(),
                "rating": rating,
                "episodes": []
            })

            penyimpanan.save_anime()
            print(f"Anime '{judul}' berhasil ditambahkan!\n")
            tampilan.pause(2, "Kembali ke menu sebelumnya...")

            if not mau_lagi():
                break

        except KeyboardInterrupt:
            print("\nOperasi dibatalkan oleh pengguna.\n")
            tampilan.pause(2)
            return
        except Exception as e:
            print(f"❌ Kesalahan saat menambahkan anime: {e}\n")
            tampilan.pause(3, "Kembali ke menu utama...")
            return

def update_anime():
    while True:
        try:
            tampilan.clear()
            anime_id = tampilan.menu_tampil_anime(penyimpanan.data_anime)
            if anime_id is None:
                print("Kembali ke menu sebelumnya...\n")
                tampilan.pause(2, " ")
                break

            anime = next((a for a in penyimpanan.data_anime if a.get("id") == anime_id), None)
            if anime is None:
                print("Anime tidak ditemukan.\n")
                tampilan.pause(2, "Kembali ke menu sebelumnya...")
                continue

            menu = inquirer.select(
                message=f"\nMengupdate {anime.get('judul')}. Pilih opsi:",
                choices=[
                    "Tambah episode baru",
                    "Ubah status akses episode",
                    "Hapus episode",
                    "Batal"
                ]
            ).execute()

            if menu == "Tambah episode baru":
                while True:
                    judul_ep = input("Judul episode baru: ").strip()
                    if judul_ep == "":
                        print("Judul episode tidak boleh kosong.\n")
                        tampilan.pause(2, "Coba lagi...")
                        continue
                    if any(ep.get("judul", "").lower() == judul_ep.lower() for ep in anime.get("episodes", [])):
                        print("Episode dengan nama ini sudah ada. Masukkan judul lain.\n")
                        tampilan.pause(2, "Coba lagi...")
                        continue
                    break

                while True:
                    akses = input("Akses episode (gratis/premium): ").lower()
                    if akses in ["gratis", "premium"]:
                        break
                    print("Input tidak valid. Hanya 'gratis' atau 'premium'.\n")
                    tampilan.pause(2, "Coba lagi...")

                anime.setdefault("episodes", []).append({
                    "judul": judul_ep,
                    "akses": akses
                })
                penyimpanan.save_anime()
                print(f"Episode '{judul_ep}' berhasil ditambahkan.\n")
                tampilan.pause(2, "Kembali ke menu sebelumnya...")

            elif menu == "Ubah status akses episode":
                episodes = anime.get("episodes", [])
                if not episodes:
                    print("Anime ini belum memiliki episode.\n")
                    tampilan.pause(2, "Kembali ke menu sebelumnya...")
                    continue
                print("\nDaftar Episode:")
                for i, ep in enumerate(episodes, start=1):
                    print(f"{i}. {ep.get('judul')} ({ep.get('akses')})")
                
                try:
                    idx = int(input("Pilih nomor episode yang ingin diubah (0 untuk batal): "))
                    if idx == 0:
                        continue
                    if not (1 <= idx <= len(episodes)):
                        print("Episode tidak ditemukan.\n")
                        tampilan.pause(2, "Kembali ke menu sebelumnya...")
                        continue
                except ValueError:
                    print("Input tidak valid. Masukkan ID berupa angka.\n")
                    tampilan.pause(2, "Kembali ke menu sebelumnya...")
                    continue
                
                while True:
                    akses_baru = input("Akses baru (gratis/premium): ").lower()
                    if akses_baru in ["gratis", "premium"]:
                        break
                    print("Input tidak valid. Hanya 'gratis' atau 'premium'.\n")
                    tampilan.pause(2, "Kembali ke menu sebelumnya...")
                
                episodes[idx - 1]["akses"] = akses_baru
                penyimpanan.save_anime()
                print("Status akses diperbarui.\n")
                tampilan.pause(2, "Kembali ke menu sebelumnya...")

            elif menu == "Hapus episode":
                episodes = anime.get("episodes", [])
                if not episodes:
                    print("Anime ini belum memiliki episode.\n")
                    tampilan.pause(2, "Kembali ke menu sebelumnya...")
                    continue

                print("\nDaftar Episode:")
                for i, ep in enumerate(episodes, start=1):
                    print(f"{i}. {ep.get('judul')} ({ep.get('akses')})")

                try:
                    idx = int(input("Pilih nomor episode yang ingin dihapus (0 untuk batal): "))
                    if idx == 0:
                        continue
                    if 1 <= idx <= len(episodes):
                        konfirmasi = inquirer.confirm(
                            message=f"Yakin ingin menghapus episode '{episodes[idx-1].get('judul')}'?"
                        ).execute()
                        if konfirmasi:
                            dihapus = episodes.pop(idx - 1)
                            penyimpanan.save_anime()
                            print(f"Episode '{dihapus.get('judul')}' berhasil dihapus.")
                        else:
                            print("Penghapusan episode dibatalkan.")
                        tampilan.pause(2)
                    else:
                        print("Nomor episode tidak valid.")
                        tampilan.pause(2)
                except ValueError:
                    print("Input tidak valid.")
                    tampilan.pause(2)
            
            elif menu == "Batal":
                break
            
            if menu != "Batal" and not mau_lagi():
                break

        except KeyboardInterrupt:
            print("\nOperasi dibatalkan oleh pengguna.\n")
            tampilan.pause(2)
            return
        except Exception as e:
            print(f"❌ Kesalahan saat update anime: {e}\n")
            tampilan.pause(3, "Kembali ke menu utama...")
            return

def hapus_anime():
    while True:
        try:
            tampilan.clear()
            anime_id = tampilan.menu_tampil_anime(penyimpanan.data_anime)
            if anime_id is None:
                print("Kembali ke menu sebelumnya...\n")
                input("Tekan Enter untuk melanjutkan...")
                break
            
            anime = next((a for a in penyimpanan.data_anime if a.get("id") == anime_id), None)
            if anime is None:
                print("Anime tidak ditemukan.\n")
                continue
                
            konfirmasi = inquirer.confirm(
                message=f"Yakin ingin menghapus anime '{anime.get('judul')}'?"
            ).execute()
            
            if konfirmasi:
                penyimpanan.data_anime.remove(anime)
                penyimpanan.reindex_anime_ids()
                penyimpanan.save_anime()
                print(f"Anime '{anime.get('judul')}' berhasil dihapus!\n")
            else:
                print("Penghapusan dibatalkan.\n")
            
            input("Tekan Enter untuk melanjutkan...")

            if not mau_lagi():
                break

        except KeyboardInterrupt:
            print("\nOperasi dibatalkan oleh pengguna.\n")
            tampilan.pause(2)
            return
        except Exception as e:
            print(f"❌ Kesalahan saat menghapus anime: {e}\n")
            tampilan.pause(3, "Kembali ke menu utama...")
            return