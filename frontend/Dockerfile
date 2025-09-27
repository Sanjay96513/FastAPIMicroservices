# Stage 1: Build the React application
FROM node:20-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Serve the application with a production-ready server
FROM nginx:stable-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
# The default nginx configuration is usually sufficient for a single-page application.
# A custom nginx.conf could be added here if needed for specific routing rules.
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]