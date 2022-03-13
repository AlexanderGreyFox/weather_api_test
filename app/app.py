from aiohttp import web
from datetime import datetime
from logger import logger

from middleware import exception_catcher
from utils import get_from_weather_api, get_from_geo_api, get_current_date

routes = web.RouteTableDef()


@routes.get("/weather")
async def get_weather(request):
    city = request.rel_url.query.get('city')
    country = request.rel_url.query.get('country_code')
    date = request.rel_url.query.get('date')
    timestamp = int(datetime.fromisoformat(date).timestamp())
    lat, lon = await get_from_geo_api(city, country)
    weather_list = await get_from_weather_api(lat, lon)
    result = get_current_date(weather_list, timestamp)

    return web.json_response({'result': result})


async def my_web_app():
    app = web.Application(middlewares=[exception_catcher])
    app.add_routes(routes)
    return app

