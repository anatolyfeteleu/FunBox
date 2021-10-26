# FunBox

----

API for FunBox project based on [Django framework](https://www.djangoproject.com/).

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


## Documentation

Documentation is alocated on URL: `{protocol}://{domain}:{port}/docs/`  
Or  
you can use `Swagger scheme`

## Swagger scheme
Location: `Insomnia_2021-10-26.json`
