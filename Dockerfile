FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y python3-tk xvfb

COPY . /app

RUN pip install --no-cache-dir numpy perlin_noise

CMD ["xvfb-run", "-a", "python", "wumpus_Final.py"]
