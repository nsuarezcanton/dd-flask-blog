# Native libraries
import os

# Flask
from flask import Flask

# Datadog Tracer
from ddtrace import tracer, patch_all, config
from ddtrace.contrib.flask import TraceMiddleware


def create_app(test_config=None):
    # Grab DD environment variables for APM config.
    dd_environment = False
    try:
        agent_service_host = os.environ['DD_AGENT_SERVICE_HOST']
        agent_service_port = os.environ['DD_AGENT_SERVICE_PORT']
        if (agent_service_host and agent_service_port):
            dd_environment = True
    except:
        pass
    # If variables not set, skips APM configuration.
    if (dd_environment):
        patch_all()
        tracer.configure(
            hostname=os.environ['DD_AGENT_SERVICE_HOST'],
            port=os.environ['DD_AGENT_SERVICE_PORT'],
        )

    # Create and configure the application
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Attached DB
    from . import db
    db.init_app(app)

    # Attach routes
    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
