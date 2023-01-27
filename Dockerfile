FROM python:3.10
LABEL maintainer="gabriel.svasc99@gmail.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./src /src
WORKDIR /src
EXPOSE 8000

RUN pip install --upgrade pip && \
  pip install -r /tmp/requirements.txt && \
  rm -rf /tmp && \
  adduser \
  --disabled-password \
  --no-create-home \
  django-user

USER django-user

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]