import requests
from datetime import datetime, timezone


def format_unix_timestamp(ts):
    return datetime.fromtimestamp(ts, timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')


def rank_tier_to_string(rank_tier):
    if not rank_tier or rank_tier == 0:
        return "Нет ранга"

    rank_names = {
        1: "Herald",
        2: "Guardian",
        3: "Crusader",
        4: "Archon",
        5: "Legend",
        6: "Ancient",
        7: "Divine",
        8: "Immortal"
    }

    rank = rank_tier // 10
    stars = rank_tier % 10

    rank_name = rank_names.get(rank, "Неизвестно")
    if rank == 8:  # Immortal обычно без звездочек
        return f"{rank_name}"

    return f"{rank_name} {stars}"

def get_dota_stats(steam32_id: int):
    url = f"https://api.opendota.com/api/players/{steam32_id}"
    r = requests.get(url)
    if r.status_code != 200:
        print(f"Ошибка: {r.status_code}")
        return None
    return r.json()


steam32_id = int(897595581)
data = get_dota_stats(steam32_id)

if data:
    profile = data.get("profile", {})
    print(f"Имя: {profile.get('personaname', 'Неизвестно')}")
    print(f"Ранг (rank_tier): {rank_tier_to_string(data.get('rank_tier', 'N/A'))}")
else:
    print("Не удалось получить данные.")

def get_recent_matches(account_id: int, limit: int = 10):
    url = f"https://api.opendota.com/api/players/{account_id}/matches?limit={limit}"

    r = requests.get(url)
    if r.status_code != 200:
        print("Ошибка:", r.status_code)
        return []
    return r.json()

def get_match_details(match_id: int):
    url = f"https://api.opendota.com/api/matches/{match_id}"
    r = requests.get(url)
    if r.status_code != 200:
        print(f"Ошибка загрузки матча {match_id}: {r.status_code}")
        return None
    return r.json()

def summarize_matches(matches):
    total_kills = total_deaths = total_assists = 0
    total_gpm = total_xpm = wins = 0
    count = 0

    for match in matches:
        match_data = get_match_details(match["match_id"])
        if not match_data:
            continue

        player_stats = None
        for player in match_data["players"]:
            if player.get("account_id") == account_id:
                player_stats = player
                break

        if not player_stats:
            continue

        total_kills += player_stats.get("kills", 0)
        total_deaths += player_stats.get("deaths", 0)
        total_assists += player_stats.get("assists", 0)
        total_gpm += player_stats.get("gold_per_min", 0)
        total_xpm += player_stats.get("xp_per_min", 0)

        player_slot = player_stats.get("player_slot", 0)
        radiant_win = match_data.get("radiant_win", False)

        is_radiant = player_slot < 128
        won = (is_radiant and radiant_win) or (not is_radiant and not radiant_win)
        wins += int(won)
        count += 1

    if count == 0:
        print("Нет данных для анализа.")
        return

    print(f"📊 Средняя KDA: {total_kills // count}/{total_deaths // count}/{total_assists // count}")
    print(f"💰 Средний GPM: {total_gpm // count}")
    print(f"⚡ Средний XPM: {total_xpm // count}")
    print(f"🏆 Винрейт: {round(wins / count * 100, 1)}%")


# Использование:
account_id = 897595581
matches = get_recent_matches(account_id)
summarize_matches(matches)

print(f"Получено матчей: {len(matches)}")

def get_heroes():
    url = "https://api.opendota.com/api/heroes"
    r = requests.get(url)
    if r.status_code != 200:
        return {}
    heroes = r.json()
    return {hero['id']: hero['localized_name'] for hero in heroes}

# Получаем последние матчи
def get_recent_matches(account_id, limit=5):
    fields = "hero_id,kills,deaths,assists,player_slot,radiant_win,lane_role,start_time"
    url = f"https://api.opendota.com/api/players/{account_id}/matches?limit={limit}&project={fields}"
    r = requests.get(url)
    if r.status_code != 200:
        return []
    return r.json()

def lane_role_to_str(role):
    roles = {
        1: "Safe Lane",
        2: "Mid Lane",
        3: "Offlane",
        4: "Jungle",
        5: "Unknown"
    }
    return roles.get(role, "-")


def get_match_details(match_id):
    url = f"https://api.opendota.com/api/matches/{match_id}"
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def get_player_stats_in_match(match_data, account_id):
    for player in match_data.get("players", []):
        if player.get("account_id") == account_id:
            return player
    return None

# Использование
account_id = 897595581
heroes = get_heroes()
matches = get_recent_matches(account_id)

for match in matches:
    match_id = match["match_id"]
    match_data = get_match_details(match_id)
    if not match_data:
        continue

    player_stats = get_player_stats_in_match(match_data, account_id)
    if not player_stats:
        continue

    hero_name = heroes.get(player_stats.get("hero_id"), "Unknown Hero")
    lane = lane_role_to_str(player_stats.get("lane_role"))
    k = player_stats.get("kills", 0)
    deaths = player_stats.get("deaths", 1)
    a = player_stats.get("assists", 0)
    player_slot = player_stats.get("player_slot", 0)
    radiant_win = match_data.get("radiant_win", False)
    start_time = match_data.get("start_time", 0)
    date_str = format_unix_timestamp(start_time) if start_time else "Unknown time"

    is_radiant = player_slot < 128
    won = (is_radiant and radiant_win) or (not is_radiant and not radiant_win)
    result = "W" if won else "L"
    performance = round((k + a) / deaths, 2)

    print(f"{hero_name} - {lane} - {result} - {k}\\{deaths}\\{a} - {performance} - {date_str}")
