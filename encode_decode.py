def char_to_custom_symbol(char, char_to_symbol_dict):
    return char_to_symbol_dict.get(char, char)

def custom_symbol_to_char(symbol, symbol_to_char_dict):
    return symbol_to_char_dict.get(symbol, symbol)

def encode_pesan(pesan_asli_baru, pesan_tersembunyi):
    # Kamus manual untuk konversi angka dan simbol lainnya
    char_to_symbol_dict = {
        '0': '!', '1': '@', '2': '#', '3': '$', '4': '%', 
        '5': '^', '6': '&', '7': '*', '8': '(', '9': ')',
        '.': '_',  'º': 'º'
    }
    
    # Konversi setiap karakter dalam pesan asli menjadi representasi ASCII dan gabungkan menjadi string
    pesan_asli_ascii = ''.join(f'{ord(char):03}' for char in pesan_asli_baru)

    # Sisipkan representasi ASCII ke dalam pesan tersembunyi dengan spasi
    pesan_tersembunyi_modifikasi = ""
    indeks_ascii = 0
    for kata in pesan_tersembunyi.split():
        pesan_tersembunyi_modifikasi += " " + kata
        if indeks_ascii < len(pesan_asli_ascii):
            pesan_tersembunyi_modifikasi += " " + pesan_asli_ascii[indeks_ascii:indeks_ascii+3]
            indeks_ascii += 3

    # Mengonversi setiap karakter dalam pesan tersembunyi menjadi simbol manual
    pesan_encoded = ''.join(char_to_custom_symbol(char, char_to_symbol_dict) for char in pesan_tersembunyi_modifikasi.strip())

    return pesan_encoded

def decode_pesan(pesan_encoded):
    # Kamus manual untuk konversi angka dan simbol 
    char_to_symbol_dict = {
        '0': '!', '1': '@', '2': '#', '3': '$', '4': '%', 
        '5': '^', '6': '&', '7': '*', '8': '(', '9': ')',
        '.': '_', 'º': 'º'
    }
    
    # Kamus terbalik untuk dekode
    symbol_to_char_dict = {v: k for k, v in char_to_symbol_dict.items()}

    # Mengonversi setiap simbol menjadi karakter teks asli
    pesan_tersembunyi_modifikasi = ''.join(custom_symbol_to_char(char, symbol_to_char_dict) for char in pesan_encoded)

    # Memisahkan kata-kata berdasarkan spasi
    words = pesan_tersembunyi_modifikasi.split()

    # Ekstraksi pesan asli dari representasi ASCII
    pesan_asli_ascii = ""
    pesan_tersembunyi_clean = ""

    for word in words:
        if word.isdigit() and len(word) == 3:
            pesan_asli_ascii += word
        else:
            pesan_tersembunyi_clean += word + " "

    # Konversi representasi ASCII kembali ke karakter asli
    pesan_asli = ''.join(chr(int(pesan_asli_ascii[i:i+3])) for i in range(0, len(pesan_asli_ascii), 3))

    return pesan_asli, pesan_tersembunyi_clean.strip(), pesan_tersembunyi_modifikasi


