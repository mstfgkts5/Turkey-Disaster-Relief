import asyncio
import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import AsyncOpenAI

app = FastAPI()

# React arayüzünün bağlanabilmesi için izinleri (CORS) ayarlıyoruz
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Geliştirme aşamasında tüm bağlantılara izin veriyoruz
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SoruIstegi(BaseModel):
    soru: str

@app.post("/soru-sor")
async def yapay_zeka_cevapla(istek: SoruIstegi):
    kullanici_sorusu = istek.soru
    satirlar = []
    
    try:
        conn = sqlite3.connect("afet_bilgi.db")
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM documents WHERE content LIKE ?", (f"%{kullanici_sorusu}%",))
        satirlar = cursor.fetchall()
        conn.close()
    except Exception:
        pass

    if not satirlar:
        referans_metin = "İlk yardım kılavuzu: Kanamalarda temiz bezle tampon yapın. Sakin olun ve baskı uygulayın."
    else:
        referans_metin = "\n".join([satir[0] for satir in satirlar[:2]])

    sistem_talimati = f"""
    Sen bir yerel afet ilk yardım asistanısın.
    Sadece sana verilen şu REFERANS METNE dayanarak Türkçe cevap ver.
    
    REFERANS METİN:
    {referans_metin}
    """
    
    try:
        client = AsyncOpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
        response = await client.chat.completions.create(
            model="llama3:8b", 
            messages=[
                {"role": "system", "content": sistem_talimati},
                {"role": "user", "content": kullanici_sorusu}
            ]
        )
        return {"cevap": response.choices[0].message.content}
    except Exception as e:
        return {"cevap": f"Yapay zeka motoru hatası: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)