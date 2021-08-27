#!/bin/bash

# Potential Improvements
# The delivery architecture is reliant to running the /infra deployment on app code deployments
# This could be shifted by creating standalone deployment scripts for the frontend and backend after initial infra run
# Backend: lifecycle ignore linux_fx_version in the app service terraform and using azure cli to update container tag
# Frontend: shift az cli upload commands from infra into frontend deploy script

# The above approach would _especially_ be recommended if frontend and backend are moved into their own repo's with their own pipelines

# this 'compiles' the frontend and places it in the deploy directory for the terraform deployment
# /frontend
bash ./scripts/build_frontend.sh &

image=${1:-"askoptum"}
tag=${2:-$(whoami)}

# This builds and pushes the docker container for the backend
# /backend
bash ./scripts/build_backend.sh "${image}" "${tag}" &

# wait for builds
wait

# This runs the terraform via runiac to configure the azure resources
# /infra
(
cd infra;
export TF_VAR_docker_tag="${tag}";
export TF_VAR_docker_image="${image}";

runiac deploy -a 8a8f04fc-cf3d-433f-972a-5ff0e8615f54 -e dev --local --container docker.repo1.uhc.com/runiac/deploy:latest-alpine-azure
)