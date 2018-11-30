FROM python:3.7.1-slim-stretch

WORKDIR /usr/src/app

RUN pip install --upgrade pip setuptools \
  && pip install pipenv==2018.11.26

COPY Pipfile ./
COPY Pipfile.lock ./
RUN pipenv install --deploy --system

ENV PYTHONUNBUFFERED 1
ENV FLASK_APP src/app.py
ENV FLASK_ENV production

COPY ./ ./

EXPOSE 5000

CMD python src/app.py
