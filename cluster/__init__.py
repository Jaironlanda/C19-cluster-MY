import os
from datetime import datetime
from flask import Flask, url_for
from flask_bootstrap import Bootstrap
from . import config

def create_app(test_config=False):
    app = Flask(__name__, instance_relative_config=True)
    bootstrap = Bootstrap(app)
    
    app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'cosmo'

    flask_env = os.getenv("FLASK_ENV", None)
    
    if flask_env == "development":
        app.config.from_object(config.DevelopmentConfig)
    elif flask_env == "production":
        app.config.from_object(config.ProductionConfig)
    elif test_config:
        # Example: app = create_app({'TESTING': True, 'DATABSE': db_path})
        app.config.from_object(config.TestingConfig)

    @app.template_filter('datetimeformat')
    def datetimeformat(value, new_format=None):
        new_value = datetime.strptime(value, '%Y-%m-%d')
        return new_value.strftime(new_format)

    # from blog.user import user_bp
    # app.register_blueprint(user_bp)

    # from blog.admin import admin_bp
    # app.register_blueprint(admin_bp)
    
    from . import cluster
    app.register_blueprint(cluster.bp)

    return app