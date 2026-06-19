FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY boundarycam_runtime ./boundarycam_runtime
COPY runtime ./runtime

ENV BOUNDARYCAM_DB=/data/boundarycam.sqlite3
EXPOSE 4187

CMD ["python3", "-m", "uvicorn", "boundarycam_runtime.api:app", "--host", "0.0.0.0", "--port", "4187"]
