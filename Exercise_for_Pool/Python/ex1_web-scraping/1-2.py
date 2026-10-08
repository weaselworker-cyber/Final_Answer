from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import pandas as pd


# Selenium設定
options = webdriver.ChromeOptions()
options.add_argument(
    "user-agent=Mozilla/5.0"
)

driver = webdriver.Chrome(options=options)


# 最初のページ
url = "https://r.gnavi.co.jp/area/jp/sushi/rs/"

all_data = []

# 店舗ページURL一覧
shop_urls = []

driver.get(url)

time.sleep(3)


# 店舗ページURLを取得
while len(shop_urls) < 50:

    links = driver.find_elements(By.TAG_NAME, "a")

    for link in links:

        href = link.get_attribute("href")

        if href and href.startswith("https://r.gnavi.co.jp/"):
            if "/area/" not in href and "/plan/" not in href and "/special-feature/" not in href:
                if href not in shop_urls:
                    shop_urls.append(href)
                if len(shop_urls) >= 50:
                    break
    if len(shop_urls) >= 50:
        break

    # 次のページへ
    try:
        next_button = driver.find_element(
            By.XPATH,
            "//img[@alt='次（2）ページを表示']/.."
            )
        time.sleep(3)
        next_button.click()
        time.sleep(3)
    except:
        print("次のページが見つかりません。")
        break


print("取得予定店舗数：", len(shop_urls))
print(shop_urls)


# スクレイピング
for a_url in shop_urls:

    print("取得する店舗URL：")
    print(a_url)

    time.sleep(3)

    driver.get(a_url)

    time.sleep(3)

    page_source = driver.page_source

    # 店舗情報
    # 店舗名
    try:
        shop_name_tag = driver.find_element(
            By.CLASS_NAME,
            "shop-info__name"
            )
        shop_name = shop_name_tag.text.strip()
    except:
        shop_name = ""


    # 電話番号
    try:

        phone_tag = driver.find_element(
            By.CLASS_NAME,
            "number"
        )

        phone = phone_tag.text.strip()

    except:

        phone = ""


    # メールアドレス
    emails = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        page_source
    )

    if emails:

        email = emails[0]

    else:

        email = ""


    # 住所
    try:

        address_tag = driver.find_element(
            By.CLASS_NAME,
            "region"
        )

        address = address_tag.text.strip()

    except:

        address = ""


    # 建物名
    try:

        building_tag = driver.find_element(
            By.CLASS_NAME,
            "locality"
        )

        building = building_tag.text.strip()

    except:

        building = ""


    # 公式URL
    try:

        official_link_tag = driver.find_element(
            By.CLASS_NAME,
            "sv-of"
        )

        official_link = official_link_tag.get_attribute("href")

    except:

        official_link = ""


    # SSL
    ssl = official_link.startswith("https://")


    # 住所の分割
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


    # 店舗情報データ
    data = {

        "店舗名": shop_name,
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


# CSV化
df = pd.DataFrame(all_data)

df.to_csv(
    "1-2.csv",
    index=False,
    encoding="utf-8-sig"
)


# ブラウザ終了
driver.quit()