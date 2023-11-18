# MIDI Auto Composer Backend

To build the image
```
docker build -t midi_auto_composer_back .
```

For running the container
```
docker run -d --name macb_container -p 8000:8000 midi_auto_composer_back
```

Documentation will be available under this address:
```
http://localhost:8000/docs#/
```

Branches:

- main - commits are being deployed to the appication
- develop - changes from task branches are merged to this branch