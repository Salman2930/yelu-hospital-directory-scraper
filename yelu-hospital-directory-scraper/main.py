from selenium import webdriver
from bs4 import BeautifulSoup as DS
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from datetime import datetime
import requests
import time
import re
import pandas as pd
from urllib.parse import urljoin
from selenium.webdriver.chrome.options import Options
options = Options()
options.page_load_strategy = "none"
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")
options.add_argument("--disable-notifications")
options.add_argument("--blink-settings=imagesEnabled=false")

service = Service(path)
driver = webdriver.Chrome(service=service, options=options)
driver.set_page_load_timeout(15)

driver.get("https://www.yelu.in/category/hospitals")
time.sleep(2)

try:
    driver.execute_script("window.stop();")
except:
    pass

soup = DS(driver.page_source, "html.parser")
all_profile_urls = []

for page in range(1, 151):

    if page == 1:
        page_url = "https://www.yelu.in/category/hospitals"
    else:
        page_url = f"https://www.yelu.in/category/hospitals/{page}"

    try:
        driver.get(page_url)
        time.sleep(2)
        driver.execute_script("window.stop();")
    except Exception as e:
        print("Listing page load issue:", page_url, e)
        continue

    soup = DS(driver.page_source, "html.parser")
    cards = soup.select("div.company")

    print("Page:", page, "Cards:", len(cards))

    for card in cards:
        h3 = card.find("h3")
        if not h3:
            continue

        a_tag = h3.find("a")
        if not a_tag:
            continue

        name = a_tag.get_text(strip=True)
        profile_url = urljoin(base_url, a_tag.get("href"))

        all_profile_urls.append({
            "name_from_listing": name,
            "profile_url": profile_url
        })


df_profiles = pd.DataFrame(all_profile_urls)
df_profiles = df_profiles.drop_duplicates(subset=["profile_url"])

print("Total profile URLs:", df_profiles.shape)


all_profile_data = []

for index, row in df_profiles.iterrows():
    profile_url = row["profile_url"]

    try:
        driver.get(profile_url)
        time.sleep(2)
        driver.execute_script("window.stop();")

        profile_soup = DS(driver.page_source, "html.parser")
        info_blocks = profile_soup.find_all("div", class_="info")

        profile_data = {
            "profile_url": profile_url
        }

        for block in info_blocks:
            label = block.find("div", class_="label")
            text = block.find("div", class_="text")

            if label and text:
                key = label.get_text(strip=True)

                if key in ["Company description", "Location map", "Working hours", "Listed in categories"]:
                    continue

                value = text.get_text(" ", strip=True)
                profile_data[key] = value

        title = profile_soup.title.get_text(strip=True) if profile_soup.title else None

        if "Hospital name" not in profile_data:
            if title:
                profile_data["Hospital name"] = title.split(" - ")[0]
            else:
                profile_data["Hospital name"] = row.get("name_from_listing")

        all_profile_data.append(profile_data)
        print(index + 1, "done:", profile_url)

    except Exception as e:
        print("Profile page issue:", index + 1, profile_url, e)
        continue

    if (index + 1) % 100 == 0:
        pd.DataFrame(all_profile_data).to_csv(
            "yelu_hospitals_backup.csv",
            index=False,
            encoding="utf-8-sig"
        )

        try:
            driver.quit()
        except:
            pass

        service = Service(path)
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(15)

        print("Backup saved and driver restarted:", index + 1)


df_final = pd.DataFrame(all_profile_data)

df_final.to_csv(
    "yelu_hospitals_final.csv",
    index=False,
    encoding="utf-8-sig"
)

print(df_final.shape)
print(df_final.head())