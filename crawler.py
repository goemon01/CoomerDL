import re
import urllib.parse


def normalize_url(url: str) -> str:
  """URL'den query parametrelerini atar ve başındaki img3, img8 gibi

  değişken subdomain öneklerini normalize eder.
  """
  parsed = urllib.parse.urlparse(url)

  # Domain başındaki imgX. kısmını temizle (örn: img8.coomerfans.com -> coomerfans.com)
  netloc = re.sub(r"^img\d+\.", "", parsed.netloc)

  return f"{parsed.scheme}://{netloc}{parsed.path}"


def load_list(path):
  try:
    with open(path, "r", encoding="utf-8") as f:
      return [line.strip() for line in f if line.strip() and "storager" not in line]
  except FileNotFoundError:
    print(f"Uyarı: '{path}' dosyası bulunamadı.")
    return []


def main():
  # Ham listeler
  crawl1_raw = load_list("crawl1.txt")
  crawl2_raw = load_list("crawl2.txt")

  if not crawl1_raw:
    print("crawl1.txt boş veya okunamadı, işlem iptal edildi.")
    return

  # Normalize edilmiş setler (subdomain ve query parametrelerinden arındırılmış)
  crawl1_norm = {normalize_url(u) for u in crawl1_raw}
  crawl2_norm = {normalize_url(u) for u in crawl2_raw}

  # Eksik olan normalize edilmiş linkler
  diff_norm = crawl1_norm - crawl2_norm

  # Ham linklerden normalize karşılığı diff'te olanları seç
  missing_raw = [u for u in crawl1_raw if normalize_url(u) in diff_norm]

  print(f"{len(missing_raw)} dosya crawl2'de eksik.")
  with open("missing.txt", "w", encoding="utf-8", newline="") as f:
    for item in missing_raw:
      f.write(item + "\n")


if __name__ == "__main__":
  main()