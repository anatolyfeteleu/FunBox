FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install gettext for makemessages command
RUN apt update && apt install -y gettext binutils libproj-dev gdal-bin

# generating directories structure
RUN mkdir -p /app/code /app/requirements

ADD ./requirements /app/requirements

# update pip
RUN python -m pip install --upgrade pip

# install requirements
RUN pip install --no-cache-dir -r /app/requirements/base.txt && \
    pip install --no-cache-dir -r /app/requirements/dev.txt

# set working directory
WORKDIR /app/code

ADD . /app/code
