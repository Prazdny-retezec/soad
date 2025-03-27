# Use node to build the Vue.js app
FROM node:lts-alpine as build

# Set working directory
WORKDIR /app

# Install project dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the source files and build the app
COPY . .
RUN npm run build

# use Nginx to serve the app
FROM nginx:alpine

# copy the built app to Nginx's default web directory
COPY --from=build /app/dist /usr/share/nginx/html

# copy a custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# expose port 80 for the web server
EXPOSE 80

# start Nginx server
CMD ["nginx", "-g", "daemon off;"]