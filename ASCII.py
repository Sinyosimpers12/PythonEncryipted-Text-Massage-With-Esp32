def tampilkan_tabel_ascii():
    # Menampilkan header tabel
    print(f"{'Char':^7} {'ASCII':^7} {'Char':^7} {'ASCII':^7} {'Char':^7} {'ASCII':^7} {'Char':^7} {'ASCII':^7}")

    # Menampilkan isi tabel
    for i in range(32, 128, 4):
        row = ""
        for j in range(4):
            if i + j < 128:
                row += f"{chr(i+j):^7} {i+j:^7} "
        print(row)

# Memanggil fungsi untuk menampilkan tabel ASCII
# Menampilan Table Ascii untuk char , Sedangkan untuk SUHU dibuatkan ASCII CUSTOM ditampiliin pada EncodeDecode.py
tampilkan_tabel_ascii()
