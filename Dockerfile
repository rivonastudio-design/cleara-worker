FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt pillow
COPY analyzer.py messages.py engine.py worker.py ./
CMD ["python", "-u", "worker.py"]
