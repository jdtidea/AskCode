#!/bin/bash

image="$1";
tag="$2";

(
cd backend;
docker build -t askoptum . || exit 1;
az acr login --name askoptum1 || exit 1;
docker tag askoptum "askoptum1.azurecr.io/${image}:${tag}" || exit 1;
docker push "askoptum1.azurecr.io/${image}:${tag}" || exit 1;
)