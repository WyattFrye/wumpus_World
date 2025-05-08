
FROM python:3.11

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y python3-tk

COPY . .

RUN pip install --no-cache-dir numpy perlin_noise tk


CMD ["python", "wumpus_Final.py"]

RUN apt-get install -y xvfb
CMD ["xvfb-run", "python", "your_script.py"]