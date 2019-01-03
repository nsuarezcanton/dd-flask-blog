FROM python:3.7
# Build-time arguments (with default values).
ARG FLASK_APP=app
ARG FLASK_ENV=development
# Environment variables for runtime.
ENV FLASK_APP=${FLASK_APP}
ENV FLASK_ENV=${FLASK_ENV}
# Copy application & set work directory.
COPY . /app
WORKDIR /app
# Install requirements.
RUN pip install -r requirements.txt
# Initialize DB.
RUN flask init-db
# Start the application.
ENTRYPOINT ["flask"]
CMD ["run", "--host=0.0.0.0", "--port=8080"]
