
### Requirements

- Docker


### Back-End
To load environment variables
```
source .env
```

Build and run the docker container:
```
docker build -t my-telegram-bot .
```

```
docker run -v $(pwd)/data:/data --env-file .env my-telegram-bot python3 main.py
```


