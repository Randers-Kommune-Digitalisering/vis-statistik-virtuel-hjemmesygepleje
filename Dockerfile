FROM node:lts-alpine

# make the 'app' folder the current working directory
WORKDIR /app

# copy project files and folders to the current working directory
COPY . .

# install project dependencies
RUN cd frontend && npm install

# build app for production with minification
RUN cd frontend && npm run build

RUN cp -r frontend/dist dist

RUN rm -rf frontend

# install project dependencies
RUN cd backend && npm install

# Run express server
RUN cd backend && npm ci --only=production

CMD [ "node", "backend/index.js" ]