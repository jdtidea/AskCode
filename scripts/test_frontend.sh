#!/bin/bash

(
    cd frontend;
    npm install;
    npm run test:ci;
)