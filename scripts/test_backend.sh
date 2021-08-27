#!/bin/bash

(
    cd backend;
    docker build -t askoptumtests -f Dockerfile.test . || exit 1;
    docker run -t askoptumtests cat coverage.xml >> coverage.xml;
    sed -i.bak "s:/backend/app:$(pwd)/app:" coverage.xml
)