FROM python:3.8.3-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_HOME=/usr/src/shop_project
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip

COPY . $APP_HOME

RUN pip install -r requirements.txt

ENTRYPOINT ["/usr/src/shop_project/entrypoint.prod.sh"]