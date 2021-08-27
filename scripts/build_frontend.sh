#!/bin/bash

(
cd frontend;
npm i || exit 1;
npm run build || exit 1;
rm -rf ../infra/webapp_deploy || exit 1;
cp -R build/ ../infra/webapp_deploy;
)
