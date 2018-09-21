# beekeeper-core
Beekeeper core for hangover face recognition. Apply openface library for face alignment then use trained model for defining BEEKEEPER level.

### Deploy
```bash
cd beekeeper-core
docker build -t beekeeper-core .
docker run --rm --name beekeeper-core -p 8000:8000 -ti beekeeper-core
```

### Usage
```bash
curl --form file=@someimage.png http://localhost:8000/upload
```
