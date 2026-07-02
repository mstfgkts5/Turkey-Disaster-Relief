import sqlite3

def afet_veritabaninda_ara(anahtar_kelime):
    """
    Veritabanında kullanıcının sorduğu kelimeye göre arama yapar 
    Hub/Agent mimarisinde 'Tool' olarak kullanılacaktır.
    """
    conn = sqlite3.connect("afet_bilgi.db")
    cursor = conn.cursor()
    
    # SQL LIKE sorgusu ile metin içinde anahtar kelimeyi arıyoruz
    cursor.execute(
        "SELECT metin_parcasi FROM kaynak_dokumanlar WHERE metin_parcasi LIKE ?", 
        ('%' + anahtar_kelime + '%',)
    )
    sonuclar = cursor.fetchall()
    conn.close()
    
    if not sonuclar:
        return f"'{anahtar_kelime}' ile ilgili yerel dökümanlarda bilgi bulunamadı."
    
    # Bulunan ilk 2 anlamlı parçayı birleştirip ajana dönüyoruz
    metin_cikti = ""
    for i, satir in enumerate(sonuclar[:2]):
        metin_cikti += f"[Kaynak Parça {i+1}]: {satir[0]}\n\n"
        
    return metin_cikti

# Fonksiyonu test etmek için (İstersen burayı çalıştırıp deneyebilirsin)
if __name__ == "__main__":
    # Örnek arama: Veritabanına eklediğin bir kelimeyi yazıp dene
    print(afet_veritabaninda_ara("ilk yardım"))