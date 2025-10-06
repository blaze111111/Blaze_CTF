# Dockerfile (player image)
FROM python:3.11-slim

WORKDIR /app

# copy only the player-visible parts
COPY src/ /app/src/
COPY tests/ /app/tests/
COPY .gitignore /app/.gitignore

RUN pip install --no-cache-dir flask requests pytest

EXPOSE 5000

CMD ["python", "/app/src/main.py"]
