#!/bin/bash
app="flask_docker"
docker build -t ${app} .
docker run -d -p 80:5000 \
  --name=${app} \
  -v $PWD:/app ${app}
