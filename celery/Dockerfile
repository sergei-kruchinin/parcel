FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src /app/
RUN useradd -m myuser
RUN chown -R myuser:myuser /app
USER myuser


