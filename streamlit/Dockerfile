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

# Install dependencies
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt-get clean

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8501

# Set user
USER $USER_UID

ENTRYPOINT ["python3", "main.py"]