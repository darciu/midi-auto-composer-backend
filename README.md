# scamp

To build the image
```
docker build -t "midi_composer_img" .
```

For running the container
```
docker run -d --name midi_composer_container -p 8000:8000 midi_composer_img
```

Documentation will be available under this address:
```
http://localhost:8000/docs#/
```