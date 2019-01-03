# DD Flask Blog

The objective of this exercise is to learn about Flask, Docker and Kubernetes as well as how they work with Datadog. As of now, it shows how the [Flask tutorial application](http://flask.pocoo.org/docs/1.0/tutorial/) can be built as a Docker image, instrumented with Datadog and deployed to a Kubernetes cluster. The APM instrumentation is fully-operational on a Docker host, and the objective is to have the same on a Kubernetes environment soon.

## Locally

Though no essential, it’s a good sanity check to be able to run the application locally. There are two steps: (1) environment setup, and (2) running the app. This assumes that you have `python3` installed.

### Setting up your Python environment

Create a Python environment and install dependencies.

```bash
# Create a Python virtual environment
$ python3 -m venv venv
# Activate the environment
$ . venv/bin/activate
# Install dependencies
$ pip install -r ./blog/requirements.txt
```

### Running the Flask application

From the blog app directory, launch the flask app. You may spice up (🌶) the hostname and port if you’d like.

```bash
# From root folder
$ cd ./blog
# Put these bad boys on your path
$ export FLASK_APP=app
$ export FLASK_ENV=development
# Initialize DB
$ flask init-db
# Run the flask app
$ flask run
# or caliente
$ flask run --host=0.0.0.0 --port=8080
```

## Docker

This section covers how to build and run a Docker image of the Flask application as well as how to run the app along with the Datadog Agent and APM solution using `docker-compose`.

### Running the application with Docker

Let’s build a nice Docker image for this puppy (🐶).

```bash
# From root folder
$ docker build ./blog -t blog:latest
# Run image. Map port from HOST to GUEST (HOST:GUEST)
$ docker run -p 8080:8080 blog:latest
```

This approach is useful to test that the Docker image builds correctly and that you can run the app within a container.

### Running the app with Datadog Agent (Docker Compose)

If we add `docker-compose` to the mix, we can quickly build the application along with the Datadog Agent. The Docker Configuration is done such that it makes use of `env/datadog.env` to set-up the agent as well as APM for the Flask application.

#### Setup

Create a file under `env` called `secret.env` . The contents of this file should look like:

```
DD_API_KEY=<your-api-key>
```

#### Running the App

It can be quickly built along quick the Datadog Agent as shown below. Need to figure whether it’s properly setup—logs look fishy (🐠).

```bash
$ docker-compose up
# or re-building the images
$ docker-compose up --build
```

If you started the app with `docker-compose`, you should see it on the Infrastructure List. In any case, you can check it out from the command line and browser.

```bash
$ curl localhost:8080
```

After hitting the applications endpoints a few times and giving it a few minutes, you should be able to see Traces. Also, given the provided Datadog config (`env/datadog.env`) , you should be able to see the applications logs. Here's an example trace:

<img src="/readme-assets/trace_example.gif" alt="Example Datadog APM Trace">

## WIP: Kubernetes

The Kubernetes deployment part of this example is still WIP. You can deploy the application to `minikube` but the Datadog part of this setup is not complete.

### Start `minikube`

```bash
# Start me up
$ minikube start
# Configure Docker environment
$ eval $(minikube docker-env)
# Build blog:latest
$ docker build ./blog -t blog:latest
```

**Note:** the _build_ command is important. Otherwise, `minikube` won’t find the image for the application.

### Build environment secrets

Create a file under `kuberbetes` called `dd_secret.txt` . The contents of this file should look like:

```
DD_API_KEY=<your-api-key>
```

Use `kubectl` to build a secret that will be passed into the Datadog Agent pod with your API key.

```bash
$ kubectl create secret generic datadog --from-env-file=kubernetes/dd_secret.txt
```

### Agent

```bash
# Deploy agent to Kubernetes cluster
$ kubectl apply -f kubernetes/agent_deploy.yaml
```

### Application

```bash
# Deploy app to Kubernetes cluster
$ kubectl apply -f kubernetes/blog_deploy.yaml
# and you can hit it up from localhost:8080
$ kubectl port-forward deployment/blog 8080:8080
```
