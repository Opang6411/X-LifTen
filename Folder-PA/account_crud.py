import storage


def tampilkan_akun():
    for i, a in enumerate(storage.akun, start=1):
        print(f"{i}. {a.get('username')} — Role: {a.get('role')}")
    print()


def ubah_role_akun():
    tampilkan_akun()
    try:
        pilih = int(input("Masukkan nomor akun yang ingin diubah role-nya: "))
    except ValueError:
        print("Input tidak valid.\n")
        return
    user = storage.akun[pilih-1]
    role_baru = input("Role baru (admin/user/pro): ").lower()
    user["role"] = role_baru
    storage.save_akun()
    print(f"✅ Role akun '{user.get('username')}' berhasil diubah menjadi {role_baru}.\n")


def hapus_akun():
    tampilkan_akun()
    try:
        pilih = int(input("Masukkan nomor akun yang ingin dihapus: "))
    except ValueError:
        print("Input tidak valid.\n")
        return
    user = storage.akun[pilih-1]
    storage.akun.remove(user)
    storage.save_akun()
    print(f"✅ Akun '{user.get('username')}' telah dihapus!\n")
