FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY prisma ./prisma
COPY start.sh ./start.sh

RUN python -m prisma generate
RUN chmod +x /app/start.sh

EXPOSE 8000

CMD ["/app/start.sh"]
