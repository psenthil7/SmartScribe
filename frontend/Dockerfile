FROM node:18-alpine

WORKDIR /app

# copy package files
COPY package*.json ./
RUN npm install

# copy src
COPY  . .

RUN npm run build

RUN npm install -g serve

EXPOSE 3000

CMD ["serve", "-s", "build", "-l", "3000"]
