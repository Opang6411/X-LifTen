import penyimpanan
import tampilan

def tambah_anime():
    while True:
        print("=== Tambah Anime ===")
        judul = input("Judul anime (0 untuk kembali): ")
        if judul == "0":
            return
        genre = input("Genre: ")
        try:
            rating = float(input("Rating anime: "))
        except ValueError:
            print("Rating tidak valid. Gunakan angka.\n")
            continue
        penyimpanan.data_anime.append({
            "id": len(penyimpanan.data_anime) + 1,
            "judul": judul,
            "genre": genre,
            "rating": rating,
            "episodes": []
        })
        penyimpanan.save_anime()
        print(f"Anime '{judul}' berhasil ditambahkan!\n")
        if not mau_lagi():
            break

def update_anime():
    while True:
        tampilan.clear()
        anime_id = tampilan.menu_tampil_anime(penyimpanan.data_anime)
        if anime_id is None:
            print("Kembali ke menu sebelumnya...\n")
            input("Tekan Enter untuk melanjutkan...")
            break
        anime = next((a for a in penyimpanan.data_anime if a["id"] == anime_id))
        print(f"\nMengupdate {anime['judul']}")
        print("1. Tambah episode baru")
        print("2. Ubah status akses episode")
        menu = input("Pilih: ")
        if menu == "1":
            judul_ep = input("Judul episode baru: ")
            akses = input("Akses episode (gratis/premium): ").lower()
            anime.setdefault("episodes", []).append({
                "judul": judul_ep,
                "akses": akses
            })
            penyimpanan.save_anime()
            print(f"Episode '{judul_ep}' berhasil ditambahkan.\n")
        elif menu == "2":
            episodes = anime.get("episodes", [])
            if not episodes:
                print("Anime ini belum memiliki episode.\n")
                continue
            print("\nDaftar Episode:")
            for i, ep in enumerate(episodes, start=1):
                print(f"{i}. {ep['judul']} ({ep['akses']})")
            try:
                idx = int(input("Pilih episode yang ingin diubah (0 untuk kembali): "))
            except ValueError:
                print("Input tidak valid.\n")
                continue
            if idx == 0:
                continue
            if not (1 <= idx <= len(episodes)):
                print("Episode tidak ditemukan.\n")
                continue
            akses_baru = input("Akses baru (gratis/premium): ").lower()
            episodes[idx - 1]["akses"] = akses_baru
            penyimpanan.save_anime()
            print("Status akses diperbarui.\n")
        else:
            print("Pilihan tidak valid.\n")
        if not mau_lagi():
            break

def hapus_anime():
    while True:
        anime_id = tampilan.menu_tampil_anime(penyimpanan.data_anime)
        if anime_id is None:
            print("Kembali ke menu sebelumnya...\n")
            input("Tekan Enter untuk melanjutkan...")
            break
        anime = next((a for a in penyimpanan.data_anime if a["id"] == anime_id))
        keyakinan = input(f"Yakin ingin menghapus anime '{anime['judul']}'? (y/n): ").lower()
        if keyakinan == "y":
            penyimpanan.data_anime.remove(anime)
            penyimpanan.save_anime()
            print(f"Anime '{anime['judul']}' berhasil dihapus!\n")
        elif keyakinan == "n":
            print("Penghapusan dibatalkan.\n")
            input("Tekan Enter untuk melanjutkan...")
        else:
            print("Input tidak valid. Penghapusan dibatalkan.\n")
            input("Tekan Enter untuk melanjutkan...")
        if not mau_lagi():
            break

def mau_lagi():
    while True:
        lagi = input("Lakukan operasi ini lagi? (y/n): ").lower()
        if lagi == "y":
            return True
        elif lagi == "n":
            print("Kembali...\n")
            input("Tekan Enter untuk melanjutkan...")
            return False
        else:
            print("Input tidak valid. Silakan masukkan 'y' atau 'n'.\n")