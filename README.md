# BeekeeperCore

BeekeeperCore is a part of [BEEKEEPER](https://github.com/vinfinit/Beekeeper) project
1. [BeekeeperNative](https://github.com/vinfinit/BeekeeperNative) - react-native application for mobile platforms
2. [BeekeeperServer](https://github.com/vinfinit/BeekeeperServer) - main node.js server
3. [BeekeeperCore](https://github.com/vinfinit/BeekeeperCore) - core application for hangover face recognition

## Workflow
1. Get image from http request
2. Apply [openface](https://github.com/cmusatyalab/openface) AlignDlib for face detection
3. Apply [openface](https://github.com/cmusatyalab/openface) AlignDlib for face alignment
4. Extract features from aligned Face
5. Use trained model for hangover face recognition

## How to Run
```bash
cd BeekeeperCore
docker build -t beekeeper-core .
docker run --rm --name beekeeper-core -p 8000:8000 -ti beekeeper-core
```

## How to Use
```bash
curl --form file=@someimage.png http://localhost:8000/upload
```
