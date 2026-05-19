import requests
from colorama import Fore, Style, init
from .item_list import ITEMS

base_url = "https://europe.albion-online-data.com/api/v2/stats/prices/"
params = "?locations=Caerleon,FortSterling&qualities=1,2,3,4,5"

full_url = base_url + ITEMS + params

response = requests.get(full_url)


def get_item_price():
    response = requests.get(full_url)
    if response.status_code == 200:
        item_price = response.json()
        return item_price
    else:
        print('error', response.status_code)
        return []


def translate(item_id, quality):
    quality_dict = {
        1: "Normal",
        2: "Good",
        3: "Outstanding",
        4: "Excellent",
        5: "Masterpiece"
    }

    enchantment = "0"

    if "@" in item_id:
        base, _, ench = item_id.partition("@")
        enchantment = ench
    else:
        base = item_id

    tier, _, item_type = base.partition("_")  # T7, BAG

    translated_name = f"{tier}.{enchantment} {item_type.lower()}, {quality_dict.get(quality, 'Unknown')}"

    return translated_name


def percent_of_items():
    data = get_item_price()
    result = []
    items_by_id = {}

    for item in data:
        item_id = item.get("item_id")
        city = item.get("city")
        sell_price_min = item.get("sell_price_min")
        sell_price_max = item.get("sell_price_max")
        quality = item.get("quality")
        average_price = (sell_price_min + sell_price_max) / 2

        if item_id not in items_by_id:
            items_by_id[item_id] = {}

        if quality not in items_by_id[item_id]:
            items_by_id[item_id][quality] = {}

        items_by_id[item_id][quality][city] = average_price

    for item_id, qualities in items_by_id.items():
        for quality, cities in qualities.items():
            if "Caerleon" in cities and "Fort Sterling" in cities:
                price1 = cities["Caerleon"]
                price2 = cities["Fort Sterling"]

                if price1 > 0 and price2 > 0:
                    percent = abs((price1 - price2) / price2) * 100

                    if percent >= 40:
                        translated_name = translate(item_id, quality)
                        if price1 > price2:
                            source = "Fort Sterling"
                            target = "Caerleon"
                        else:
                            source = "Caerleon"
                            target = "Fort Sterling"

                        line = (f"{translated_name}: Есть профит {percent:.2f}% "
                                f"({source} → {target}, {price1:.1f} → {price2:.1f})")
                        result.append(line)

    return result

def print_colored_profit(item_id, quality, percent, price_caerleon, price_fortsterling):
    translated_name = translate(item_id, quality)

    if price_caerleon > price_fortsterling:
        ca_color = Fore.RED
        fs_color = Fore.GREEN
    elif price_caerleon < price_fortsterling:
        ca_color = Fore.GREEN
        fs_color = Fore.RED

    print(f"{translated_name}: Есть профит {percent:.2f}% "
          f"(Caerleon={ca_color}{price_caerleon}{Style.RESET_ALL}, "
          f"Fort Sterling={fs_color}{price_fortsterling}{Style.RESET_ALL})")



if __name__ == "__main__":
    percent_of_items()
    data = get_item_price()

    for item in data:
        filtered_item = {
            "item_id": item.get("item_id"),
            "city": item.get("city"),
            "quality": item.get("quality"),
            "sell_price_min": item.get("sell_price_min"),
            "sell_price_max": item.get("sell_price_max")
        }

