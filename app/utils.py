import aiohttp
import asyncio
import os
from urllib import parse

api_key = os.environ.get("API_KEY")


async def get_from_geo_api(city, country):
    base_url = "http://api.openweathermap.org/geo/1.0/direct"
    query = f"?q={city},{country}&limit=5&appid={api_key}"
    url = parse.urljoin(base_url, query)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            response = await resp.json()
            lat, lon = (response[0]['lat'], response[0]['lon'])
            print(lat, lon)
            return lat, lon


async def get_from_weather_api(lat, lon):
    base_url = "https://api.openweathermap.org/data/2.5/onecall"
    query = f"?lat={lat}&lon={lon}&exclude=current,minutely,daily&appid={api_key}"
    url = parse.urljoin(base_url, query)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            response = await resp.json()
            print(response.get('hourly'))

            return response.get('hourly', None)


def get_current_date(weather_list, current_date):
    i = 0
    j = 1

    while j < len(weather_list):
        if current_date > weather_list[i]['dt'] and current_date < weather_list[j]['dt']:
            return [weather_list[i], weather_list[j]]
        elif current_date == weather_list[i]['dt']:
            return weather_list[i]
        elif current_date == weather_list[j]['dt']:
            return weather_list[j]
        elif j == len(weather_list):
            return []
        else:
            i += 1
            j += 1


if __name__ == '__main__':
    lat, lon = asyncio.run(get_from_geo_api("Moscow", 'RU'))
    weather_list = asyncio.run(get_from_weather_api(lat, lon))
    print(get_current_date(weather_list, 1645120701))
