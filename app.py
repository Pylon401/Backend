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

async def normalize(session, url, type):
    print(f'Norm/fetch for {url} started.')
    normalized_entries = []
    
    if type == 'pypi':
        feed_data = feedparser.parse(await fetch(session, url))
        entries = feed_data.entries

        for entry in entries:
            normalized_entries.append({
                'source': 'pypi',
                'title': entry['title'],
                'link': entry['link'],
                'desc': entry['summary']
            })
    elif type == 'github':
        entries = json.loads(await fetch(session, url))
        entries = entries['items'][:20]
    
        for entry in entries:
            normalized_entries.append({
                'source': 'github',
                'title': entry['name'],
                'link': entry['html_url'],
                'desc': entry['description'],
                'stars': entry['stargazers_count']
            })

    print(f'Norm/fetch for {url} completed.')
    return normalized_entries

# The GATHER Level
async def main(request):
    urls = [
        {
            'url': 'https://pypi.org/rss/updates.xml',
            'type': 'pypi'
        },
        {
            'url': 'https://pypi.org/rss/packages.xml',
            'type': 'pypi'
        },
        {
            'url': 'https://api.github.com/search/repositories?q=language:python&sort=stars&order=desc',
            'type': 'github'
        },
        {
            'url': 'https://api.github.com/search/repositories?q=language:python&sort=updated&order=desc',
            'type': 'github'
        }
    ]
    tasks = []

    async with ClientSession() as session:
        for url in urls:
            task = asyncio.ensure_future(normalize(session, url['url'], url['type']))
            tasks.append(task)
            breakpoint()
        
        
        responses = await asyncio.gather(*tasks)
        print(responses)

# def run_main(request):
#     loop = asyncio.get_event_loop()
#     future = asyncio.ensure_future(main())
#     loop.run_until_complete(future)

# async def main(request):
#     entries = []
#     async with ClientSession() as session:
#         result_1 = await normalize_pypi(session, 'https://pypi.org/rss/updates.xml')
#         result_2 = await normalize_pypi(session, 'https://pypi.org/rss/packages.xml')
#         result_3 = await normalize_github(session, 'https://api.github.com/search/repositories?q=language:python&sort=stars&order=desc')
#         result_4 = await normalize_github(session, 'https://api.github.com/search/repositories?q=language:python&sort=updated&order=desc')
#         entries = result_1 + result_2 + result_3 + result_4

#     return web.Response(text=json.dumps(entries))

# The RUN Level
app = web.Application()
app.add_routes([
    web.get('/', main),
])

if __name__ == '__main__':
    web.run_app(app)