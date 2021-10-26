# FunBox

----

API for FunBox project based on [Django framework](https://www.djangoproject.com/).

The application allows, using API methods: 
- register the visited resources; 
- get a list of these resources for a certain period of time.

As a place for storing information, `Redis` is used.

## Summary

Requirements: 
- Development
  - `requirements/dev.txt`
- Production
  - `requirements/base.txt`

## Development

To run project in sync development mode, you can use one of following commands:
```
source /<env dir>/bin/activate
python3 manage.py runserver
```

## Docker

### Installation

To build project in Docker, please build images and run them via compose:
```
docker-compose build
docker-compose up
```

### Run

To run project in Docker, please enter the following command:
```
docker-compose up
```

To connect to running container, please enter:
```
docker-compose exec app /bin/bash
```

You can use any linux shell utility or program instead of `/bin/bash`,
e.g. `ls`, `python`, `sh` or `apt` etc.


## API

### Show visits

Info: Request that returns visited resources by `from` and `to` parameters in query parameters.  
Method: `GET`  
URL: `/api/visited-domains/`

Query parameters: 
- from (`<str|int|float>`) - `POSIX` datetime format
- to (`<str|int|float>`) - `POSIX` datetime format

Sample request:
```
curl --request GET \
  --url 'http://0.0.0.0:8000/api/visited-domains/?from=1635238200&to=1735243999'
```

### Register visit

Info: Request that registers visited resources at this point in time.  
Method: `POST`  
URL: `/api/visited-links/`

Request body: 
- links (`<List[str]>`) - array of resource addresses

Sample request:
```
curl --request POST \
  --url http://0.0.0.0:8000/api/visited-links/ \
  --header 'Content-Type: application/json' \
  --data '{
	"links": [
		"https://google.com"
	]
}'
```


## Documentation

The documentation can be found at the URL: `{protocol}://{domain}:{port}/docs/`  
Or  
you can use `Swagger scheme`


## Swagger scheme

Location: `Insomnia_2021-10-26.json`
