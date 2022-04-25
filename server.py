import asyncio
import os
import json
import logging
from datetime import timedelta, datetime

os.environ.setdefault('AIOHTTP_NO_EXTENSIONS', "1")
from aiohttp import web
import aiohttp

USER_AGENT = {"User-Agent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-A605FN) AppleWebKit/537.36 (KHTML, like Gecko)"
                            " Chrome/87.0.4280.86 Mobile Safari/537.36"}
EXCHANGE_API_URL = "http://127.0.0.1/NBUStatService/v1/statdirectory/exchange"
with open("config.json") as file:
    CONFIG = json.load(file)
    print(CONFIG)


def daterange(start_date, end_date):
    for n in range((end_date - start_date).days):
        yield start_date + timedelta(n)


async def get_exchange(date_, session):
    params = {'date': date_.strftime("%Y%m%d"), 'json': 'get_data'}
    async with session.get(EXCHANGE_API_URL, params=params, headers=USER_AGENT) as response:
        return await response.json()


def authorise(token):
    username = CONFIG["tokens"].get(token)
    if not username:
        raise aiohttp.web.HTTPUnauthorized(text="Unauthorized")
        logging.warning("Unauthorized %s", username)
    logging.warning("Authorised %s", username)


async def handle(request):
    # print()
    # print(request.query)
    authorise(request.headers["Authentication"])
    input_data = request.query

    try:
        from_date = datetime.strptime(input_data['from'], '%Y-%m-%d').date()
        to_date = datetime.strptime(input_data['to'], '%Y-%m-%d').date()
    except:
        return aiohttp.web.HTTPBadRequest(text="400, Check format: /exchange?from=yyyy-mm-dd&to=yyyy-mm-dd")

    async with aiohttp.ClientSession() as session:
        tasks = []
        for item in daterange(from_date, to_date):
            task = get_exchange(item, session)
            tasks.append(task)
        results = await asyncio.gather(*tasks)

    return web.json_response(results)


def create_app():
    app = web.Application()
    app.add_routes([web.get('/exchange', handle)])
    return app


if __name__ == '__main__':
    web.run_app(create_app())
