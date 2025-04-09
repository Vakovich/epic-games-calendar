# script.py
import requests
from ics import Calendar, Event

URL = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=ru&country=RU&allowCountries=RU"

def fetch_free_games():
    response = requests.get(URL)
    data = response.json()
    games = []

    for game in data['data']['Catalog']['searchStore']['elements']:
        if game.get('promotions') and game['promotions'].get('promotionalOffers'):
            promo = game['promotions']['promotionalOffers'][0]['promotionalOffers'][0]
            title = game['title']
            start = promo['startDate']
            end = promo['endDate']
            games.append({
                'title': title,
                'start': start,
                'end': end
            })

    return games

def generate_calendar(games):
    calendar = Calendar()
    for game in games:
        e = Event()
        e.name = f"🎮 Бесплатно: {game['title']}"
        e.begin = game['start']
        e.end = game['end']
        e.description = "Забери на Epic Games: https://store.epicgames.com/ru/free-games"
        e.url = "https://store.epicgames.com/ru/free-games"
        calendar.events.add(e)

    with open("epic_free_games.ics", "w", encoding="utf-8") as f:
        f.writelines(calendar)

games = fetch_free_games()
generate_calendar(games)
