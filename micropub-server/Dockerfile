FROM node:20-alpine
RUN apk add --no-cache git openssh-client
RUN git config --global --add safe.directory /repo \
 && git config --global user.email "ed@bowlerdesign.co.uk" \
 && git config --global user.name "Ed Leeman"
WORKDIR /app
COPY package.json .
RUN npm install
COPY index.js .
CMD ["node", "index.js"]
