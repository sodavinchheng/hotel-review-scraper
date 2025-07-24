# Development stage
FROM node:20-alpine as development

WORKDIR /app

# Install system dependencies
RUN apk add --update \
    curl \
    jq \
    && rm -rf /var/cache/apk/*

# Install Java 11 for OpenAPI generation
RUN apk add --no-cache java-cacerts
RUN apk --no-cache add openjdk11 --repository=http://dl-cdn.alpinelinux.org/alpine/edge/community

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install -g @openapitools/openapi-generator-cli
RUN npm install

# Copy source code
COPY . .

# Expose port
EXPOSE 5173

# Start development server
CMD ["npm", "run", "dev", "--", "--host"]
