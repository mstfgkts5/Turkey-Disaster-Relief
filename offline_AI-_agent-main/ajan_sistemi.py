import sqlite3
import requests  # Ollama ile konuşabilmek için

# 1. ADIM: Senin hazırladığın veritabanı arama fonksiyonu
def afet_veritabaninda_ara(soru_kelimesi):
    conn = sqlite3.connect('afet_bilgi.db')
    cursor = conn.cursor()
    
    # 'icerik' hatası düzeltildi, senin veritabanındaki gerçek sütun adı 'metin_parcasi' yazıldı
    cursor.execute("SELECT metin_parcasi FROM kaynak_dokumanlar WHERE metin_parcasi LIKE ?", (f'%{soru_kelimesi}%',))
    sonuclar = cursor.fetchall()
    conn.close()
    
    if sonuclar:
        # Bulunan tüm döküman metinlerini birleştiriyoruz
        return "\n".join([satir[0] for satir in sonuclar])
    return "Veritabanında bu konuyla ilgili spesifik bir döküman bulunamadı."

# 2. ADIM: Ollama'ya veritabanı bilgisiyle birlikte soru gönderme fonksiyonu
def yapay_zekaya_sor(kullanici_sorusu, arama_anahtari):
    # Önce senin veritabanından ilgili yazıları çekiyoruz
    veritabanindan_gelen_bilgi = afet_veritabaninda_ara(arama_anahtari)
    
    # YAPAY ZEKAYI SINIRLANDIRDIĞIMIZ ŞABLON (Prompt)
    sistem_talimati = f"""
    Sen Türkiye Afette Elele projesinin resmi yapay zeka asistanısın. 
    Sadece sana aşağıda verilen 'GÜVENİLİR BİLGİ' kısmına dayanarak cevap vereceksin.
    Eğer bilgi içeride yoksa, kendi kafandan bilgi uydurma.
    KESİNLİKLE SADECE TÜRKÇE CEVAP VER.

    GÜVENİLİR BİLGİ:
    {veritabanindan_gelen_bilgi}
    """
    
    # Ollama'nın bilgisayarındaki yerel adresi (API Endpoint)
    ollama_url = "http://localhost:11434/api/chat"
    
    # Ollama'ya göndereceğimiz paket
    veri_paketi = {
        "model": "llama3:8b",  # Bilgisayarına indirdiğin modelin adı
        "messages": [
            {"role": "system", "content": sistem_talimati},
            {"role": "user", "content": kullanici_sorusu}
        ],
        "stream": False  # Cevabı parça parça değil, tek seferde bütün almak için
    }
    
    # İstek atıyoruz
    response = requests.post(ollama_url, json=veri_paketi)
    
    if response.status_code == 200:
        return response.json()['message']['content']
    else:
        return f"Ollama bağlantı hatası: {response.status_code}"

# 🚀 TEST EDİYORUZ
if __name__ == "__main__":
    # Veritabanında olan "ilk yardım" kelimesini aratıyoruz
    anahtar = "ilk yardım" 
    soru = "Afet anında ilk yardım yaparken nelere dikkat etmeliyiz?"
    
    print("Veritabanı aranıyor ve Ollama tetikleniyor...\n")
    cevap = yapay_zekaya_sor(soru, anahtar)
    print("--- YAPAY ZEKANIN CEVABI ---")
    print(cevap)