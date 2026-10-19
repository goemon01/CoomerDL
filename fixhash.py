# fix_hashes.py

import re
import urllib.parse

def extract_base(url):
    """
    URL'den sadece path kısmını alır (domain'i yok sayar).
    """
    parsed = urllib.parse.urlparse(url)
    return parsed.path

def extract_params(url):
    """
    URL içindeki e= ve hash= parametrelerini çıkarır.
    """
    match = re.search(r"\?e=([^&]+)&hash=(.+)", url)
    if match:
        return match.group(1), match.group(2)
    return None, None

def main():
    expired_file = "expired.txt"
    new_file = "new.txt"
    output_file = "expired_fixed.txt"

    # Yeni linkleri base → full link şeklinde map’le
    new_links_map = {}

    with open(new_file, "r", encoding="utf-8") as f:
        for line in f:
            url = line.strip()
            if not url:
                continue
            base = extract_base(url)
            new_links_map[base] = url

    # Eski linkleri güncelle
    updated_lines = []

    with open(expired_file, "r", encoding="utf-8") as f:
        for line in f:
            old_url = line.strip()
            if not old_url:
                continue

            base = extract_base(old_url)

            if base in new_links_map:
                # Yeni link bulundu → parametreleri al
                new_url = new_links_map[base]
                new_e, new_hash = extract_params(new_url)

                parsed_new = urllib.parse.urlparse(new_url)
                # Yeni domain + path + yeni parametreler
                fixed_url = f"{parsed_new.scheme}://{parsed_new.netloc}{parsed_new.path}?e={new_e}&hash={new_hash}"
                updated_lines.append(fixed_url)
            else:
                # Yeni link yok → olduğu gibi bırak
                updated_lines.append(old_url)

    # Sonucu yaz
    with open(output_file, "w", encoding="utf-8") as f:
        for line in updated_lines:
            f.write(line + "\n")

    print("Tamamlandı! Güncellenmiş dosya:", output_file)


if __name__ == "__main__":
    main()
