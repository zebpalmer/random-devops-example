# Base Image
FROM python:3.7-slim-stretch as base

# preload reqs so docker can cache this layer for faster rebuilding
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt && pip3 install gunicorn gevent aiohttp
COPY gunicorn.cfg /gunicorn.cfg

# STAGE: Final
FROM base as final

COPY app_b.py /


HEALTHCHECK --interval=15s --timeout=5s \
  CMD curl -f http://localhost/healthz || exit 1

EXPOSE 80

CMD ["gunicorn", "--config", "/gunicorn.cfg", "-b", "0.0.0.0:80", "app_b:application"]