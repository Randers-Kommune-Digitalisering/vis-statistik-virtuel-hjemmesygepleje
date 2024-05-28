# app/Dockerfile

FROM python:3.12-slim

# Set dir and user
ENV APP_HOME=/app
ENV USERNAME=non-root
ENV USER_UID=11000
ENV USER_GID=$USER_UID

# Create the user
RUN addgroup --gid $USER_GID nonroot && \
    adduser --uid $USER_UID --gid $USER_GID --disabled-password --gecos "" nonroot

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libmariadb-dev

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8501

# Set user
USER $USER_UID

ENTRYPOINT ["python3", "main.py"]
#ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]