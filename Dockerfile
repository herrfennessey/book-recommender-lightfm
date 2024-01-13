# We need to compile on 3.11 because lightfm requires GCC
FROM python:3.11 as builder
ENV PYTHONUNBUFFERED True

RUN pip install --upgrade pip setuptools wheel
COPY requirements.txt .
RUN pip install --no-cache-dir -r  requirements.txt

ENV APP_HOME /root
WORKDIR $APP_HOME
COPY ./src $APP_HOME/app/src
COPY ./model $APP_HOME/app/model

# Stage 2: Runtime stage with a smaller base image
FROM python:3.11-slim

# Update package list and install libgomp1 (required by lightfm)
RUN apt-get update && \
    apt-get install -y libgomp1 && \
    rm -rf /var/lib/apt/lists/*

# Copy only the built artifacts from the builder stage
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /root/app /app

# Set up environment variables
ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME

EXPOSE 8080
CMD ["gunicorn", "--bind", ":8080", "src.main:app"]
