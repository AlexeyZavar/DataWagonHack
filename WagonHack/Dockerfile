FROM node:16-bullseye

WORKDIR /app
COPY package.json package.json
RUN yarn

COPY . .

RUN yarn generate

ENV HOST 0.0.0.0
CMD [ "yarn", "start" ]
