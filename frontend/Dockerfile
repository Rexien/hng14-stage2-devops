FROM node:22-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci

FROM node:22-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
RUN apk upgrade --no-cache
RUN addgroup -S appgroup && adduser -S appuser -G appgroup && chown -R appuser:appgroup /app
USER appuser
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget -qO- http://localhost:3000/ > /dev/null || exit 1
CMD ["npm", "start"]
