FROM python:3.8-slim
WORKDIR /app
COPY . /app
RUN pip install tensorflow flask pandas numpy requests
EXPOSE 5001
CMD ["python", "app.py"]
