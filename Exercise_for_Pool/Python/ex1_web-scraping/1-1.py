import requests
import time
from bs4 import BeautifulSoup
import re
import pandas as pd

url_lists = ["https://r.gnavi.co.jp/area/jp/sushi/rs/","https://r.gnavi.co.jp/area/jp/sushi/rs/?sort=HIGH&p=2"]

time.sleep(3)

headers = {"User-Agent": "Mozilla/5.0"}
all_data = []

#店舗ページURL一覧
shop_urls = []

for url_list in url_lists:
    time.sleep(3)
    response = requests.get(url_list, headers=headers)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a", href=True)

    for link in links:
        href = link.get("href")
        if href.startswith("https://r.gnavi.co.jp/"):
            if "/plan/" not in href and "/special-feature/" not in href:
                if href not in shop_urls:
                    shop_urls.append(href)
                if len(shop_urls) >= 50:
                    break
    if len(shop_urls) >= 50:
        break
print("取得予定店舗数：", len(shop_urls))
print(shop_urls)

#スクレイピング
for a_url in shop_urls:
    print("取得する店舗URL：")
    print(a_url)
    time.sleep(3)
    response = requests.get(a_url, headers=headers)    
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    #店舗情報
    #店舗名
    shop_name_tag = soup.find("h1",class_="shop-info__name")
    if shop_name_tag:
        shop_name = shop_name_tag.find("a").text.strip()
    else:
        shop_name = ""
    #電話番号
    phone_tag = soup.find("span", class_="number")
    if phone_tag:
        phone =phone_tag.text.strip()
    else:
        phone = ""
    #メールアドレス
    emails = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        response.text
        )
    if emails:
        email = emails[0]
    else:
        email = ""
    #住所
    address_tag = soup.find("span", class_="region")
    if address_tag:
        address = address_tag.text.strip()
    else:
        address = ""
    #建物名
    building_tag = soup.find("span", class_="locality")
    if building_tag:
        building = building_tag.text.strip()
    else:
        building = ""
    #公式URL
    official_link_tag = soup.find("a", class_="sv-of")
    if official_link_tag:
        official_link = official_link_tag.get("href")
    else:
        official_link = ""
    #SSL
    ssl = official_link.startswith("https://")
    #住所の分割
    match = re.match(
        r"^(東京都|北海道|(?:大阪|京都)府|.{2,3}県)(.*?(?:市[^区]*区|市|区|町|村))(.*)$",
        address
        )
    if match:
        prefecture = match.group(1)
        city = match.group(2)
        street = match.group(3)
    else:
        prefecture = ""
        city = ""
        street = ""
    
    #店舗情報データ
    data = {
        "店舗名":shop_name,
        "電話番号": phone,
        "メールアドレス": email,
        "都道府県": prefecture,
        "市区町村": city,
        "番地": street,
        "建物名": building,
        "URL": official_link,
        "SSL": ssl
        }
    print(data)
    all_data.append(data)

print(all_data)


#CSV化
df = pd.DataFrame(all_data)
df.to_csv("1-1.csv", index=False, encoding="utf-8-sig")