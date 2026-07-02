import os
import sqlite3
from pypdf import PdfReader

# 1. SQLite Veritabanı Bağlantısı (Yoksa otomatik oluşturur)
DB_NAME = "afet_bilgi.db"
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Tabloyu oluşturalım (Metinleri ve hangi dosyadan geldiklerini tutacak)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS kaynak_dokumanlar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dosya_adi TEXT,
        metin_parcasi TEXT
    )
''')
conn.commit()

def metni_parcalara_bol(metin, kelime_siniri=300):
    """Metni yaklaşık 300 kelimelik parçalara böler."""
    kelimeler = metin.split()
    parcalar = []
    for i in range(0, len(kelimeler), kelime_siniri):
        parca = " ".join(kelimeler[i:i+kelime_siniri])
        parcalar.append(parca)
    return parcalar

def verileri_isle():
    data_klasoru = "data"
    if not os.path.exists(data_klasoru):
        print("Lütfen önce 'data' adında bir klasör oluşturun!")
        return

    for dosya in os.listdir(data_klasoru):
        dosya_yolu = os.path.join(data_klasoru, dosya)
        tam_metin = ""
        
        # TXT Dosyalarını Oku
        if dosya.endswith(".txt"):
            with open(dosya_yolu, "r", encoding="utf-8") as f:
                tam_metin = f.read()
        
        # PDF Dosyalarını Oku
        elif dosya.endswith(".pdf"):
            reader = PdfReader(dosya_yolu)
            for page in reader.pages:
                tam_metin += page.extract_text() + "\n"
        
        if tam_metin:
            parcalar = metni_parcalara_bol(tam_metin)
            for parca in parcalar:
                cursor.execute(
                    "INSERT INTO kaynak_dokumanlar (dosya_adi, metin_parcasi) VALUES (?, ?)",
                    (dosya, parca)
                )
            conn.commit()
            print(f"✅ {dosya} başarıyla işlendi ve {len(parcalar)} parçaya bölünerek veritabanına kaydedildi.")

if __name__ == "__main__":
    verileri_isle()
    conn.close()
    print(f"\n🚀 Tüm dökümanlar başarıyla '{DB_NAME}' veritabanına işlendi!")