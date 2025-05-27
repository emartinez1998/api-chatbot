FROM python:3.11-slim

WORKDIR /api-chatbot


# - libglib2.0-0, libpango1.0-0, libgdk-pixbuf2.0-0 y libcairo2: requeridas por WeasyPrint
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    libpq-dev \
    gcc \
    libglib2.0-0 \
    libpango1.0-0 \
    libgdk-pixbuf2.0-0 \
    libcairo2 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /api-chatbot/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "api_chatbot.wsgi:application", "--bind", "0.0.0.0:8000"]