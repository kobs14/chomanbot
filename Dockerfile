FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt

COPY . .

RUN apk add --no-cache ffmpeg
ENV FFPROBE_PATH=/usr/bin/ffprobe

EXPOSE 5000

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000" ]
