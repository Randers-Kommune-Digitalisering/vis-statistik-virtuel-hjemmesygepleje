# app/Dockerfile

FROM python:3.12-slim

# Set dir and user
ENV APP_HOME=/app
ENV APP_USER=non-root

# Add user
RUN addgroup $APP_USER && \
    adduser $APP_USER -D -G $APP_USER -h $APP_HOME

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libmariadb-dev

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8501

# Set user
USER $APP_USER

ENTRYPOINT ["python3", "main.py"]
#ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]