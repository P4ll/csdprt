FROM python:3.8.3-alpine
# set work directory
WORKDIR /usr/src/app
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev python3-dev jpeg-dev zlib-dev
# install dependencies
RUN pip install --upgrade pip
#COPY ./requirements.txt .
COPY . .
RUN pip install -r requirements.txt
# copy project
RUN mkdir /root/.config/ \
    && mkdir /root/.config/gspread 
COPY service_account.json /root/.config/gspread/service_account.json
RUN python manage.py migrate
EXPOSE 8008
