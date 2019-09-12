# Pynterest - Back End

**Authors**: Tammy Do, Skyler Burger, Joshua Ho

**Version**: 1.3.0

[![CircleCI](https://circleci.com/gh/Pynterest/backend/tree/master.svg?style=svg)](https://circleci.com/gh/Pynterest/backend/tree/master)

## Overview
This back end server aggregates information from GitHub, PyPI, and Reddit for consumption by the [Pynterest front end](https://pynterest-58401.firebaseapp.com/).

## Architecture
### Frameworks
- [**aiohttp**](https://pypi.org/project/aiohttp/) : to create and run our asynchronous server

### Python Standard Library:
- [**asyncio**](https://docs.python.org/3/library/asyncio.html) : to create asynchronous coroutines and gather them for execution
- [**json**](https://docs.python.org/3/library/json.html) : to load responses from API calls into JSON format
- [**time**](https://docs.python.org/3/library/time.html) : to track the time needed to complete our requests

### Packages
- [**aiohttp_cors**](https://pypi.org/project/aiohttp_cors/) : to allow cross-origin resource sharing to our front end which is deployed on Firebase
- [**feedparser**](https://pypi.org/project/feedparser/) : to parse RSS/XML feed data
- [**pytest**](https://pypi.org/project/pytest/) : to test our codebase
- [**uvloop**](https://pypi.org/project/uvloop/) : to replace asyncio's default event loop with a faster event loop that utilizes Cython

### Continuous Integration
- [**CircleCI**](https://circleci.com/) : to manage continuous integration based on the results of our pytest testing suite

## API
- **/** : a call to the root route will return a JSON object containing results from six API requests to be consumed by a front end

## Change Log
09-09-2019 - 1.1.0
- Added GitHub and PyPI API integration

09-10-2019 - 1.2.0
- Added Reddit API integration

09-11-2019 - 1.3.0
- Deployed to [Heroku](https://pyn-terest.herokuapp.com/)
- Added CORS functionality

09-12-2019 - 1.4.0
- Added testing
- Added CircleCI integration
