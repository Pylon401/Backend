from aiohttp import web, ClientSession
import aiohttp_cors
import uvloop
import feedparser

import asyncio
import time
import json


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

__all__ = ["app"]

routes = web.RouteTableDef()

# =====
# FETCH
# =====

async def fetch(session, url):
    """
    Takes in a ClientSession and a URL string.
    Awaits a request to the given URL.
    Returns the payload.
    """
    async with session.get(url) as response:
        return await response.text()


# ===========
# NORMALIZERS
# ===========

async def normalize_reddit_webdev(response, category):
    """
    Takes in a response from the webdev subreddit.
    Parses the entries and normalizes them for our use.
    Returns the normalized entries.
    """
    entries = response['data']['children']

    normalized_entries = {
        'source': 'reddit',
        'category': category,
        'data':[]
    }

    for entry in entries:
        normalized_entries['data'].append({
            'title': entry['data'].get('title', None),
            'link': entry['data'].get('permalink', None),
            'thumbnail': entry['data'].get('thumbnail', None),
            'ups': entry['data'].get('ups', None),
        })

    return normalized_entries


async def reddit_webdev(session, url, category):
    """
    Takes in a ClientSession and a URL string to WebDev Subreddit.
    Awaits a fetch coroutine, then normalizes the payload.
    Returns the normalized entries.
    """
    print('url start', url)
    response = json.loads(await fetch(session, url))
    print('url done', url)

    return await normalize_reddit_webdev(response, category)


async def normalize_reddit_programmerhumor(response, category):
    """
    Takes in a response from the ProgrammerHumor subreddit.
    Parses the entries and normalizes them for our use.
    Returns the normalized entries.
    """
    entries = response['data']['children']
    normalized_entries = {
        'source': 'reddit',
        'category': category,
        'data':[]
    }

    for entry in entries:

        normalized_entries['data'].append({
            'title': entry['data'].get('title', None),
            'link': entry['data'].get('permalink', None),
            'image': entry['data'].get('url', None),
            'ups': entry['data'].get('ups', None),
        })

    return normalized_entries


async def reddit_programmerhumor(session, url, category):
    """
    Takes in a ClientSession and a URL string to Programmer Humor Subreddit.
    Awaits a fetch coroutine, then normalizes the payload.
    Returns the normalized entries.
    """
    print('url start', url)
    response = json.loads(await fetch(session, url))
    print('url done', url)

    return await normalize_reddit_programmerhumor(response, category)
    

async def normalize_reddit_no_image(response, category):
    """
    Takes in a response from the Reddit API.
    Parses the entries and normalizes them for our use.
    Returns the normalized entries.
    """
    entries = response['data']['children']
    
    normalized_entries = {
        'source': 'reddit',
        'category': category,
        'data':[]
    }

    for entry in entries:
        normalized_entries['data'].append({
            'title': entry['data'].get('title', None),
            'link': entry['data'].get('permalink', None),
            'ups': entry['data'].get('ups', None),
        })

    return normalized_entries


async def reddit_no_image(session, url, category):
    """
    Takes in a ClientSession and a URL string to Python Subreddit.
    Awaits a fetch coroutine, then normalizes the payload.
    Returns the normalized entries.
    """
    print('url start', url)
    response = json.loads(await fetch(session, url))
    print('url done', url)

    return await normalize_reddit_no_image(response, category)


async def normalize_pypi(feed_data, category):
    """
    Takes in a response from the PyPI API.
    Parses the entries and normalizes them for our use.
    Returns the normalized entries.
    """
    entries = feed_data.entries

    normalized_entries = {
        'source': 'pypi',
        'category': category,
        'data':[]
    }

    for entry in entries:
        normalized_entries['data'].append({
            'source': 'pypi',
            'category': category,
            'title': entry['title'],
            'link': entry['link'],
            'desc': entry['summary']
        })

    return normalized_entries


async def pypi(session, url, category):
    """
    Takes in a ClientSession and a URL string to PyPI.
    Awaits a fetch coroutine, then normalizes the payload.
    Returns the normalized entries.
    """
    print('url start', url)
    feed_data = feedparser.parse(await fetch(session, url))
    print('url done', url)

    return await normalize_pypi(feed_data, category)


async def normalize_github(response, category):
    """
    Takes in a response from the GitHub API.
    Parses the entries and normalizes them for our use.
    Returns the normalized entries.
    """
    entries = response['items']
    
    normalized_entries = {
        'source': 'github',
        'category': category,
        'data':[]
    }

    for entry in entries:
        normalized_entries['data'].append({
            'source': 'github',
            'category': category,
            'title': entry['name'],
            'link': entry['html_url'],
            'desc': entry['description'],
            'stars': entry['stargazers_count']
        })

    return normalized_entries


async def github(session, url, category):
    """
    Takes in a ClientSession and a URL string to GitHub.
    Awaits a fetch coroutine, then normalizes the payload.
    Returns the normalized entries.
    """
    print('url start', url)
    response = json.loads(await fetch(session, url))
    print('url done', url)
    

    return await normalize_github(response, category)


# ======
# ROUTES
# ======

async def gather_data(request):
    start_time = time.perf_counter()
    entries = []

    async with ClientSession() as session:
        entries.append(github(session, 'https://api.github.com/search/repositories?q=language:python&sort=stars&order=desc', 'popular'))
        entries.append(github(session, 'https://api.github.com/search/repositories?q=language:python&sort=updated&order=desc', 'updated'))
        entries.append(reddit_webdev(session, 'https://www.reddit.com/r/webdev/.json?', 'webdev'))
        entries.append(reddit_programmerhumor(session, 'https://www.reddit.com/r/programmerhumor/.json?', 'programmerhumor'))
        entries.append(reddit_no_image(session, 'https://www.reddit.com/r/python/.json?', 'python'))
        entries.append(reddit_no_image(session, 'https://www.reddit.com/r/learnprogramming/.json?', 'learnprogramming'))
        entries.append(pypi(session, 'https://pypi.org/rss/updates.xml', 'updated'))
        entries.append(pypi(session, 'https://pypi.org/rss/packages.xml', 'newest'))

        results = await asyncio.gather(*entries)
    
    elapsed_time = time.perf_counter() - start_time
    print(f'Elapsed time: {elapsed_time:0.2f}')
    return web.Response(
        text=json.dumps(results),
        headers={
            "X-Custom-Server-Header": "Custom data",
        })


# ===
# APP
# ===

app = web.Application()

cors = aiohttp_cors.setup(app)

resource = cors.add(app.router.add_resource("/"))

cors.add(resource.add_route("GET", gather_data), {
    "*":
        aiohttp_cors.ResourceOptions(allow_credentials=False),
    "http://client.example.org":
        aiohttp_cors.ResourceOptions(allow_credentials=True),
})
