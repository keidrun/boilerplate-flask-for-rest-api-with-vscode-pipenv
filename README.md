# boilerplate-flask-for-rest-api-with-vscode-pipenv [![Build Status][travis-image]][travis-url] [![Coverage][codecov-image]][codecov-url] [![License: MIT][license-image]][license-url]

Boilerplate of Flask for REST API with VSCode and Pipenv.

## Required

- Docker installed

## Let's begin developing

```bash
git clone https://github.com/keidrun/boilerplate-flask-for-rest-api-with-vscode-pipenv.git
cd boilerplate-flask-for-rest-api-with-vscode-pipenv
docker-compose up
```

## Develop with debugging (Remote Debugging)

### 0. Prepare

It's necessary to insatll `ptvsd` locally for Remote Debugging.

```bash
pip install ptvsd
```

### 1. Turn on remote debugging mode

Set `FLASK_ENV=debugging` in `docker-compose.yml`.

```yaml
...
    environment:
      - FLASK_ENV=debugging
...
``````

#### FLASK_ENV

|  FLASK_ENV  |                Description                |
| ----------- | ----------------------------------------- |
| puroduction | Activate flask puroduction mode           |
| development | Activate flask development mode           |
|  debugging  | Use remote debugging config and no reload |
|  testing    | Enable flask TESTING flag                 |

### 2. Run Docker

```bash
docker-compose up
``````

### 3. Attach to Docker Container from VSCode

Execute debugging in VSCode

## Develop with testing

```bash
docker-compose -f docker-compose.test.yml up -d
docker-compose -f docker-compose.test.yml exec web pytest -sv --cov=src --cov-report term-missing test/
```

## API endpoints

|  Method  |       URI        |         Data          |
| -------- | ---------------- | --------------------- |
|   POST   |  /api/users      | name,age,gender,email |
|   GET    |  /api/users      |           -           |
|   GET    |  /api/users/:id  |           -           |
|   PUT    |  /api/users/:id  | name,age,gender,email |
|  DELETE  |  /api/users/:id  |           -           |

[travis-url]: https://travis-ci.org/keidrun/boilerplate-flask-for-rest-api-with-vscode-pipenv
[travis-image]: https://secure.travis-ci.org/keidrun/boilerplate-flask-for-rest-api-with-vscode-pipenv.svg?branch=master
[codecov-url]: https://codecov.io/gh/keidrun/boilerplate-flask-for-rest-api-with-vscode-pipenv
[codecov-image]: https://codecov.io/gh/keidrun/boilerplate-flask-for-rest-api-with-vscode-pipenv/branch/master/graph/badge.svg
[license-url]: https://opensource.org/licenses/MIT
[license-image]: https://img.shields.io/badge/License-MIT-yellow.svg
