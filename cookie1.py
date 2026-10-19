import time
from playwright.sync_api import sync_playwright

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like"
    " Gecko) Chrome/122.0.0.0 Safari/537.36"
)
OUTPUT_FILE = r"C:\Users\Administrator\Desktop\Packet\CoomerDL-main\CoomerDL-latest\downloader\adapters\headers.txt"


def get_coomerfans_cookies():
    target_url = "https://coomerfans.com/"
    print(f"[{target_url}] adresine bağlanılıyor...")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized",
            ],
        )

        context = browser.new_context(
            user_agent=USER_AGENT,
            viewport=None,
        )

        page = context.new_page()

        page.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () =>"
            " undefined})"
        )

        page.goto(target_url, wait_until="domcontentloaded")
        print(
            "Sayfa açıldı. 'bg_clearance' çerezi bekleniyor (Ekranda doğrulama"
            " kutusu çıkarsa tıklayın)..."
        )

        cookies = []
        for i in range(30):
            cookies = context.cookies()
            cookie_names = [c["name"] for c in cookies]

            if "bg_clearance" in cookie_names:
                print("\n[BAŞARILI] 'bg_clearance' çerezi yakalandı!")
                break

            time.sleep(1)

        browser.close()

        cookie_header = "; ".join(
            [f"{c['name']}={c['value']}" for c in cookies]
        )
        return cookie_header


if __name__ == "__main__":
    try:
        cookie_result = get_coomerfans_cookies()

        print("\n" + "=" * 60)
        print("ÇEKİLEN COOKIE HEADER:")
        print("=" * 60)
        print(cookie_result)
        print("=" * 60 + "\n")

        # Doğrudan mevcut dosyaya yazar
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(f"User-Agent: {USER_AGENT}\n")
            f.write(f"Cookie: {cookie_result}\n")

        print(f"[BAŞARILI] Bilgiler kaydedildi: {OUTPUT_FILE}")

    except Exception as e:
        print(f"\n[HATA] Bir sorun oluştu: {e}")