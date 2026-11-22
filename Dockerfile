FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends libzbar0 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt pillow
COPY analyzer.py messages.py engine.py worker.py ./
COPY dict ./dict
CMD ["python", "-u", "worker.py"]
