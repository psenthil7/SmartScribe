FROM python:3.11-slim

# install dependencies
RUN -apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

    