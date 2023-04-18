FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt

COPY . .

ENV TELEGRAM_BOT_TOKEN=6020286361:AAF9PdDM7pNjbJFEoULkHXcA7rhxsMc-V8E

EXPOSE 5000

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000" ]
