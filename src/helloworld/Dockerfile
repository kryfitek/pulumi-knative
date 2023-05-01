FROM python:3.9.2-alpine

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# get curl for healthchecks
RUN apk add curl

# Copy local code to the container image.
ENV APP_HOME /app
ENV PORT 8080
WORKDIR $APP_HOME
COPY app.py wsgi.py requirements.txt ./

# Install production dependencies.
RUN pip install -r requirements.txt

EXPOSE $PORT

HEALTHCHECK --start-period=5s --timeout=15s --interval=30s \
    CMD curl --fail http://localhost:$PORT/health-check || exit 1   

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app