# beekeeper-core
Beekeeper core for hangover face recognition

## How to run
```bash
cd beekeeper-core
docker build -t beekeeper-core .
docker run --rm -ti -p 8000:8000 beekeeper-core
```

## How to use
```bash
curl --form file=@someimage.png http://localhost:8000/upload
```
