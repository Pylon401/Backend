from aiohttp import web, ClientSession
import feedparser

import asyncio
import json
import time


# Allows use of the @routes decorator
routes = web.RouteTableDef()


async def fetch(session, url):
    """
    Takes in a ClientSession and a URL string.
    Awaits a request to the given URL.
    Returns the payload.
    """
    async with session.get(url) as response:
        return await response.text()


async def normalize_pypi(session, url, category):
    """
    Takes in a ClientSession and a URL string to PyPI.
    Awaits a fetch coroutine, then normalizes the payload.
    Returns the normalized entries.
    """
    print('url start', url)
    feed_data = feedparser.parse(await fetch(session, url))
    print('url done', url)
    entries = feed_data.entries
    normalized_entries = []
    for entry in entries:
        normalized_entries.append({
            'source': 'pypi',
            'category': category,
            'title': entry['title'],
            'link': entry['link'],
            'desc': entry['summary']
        })

    return normalized_entries


async def normalize_github(session, url, category):
    """
    Takes in a ClientSession and a URL string to GitHub.
    Awaits a fetch coroutine, then normalizes the payload.
    Returns the normalized entries.
    """
    print('url start', url)
    response = json.loads(await fetch(session, url))
    print('url done', url)
    entries = response['items']
    normalized_entries = []

    for entry in entries:
        normalized_entries.append({
            'source': 'github',
            'category': category,
            'title': entry['name'],
            'link': entry['html_url'],
            'desc': entry['description'],
            'stars': entry['stargazers_count']
        })

    return normalized_entries


async def normalize_reddit_webdev(session, url, category):
    """
    Takes in a ClientSession and a URL string to WebDev Subreddit.
    Awaits a fetch coroutine, then normalizes the payload.
    Returns the normalized entries.
    """
    print('url start', url)
    response = json.loads(await fetch(session, url))
    print('url done', url)
    entries = response['data']['children']
    normalized_entries = []

    for entry in entries:
        normalized_entries.append({
            'source': 'reddit',
            'category': category,
            'title': entry['data'].get('title', None),
            'link': entry['data'].get('permalink', None),
            'thumbnail': entry['data'].get('thumbnail', None),
        })

    return normalized_entries


async def normalize_reddit_python(session, url, category):
    """
    Takes in a ClientSession and a URL string to Python Subreddit.
    Awaits a fetch coroutine, then normalizes the payload.
    Returns the normalized entries.
    """
    print('url start', url)
    response = json.loads(await fetch(session, url))
    print('url done', url)

    print('response:', response)

    entries = response['data']['children']
    normalized_entries = []

    for entry in entries:
        normalized_entries.append({
            'source': 'reddit',
            'category': category,
            'title': entry['data'].get('title', None),
            'link': entry['data'].get('permalink', None),
            'thumbnail': entry['data'].get('thumbnail', None),
        })

    return normalized_entries


async def normalize_reddit_learnprogramming(session, url, category):
    """
    Takes in a ClientSession and a URL string to Learn Programming Subreddit..
    Awaits a fetch coroutine, then normalizes the payload.
    Returns the normalized entries.
    """
    print('url start', url)
    response = json.loads(await fetch(session, url))
    print('url done', url)

    entries = response['data']['children']
    normalized_entries = []

    for entry in entries:
        normalized_entries.append({
            'source': 'reddit',
            'category': category,
            'title': entry['data'].get('title', None),
            'link': entry['data'].get('permalink', None),
            # 'thumbnail': entry['data'].get('thumbnail', None),
        })

    return normalized_entries


### CURRENTLY WORKING ON THIS ###
async def normalize_reddit_programminghumor(session, url, category):
    """
    Takes in a ClientSession and a URL string to Programming Humor Subreddit.
    Awaits a fetch coroutine, then normalizes the payload.
    Returns the normalized entries.
    """
    print('url start', url)
    response = json.loads(await fetch(session, url))
    print('url done', url)

    print('response:', response)

    entries = response['data']['children']
    normalized_entries = []

    for entry in entries:
        normalized_entries.append({
            'source': 'reddit',
            'category': category,
            'title': entry['data'].get('title', None),
            'link': entry['data'].get('permalink', None),

            # 'thumbnail': entry['data'].get('secure_media', None).get('oembed', None),
            # ['secure_media']['oembed'],
            # 'thumbnail': entry['data']['media']['oembed'].get('thumbnail_url', None),
        })

    return normalized_entries


@routes.get('/')
async def main(request):
    """
    Takes in a Request object from the client.
    Creates a ClientSession and coroutines for each API.
    Awaits the normalized entries from the gathered coroutines.
    Returns all of the normalized entries.
    """
    start_time = time.perf_counter()
    entries = []
    async with ClientSession() as session:

        entries.append(normalize_github(session, 'https://api.github.com/search/repositories?q=language:python&sort=stars&order=desc', 'popular'))
        entries.append(normalize_github(session, 'https://api.github.com/search/repositories?q=language:python&sort=updated&order=desc', 'updated'))
        entries.append(normalize_pypi(session, 'https://pypi.org/rss/updates.xml', 'updated'))
        entries.append(normalize_pypi(session, 'https://pypi.org/rss/packages.xml', 'newest'))
        entries.append(normalize_reddit_webdev(session, 'https://www.reddit.com/r/webdev/top/.json?', 'webdev'))
        entries.append(normalize_reddit_python(session, 'https://www.reddit.com/r/python/top/.json?', 'python'))
        entries.append(normalize_reddit_learnprogramming(session, 'https://www.reddit.com/r/learnprogramming/top/.json?', 'learnprogramming'))                        
        entries.append(normalize_reddit_programminghumor(session, 'https://www.reddit.com/r/programminghumor/top/.json?', 'programminghumor'))

        results = await asyncio.gather(*entries)

    elapsed_time = time.perf_counter() - start_time
    print(f'Elapsed time: {elapsed_time:0.2f}')
    return web.Response(text=json.dumps(results))


# Instantiates an app and adds our routes
app = web.Application()
app.router.add_routes(routes)


if __name__ == '__main__':
    web.run_app(app)