FROM python:2.7.13-slim

ADD . /app

CMD ["python", "/app/run.py" ,"-f" ,"/app/data/karlsruhe_small.osm", "-n", "p" ,"-c", "-l"]