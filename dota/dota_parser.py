import requests
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

url = "https://api.stratz.com/api/v1/heroStats"
headers = {
    "Authorization": "Bearer DOTA_TOKEN"
}

response = requests.get(url, headers=headers)
data = response.json()


def click_when_clickable(by, value, timeout=10):
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )
    element.click()

click_when_clickable(By.XPATH, '/html/body/main/div[4]/div[1]/div[1]/div/div[4]')

hero_blocks = driver.find_elements(By.CSS_SELECTOR, "a.oNzMU")
heroes = []

for block in hero_blocks:
    try:
        name = block.find_element(By.TAG_NAME, "img").get_attribute("alt")
        winrate = block.find_element(By.CLASS_NAME, "iBBJnD").text.strip()
        heroes.append((name, float(winrate)))
    except Exception:
        continue

heroes.sort(key=lambda x: x[1], reverse=True)

for name, rate in heroes:
    print(f"{name}: {rate}%")

