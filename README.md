# scamp

To build the image
```
docker build -t "scamp_img" .
```

For running the container
```
docker run -d --name scamp_container -p 8000:8000 scamp_img
```

Documentation will be available under this address:
```
http://localhost:8000/docs#/
```