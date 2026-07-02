import sqlite3

conn = sqlite3.connect("afet_bilgi.db")
cursor = conn.cursor()

# Veritabanındaki ilk 3 satırı çekip ekrana basalım
cursor.execute("SELECT id, dosya_adi, metin_parcasi FROM kaynak_dokumanlar LIMIT 3")
satirlar = cursor.fetchall()

print("--- VERİTABANI İÇERİK TESTİ ---")
if not satirlar:
    print("⚠️ Veritabanı boş! 'data' klasörüne döküman atıp database_prep.py'ı tekrar çalıştırın.")
else:
    for satir in satirlar:
        print(f"\nID: {satir[0]} | Kaynak Dosya: {satir[1]}")
        print(f"Metin Özeti: {satir[2][:150]}...") # İlk 150 karakteri gösterir
print("\n-------------------------------")

conn.close()