FROM python:3.9.2-alpine

# upgrade pip
RUN pip install --upgrade pip

# get curl for healthchecks
RUN apk add curl

# permissions and nonroot user for tightened security
RUN adduser -D nonroot
RUN mkdir /app/ && chown -R nonroot:nonroot /app
RUN mkdir -p /var/log/app && touch /var/log/app/app.err.log && touch /var/log/app/app.out.log
RUN chown -R nonroot:nonroot /var/log/app
WORKDIR /app
USER nonroot

# venv
ENV VIRTUAL_ENV=/app/venv

# python setup
COPY --chown=nonroot:nonroot requirements.txt requirements.txt
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN export APP=app.py
RUN pip install -r requirements.txt

# copy files
COPY --chown=nonroot:nonroot app.py wsgi.py ./

# define the port number the container should expose
EXPOSE 8080

HEALTHCHECK --start-period=5s --timeout=15s --interval=30s \
    CMD curl --fail http://localhost:8080/health-check || exit 1   

CMD exec gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 app:app