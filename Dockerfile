FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir "pip>=26.2.2" && pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
ENV PYTHONUNBUFFERED=1
CMD ["streamlit", "run", "twitter_on_health.py", "--server.port=8501", "--server.headless=true"]
