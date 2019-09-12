from app.api_fetch import (
    normalize_github, 
    normalize_pypi, 
    normalize_reddit_programmerhumor, 
    normalize_reddit_no_image,
    normalize_reddit_webdev
)

import pytest
import feedparser

import asyncio
import json


# ========
# FIXTURES
# ========

@pytest.fixture
def github_sample():
    with open('test/github_sample.json') as file:
        contents = file.read()
    return json.loads(contents)


@pytest.fixture
def pypi_sample():
    with open('test/pypi_sample.xml') as file:
        contents = file.read()

    return feedparser.parse(contents)


@pytest.fixture
def humor_sample():
    with open('test/programmerhumor_sample.json') as file:
        contents = file.read()

    return json.loads(contents)


@pytest.fixture
def no_image_sample():
    with open('test/reddit_no_images_sample.json') as file:
        contents = file.read()

    return json.loads(contents)


@pytest.fixture
def webdev_sample():
    with open('test/webdev_sample.json') as file:
        contents = file.read()

    return json.loads(contents)


# =====
# TESTS
# =====

def test_normalize_reddit_webdev(webdev_sample):
    expected = {
        'source': 'reddit',
        'category': 'webdev',
        'data': [
            {
                'title': 'This video shows the most popular programming languages on Stack Overflow since September 2008',
                'link': '/r/webdev/comments/d30k6s/this_video_shows_the_most_popular_programming/',
                'thumbnail': 'https://a.thumbs.redditmedia.com/odFWirrXKbYp38Dm2lxw-fj3Q3a_aPuKlLS97phWx50.jpg',
                'ups': 931
            }
        ]
    }

    actual = asyncio.run(normalize_reddit_webdev
    (webdev_sample, 'webdev'))
    assert actual == expected


def test_normalize_reddit_no_image(no_image_sample):
    expected = {
        'source': 'reddit',
        'category': 'python',
        'data': [
            {
                'title': 'r/Python Job Board',
                'link': '/r/Python/comments/cmq4jj/rpython_job_board/',
                'ups': 90
            }
        ]
    }

    actual = asyncio.run(normalize_reddit_no_image(no_image_sample, 'python'))
    assert actual == expected


def test_normalize_reddit_programmerhumor(humor_sample):
    expected = {
        'source': 'reddit',
        'category': 'programmerhumor',
        'data': [
            {
                'title': 'He codes in mysterious ways',
                'link': '/r/ProgrammerHumor/comments/d37zbm/he_codes_in_mysterious_ways/',
                'image': 'https://i.redd.it/kvvp34uf16m31.png',
                'ups': 4985
            }
        ]
    }

    actual = asyncio.run(normalize_reddit_programmerhumor(humor_sample, 'programmerhumor'))
    assert actual == expected


def test_normalize_github(github_sample):
    expected = {
        'source': 'github',
        'category': 'popular',
        'data':[{
            'source': 'github',
            'category': 'popular',
            "title":"system-design-primer",
            "link": "https://github.com/donnemartin/system-design-primer",
            "desc": "Learn how to design large-scale systems. Prep for the system design interview.  Includes Anki flashcards.",
            "stars": 72711
        }]
    }

    actual = asyncio.run(normalize_github(github_sample, 'popular'))
    assert actual == expected


def test_normalize_pypi(pypi_sample):
    expected = {
        'source': 'pypi',
        'category': 'updated',
        'data': [
            {
                'source': 'pypi',
                'category': 'updated',
                'title': 'confidant 5.0.1',
                'link': 'https://pypi.org/project/confidant/5.0.1/',
                'desc': 'A secret management system and client.'
            }
        ]
    }

    actual = asyncio.run(normalize_pypi(pypi_sample, 'updated'))
    assert actual == expected