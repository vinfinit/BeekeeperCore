FROM bamos/openface
MAINTAINER vinfinit https://github.com/vinfinit

WORKDIR /app/beekeeper-core
COPY models models
COPY server server

EXPOSE 8000

CMD ["python", "server/main.py"]
