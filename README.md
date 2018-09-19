# beekeeper-core
Beekeeper core for hangover face recognition

## How to run
```bash
cd beekeeper-core
docker build -t beekeeper-core .
docker run --rm --name beekeeper-core -p 8000:8000 -ti beekeeper-core
```

## How to use
```bash
curl --form file=@someimage.png http://localhost:8000/upload
```
