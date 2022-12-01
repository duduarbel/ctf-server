#!/bin/bash

cd dockers

if [ $# -eq 1 ] && [ $1 == 'clean' ]
then
    docker kill $(docker ps | awk '{print $1}')
    docker rm $(docker ps -a | awk '{print $1}')
    docker rmi ctf_cookies
    docker rmi ctf_connection_failed
    docker rmi ctf_mirror
fi

docker build -f Dockerfile_connection -t ctf_connection_failed --build-arg exe=./client,./server .
docker build -f Dockerfile_mirror -t ctf_mirror --build-arg exe=./Mirror .
docker build -f Dockerfile_cookies -t ctf_cookies --build-arg exe=./cookies .

cd ..
