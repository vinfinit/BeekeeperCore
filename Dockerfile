FROM bamos/openface
MAINTAINER vinfinit https://github.com/vinfinit

RUN pip install --upgrade pip \
  scikit-learn \
  joblib

WORKDIR /app/beekeeper-core
COPY models models
COPY server server

EXPOSE 8000

CMD ["python", "server/main.py"]
