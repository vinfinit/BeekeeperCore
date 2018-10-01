FROM bamos/openface
MAINTAINER vinfinit https://github.com/vinfinit

RUN pip install --upgrade pip \
  && pip install scikit-learn==0.20.0

WORKDIR /app/beekeeper-core
COPY models models
COPY server server
COPY beekeeper beekeeper
COPY data data

EXPOSE 8000

CMD ["python", "server/main.py"]
