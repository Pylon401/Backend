from aiohttp import web, ClientSession
import feedparser

import asyncio
import json

# URLS
# https://pypi.org/rss/updates.xml
# https://pypi.org/rss/packages.xml
# https://api.github.com/search/repositories?q=language:python&sort=stars&order=desc
# https://api.github.com/search/repositories?q=language:python&sort=updated&order=desc

# The FETCH Level
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

# The NORMALIZE Level
async def normalize_pypi(session, url):
    feed_data = feedparser.parse(await fetch(session, url))
    entries = feed_data.entries
    normalized_entries = []
    for entry in entries:
        normalized_entries.append({
            'source': 'pypi',
            'title': entry['title'],
            'link': entry['link'],
            'desc': entry['summary']
        })

    return normalized_entries

async def normalize_github(session, url):
    response = await fetch(session, url)
    normalized_entries = []
    for entry in response:
        normalized_entries.append({
            'source': 'github',
            'title': entry['name'],
            'link': entry['html_url'],
            'desc': entry['description'],
            'stars': entry['stargazers_count']
        })

    return normalized_entries

# The GATHER Level
async def main(request):
    entries = []
    async with ClientSession() as session:
        entries.append(await normalize_pypi(session, 'https://pypi.org/rss/updates.xml'))
        entries.append(await normalize_pypi(session, 'https://pypi.org/rss/packages.xml'))

    return web.Response(text=json.dumps(entries))

# The RUN Level
app = web.Application()
app.add_routes([
    web.get('/', main),
])

if __name__ == '__main__':
    web.run_app(app)