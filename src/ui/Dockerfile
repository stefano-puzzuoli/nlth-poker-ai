FROM node:alpine
WORKDIR '/app'

COPY package.json .
RUN npm install yarn
COPY . .
CMD ['yarn', 'start']