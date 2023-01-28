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
  django-user && \
  mkdir -p /vol/web/media && \
  mkdir -p /vol/web/static && \
  chown -R django-user:django-user /vol && \
  chmod -R 755 /vol

USER django-user

VOLUME ["/vol/web"]

CMD ["python", "manage.py", "0.0.0.0:8000"]