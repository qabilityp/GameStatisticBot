from selenium.common import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get("https://albionfreemarket.com/pricecheck/")

wait = WebDriverWait(driver, 10)

def click_when_clickable(by, value, timeout=10):
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )
    element.click()

click_when_clickable(By.XPATH, '//button[.//span[contains(text(), "Accept All")]]')
click_when_clickable(By.ID, "mat-select-1")
click_when_clickable(By.XPATH, '//mat-option//span[normalize-space(text())="All"]')
click_when_clickable(By.ID, "mat-select-4")
click_when_clickable(By.XPATH, '//mat-option//span[normalize-space(text())="4"]')

click_when_clickable(By.XPATH, '//button[@aria-label="Options Menu"]')
click_when_clickable(By.XPATH, '//span[contains(text(), "Server:")]')
click_when_clickable(By.XPATH, '//button[.//span[text()="Europe"]]')
click_when_clickable(By.XPATH, '//button[@aria-label="Options Menu"]')
click_when_clickable(By.XPATH, '//span[contains(text(), "English")]')
click_when_clickable(By.XPATH, '//button[.//span[text()="Русский"]]')
click_when_clickable(By.XPATH, '//div[contains(text(), "Black Market")]')
click_when_clickable(By.XPATH, '//div[contains(text(), "Brecilien")]')
click_when_clickable(By.XPATH, '//div[contains(text(), "Bridgewatch")]')
click_when_clickable(By.XPATH, '//div[contains(text(), "Lymhurst")]')
click_when_clickable(By.XPATH, '//div[contains(text(), "Martlock")]')
click_when_clickable(By.XPATH, '//div[contains(text(), "Thetford")]')


#Ближний бой: Топоры, Кинжалы, Молоты

class MeleeCategory():
    def __init__(self):
        click_when_clickable(By.ID, "mat-select-2")
        click_when_clickable(By.XPATH, '//mat-option//span[normalize-space(text())="Ближний бой"]')
        self.category = "Ближний бой"

##################################################################################################

class AxesSubcategory(MeleeCategory):
    def __init__(self):
        super().__init__()
        click_when_clickable(By.ID, "mat-select-3")
        click_when_clickable(By.XPATH, '//mat-option//span[normalize-space(text())="Топоры"]')
        self.subcategory = 'Топоры'

class Daggers(MeleeCategory):
    def __init__(self):
        super().__init__()
        click_when_clickable(By.ID, "mat-select-3")
        click_when_clickable(By.XPATH, '//mat-option//span[normalize-space(text())="Кинжалы"]')
        self.subcategory = "Кинжалы"

class Hammers(MeleeCategory):
    def __init__(self):
        super().__init__()
        click_when_clickable(By.ID, "mat-select-3")
        click_when_clickable(By.XPATH, '//mat-option//span[normalize-space(text())="Молоты"]')
        self.subcategory = "Молоты"

##################################################################################################

class VarietySubcategoryAxes(AxesSubcategory):
    def __init__(self):
        super().__init__()

    def big_axes(self):
        click_when_clickable(By.ID, "mat-select-5")
        click_when_clickable(By.XPATH,'//mat-option//span[starts-with(normalize-space(text()), "Большой топор")]')

    def dest_of_worlds(self):
        click_when_clickable(By.ID, "mat-select-11")
        click_when_clickable(By.XPATH,'//mat-option[.//span[contains(@class, "mat-option") and contains(normalize-space(.), "Разрушитель миров")]]')

    def bear_paws(self):
        click_when_clickable(By.ID, "mat-select-11")
        click_when_clickable(By.XPATH,'//mat-option[.//span[contains(@class, "mat-option") and contains(normalize-space(.), "Медвежьи лапы")]]')

    def halberds(self):
        click_when_clickable(By.ID, "mat-select-11")
        click_when_clickable(By.XPATH,'//mat-option[.//span[contains(@class, "mat-option") and contains(normalize-space(.), "Алебарда")]]')

    def scavenger(self):
        click_when_clickable(By.ID, "mat-select-11")
        click_when_clickable(By.XPATH,'//mat-option[.//span[contains(@class, "mat-option") and contains(normalize-space(.), "Падальщик")]]')

    def crystal_reaper(self):
        click_when_clickable(By.ID, "mat-select-11")
        click_when_clickable(By.XPATH,'//mat-option[.//span[contains(@class, "mat-option") and contains(normalize-space(.), "Хрустальный жнец")]]')


    def hells_scythe(self):
        click_when_clickable(By.ID, "mat-select-11")
        click_when_clickable(By.XPATH,'//mat-option[.//span[contains(@class, "mat-option") and contains(normalize-space(.), "Адская коса")]]')

    def battle_axe(self):
        click_when_clickable(By.ID, "mat-select-11")
        click_when_clickable(By.XPATH,'//mat-option[.//span[contains(@class, "mat-option") and contains(normalize-space(.), "Боевой топор")]]')




def name_items():
    list_items = []
    card_count = len(driver.find_elements(By.XPATH, "//app-item-price-card"))
    for i in range(card_count):
        card = driver.find_elements(By.XPATH, "//app-item-price-card")[i]
        line = card.text.strip()
        name = line.split('\n')[0]
        if name not in list_items:
            list_items.append(name)
    return list_items

variety = VarietySubcategoryAxes()

all_items = {}

variety.big_axes()
time.sleep(1)
all_items["Большой топор"] = name_items()

variety.dest_of_worlds()
time.sleep(1)
all_items["Разрушитель Миров"] = name_items()

variety.bear_paws()
time.sleep(1)
all_items["Медвежьи лапы"] = name_items()

variety.halberds()
time.sleep(1)
all_items["Алебарда"] = name_items()

variety.scavenger()
time.sleep(1)
all_items["Падальщик"] = name_items()

variety.crystal_reaper()
time.sleep(1)
all_items["Хрустальная жнец"] = name_items()

variety.hells_scythe()
time.sleep(1)
all_items["Адская коса"] = name_items()

variety.battle_axe()
time.sleep(1)
all_items["Боевой топор"] = name_items()


print(all_items)
