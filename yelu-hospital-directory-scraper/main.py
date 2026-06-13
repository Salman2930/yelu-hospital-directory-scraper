#main source code
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


base_url = "https://www.yelu.in"
final_data = []


url = 'https://www.yelu.in/'

path = r"C:\webdrivers\chromedriver.exe"

service = Service(path)

driver = webdriver.Chrome(service=service)

driver.get(url)

driver.find_element(By.XPATH,'/html/body/section[1]/div/div[2]/a[2]/i').click()

time.sleep(2)
# find search box by ID
search_box = driver.find_element(By.ID, "CompanySearchQuery")

#then clear the text
search_box.clear()
#finally type "hospital"
search_box.send_keys("hospitals")

time.sleep(2)

#click search button
driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/form/a').click()

soup = DS(driver.page_source, "html.parser")
#print(soup)
all_profile_urls = []

for page in range(1, 315):

    if page == 1:
        page_url = "https://www.yelu.in/category/hospitals"
    else:
        page_url = f"https://www.yelu.in/category/hospitals/{page}"

    driver.get(page_url)
    time.sleep(3)

    soup = DS(driver.page_source, "html.parser")
    cards = soup.select("div.company")

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

print(df_profiles.shape)

all_profile_data = []

for index, row in df_profiles.iterrows():
    profile_url = row["profile_url"]
    
    driver.get(profile_url)
    time.sleep(2)
    
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

    # fallback for missing Hospital name
    title = profile_soup.title.get_text(strip=True) if profile_soup.title else None

    if "Hospital name" not in profile_data and title:
        profile_data["Hospital name"] = title.split(" - ")[0]
    
    all_profile_data.append(profile_data)
    print(index + 1, "done:", profile_url)

df_final = pd.DataFrame(all_profile_data)

print(df_final.shape)
print(df_final.head())