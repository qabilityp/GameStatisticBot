import requests

def get_mplus_stats(region, realm, name):
    url = f"https://raider.io/api/v1/characters/profile"
    params = {
        "region": region,
        "realm": realm,
        "name": name,
        "fields": "mythic_plus_best_runs,mythic_plus_scores_by_season:current"
    }
    r = requests.get(url, params=params)

    if r.status_code != 200:
        print(f"Ошибка: {r.status_code}")
        return None

    return r.json()

data = get_mplus_stats("eu", "Blackhand", "jdotb")
