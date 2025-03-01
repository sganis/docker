FROM python:3.10
WORKDIR /app
COPY server/ ./server/
COPY client/dist ./client/dist/
WORKDIR /app/server
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]