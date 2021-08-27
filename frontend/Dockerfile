#BASE Stage - use development build target for local dev
FROM docker.repo1.uhc.com/node:13.12.0-alpine as development

# App directory
WORKDIR /app

# do npm stuff first, otherwise the build cache is borked
COPY package.json package-lock.json ./
RUN npm config set registry https://repo1.uhc.com/artifactory/api/npm/npm-virtual/ --global
RUN npm ci

# App dependencies
COPY public public
COPY src src
COPY nginx nginx

#If you are NOT targeting development, then this CMD will be ignored and the last CMD will execute
CMD [ "npm", "start" ]

# BUILD Stage, use for prod deployments
FROM development AS builder
RUN npm run build

FROM docker.repo1.uhc.com/nginx:stable-alpine AS production

COPY --from=builder /app/build /usr/share/nginx/html
COPY --from=builder /app/nginx/nginx.conf /etc/nginx/conf.d/default.conf

# if you are targeting development build target then this command will not execute
CMD ["nginx", "-g", "daemon off;"]
