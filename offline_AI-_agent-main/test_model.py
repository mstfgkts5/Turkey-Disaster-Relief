import asyncio
from foundry_local_sdk import FoundryLocalManager, Configuration

async def main():
    try:
        # 1. Yapılandırmayı oluşturuyoruz
        config = Configuration(app_name="afette-el-ele")
        
        # 2. Yöneticiyi ayağa kaldırıyoruz
        manager = FoundryLocalManager(config)
        
        # 3. Kataloğu alıp modelleri düz liste olarak çekiyoruz
        catalog = manager.catalog
        models = catalog.list_models()
        
        print(f"\n🚀 BAŞARILI! Microsoft Foundry Local canavar gibi çalışıyor.")
        print(f"Kullanılabilir yerel model sayısı: {len(models)}\n")
        print("İnternetsiz (Offline) çalıştırabileceğimiz modeller:")
        
        if not models:
            print(" 🤔 Şu an indirilmiş yerel model bulunamadı ama bağlantı başarılı!")
        else:
            for model in models:
                print(f" 📦 Model ID: {model.id}")
                
    except Exception as e:
        print(f"\n❌ Beklenmeyen bir hata oluştu: {e}")

if __name__ == "__main__":
    asyncio.run(main())