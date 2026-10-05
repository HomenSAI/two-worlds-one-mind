# Reproducible environment for building and checking the book.
# Isolated from every other project: it only reads the repository mounted at /work.
FROM node:22.11.0-bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PUPPETEER_SKIP_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      chromium python3 python3-pip git ca-certificates \
      fonts-liberation fonts-dejavu-core poppler-utils \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/tools
COPY tools/requirements.txt tools/package.json tools/package-lock.json ./
RUN pip3 install --break-system-packages --no-cache-dir -r requirements.txt \
 && npm install -g npm@10.9.3 \
 && npm ci --legacy-peer-deps --no-audit --no-fund

ENV NODE_PATH=/opt/tools/node_modules \
    PATH=/opt/tools/node_modules/.bin:$PATH
WORKDIR /work
