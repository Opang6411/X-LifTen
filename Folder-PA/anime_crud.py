import storage


def tampilkan_anime():
    for a in storage.data_anime:
        print(f"{a['id']}. {a['judul']} ({a['genre']}) - Rating {a['rating']}")
        for i, ep in enumerate(a.get("episodes", []), start=1):
            print(f"   - Episode {i} - {ep['judul']} ({ep['akses']})")
    print()


def tambah_anime():
    judul = input("Judul anime: ")
    genre = input("Genre: ")
    try:
        rating = float(input("Rating anime: "))
    except ValueError:
        print("Rating tidak valid. Gunakan angka.\n")
        return
    storage.data_anime.append({
        "id": len(storage.data_anime) + 1,
        "judul": judul,
        "genre": genre,
        "rating": rating,
        "episodes": []
    })
    storage.save_anime()
    print(f"✅ Anime '{judul}' berhasil ditambahkan!\n")


def update_anime():
    tampilkan_anime()
    try:
        pilih = int(input("Pilih ID anime yang ingin diperbarui: "))
    except ValueError:
        print("Input tidak valid.\n")
        return
    anime = next((a for a in storage.data_anime if a["id"] == pilih), None)
    if not anime:
        print("Anime tidak ditemukan.\n")
        return
    print(f"🔧 Mengupdate {anime['judul']}")
    print("1. Tambah episode baru")
    print("2. Ubah status akses episode")
    menu = input("Pilih: ")

    if menu == "1":
        judul_ep = input("Judul episode baru: ")
        akses = input("Akses episode (gratis/premium): ").lower()
        anime.setdefault("episodes", []).append({"judul": judul_ep, "akses": akses})
        storage.save_anime()
        print(f"✅ Episode '{judul_ep}' berhasil ditambahkan.\n")

    elif menu == "2":
        for i, ep in enumerate(anime.get("episodes", []), start=1):
            print(f"{i}. {ep['judul']} ({ep['akses']})")
        try:
            idx = int(input("Pilih episode yang ingin diubah: ")) - 1
        except ValueError:
            print("Input tidak valid.\n")
            return
        akses_baru = input("Akses baru (gratis/premium): ").lower()
        anime["episodes"][idx]["akses"] = akses_baru
        storage.save_anime()
        print("✅ Status akses diperbarui.\n")


def hapus_anime():
    tampilkan_anime()
    try:
        pilih = int(input("Masukkan ID anime yang ingin dihapus: "))
    except ValueError:
        print("Input tidak valid.\n")
        return
    anime = next((a for a in storage.data_anime if a["id"] == pilih), None)
    if anime:
        storage.data_anime.remove(anime)
        storage.save_anime()
        print(f"✅ Anime '{anime['judul']}' telah dihapus!\n")
    else:
        print("Anime tidak ditemukan.\n")
