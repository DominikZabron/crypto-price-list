FROM python:3.7.2-alpine3.9

WORKDIR /app

COPY . /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

RUN pip install --trusted-host pypi.python.org pipenv
RUN pipenv lock -r >> requirements.txt
RUN pip install -r requirements.txt