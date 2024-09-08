import os
from flask import Flask

def create_app(test_config=None):
    """ crear y configurar la app: 
    'instance_relative_config' crea una carpeta fuera del paquete para guardar
    datos locales, como secretos de configuración o archivos de la database """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'miniblog.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # asegurarse de que la carpeta instance existe
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # importa y llama a la base de datos
    from . import db
    db.init_app(app)

    # importa y registra el blueprint 'auth'
    from . import auth
    app.register_blueprint(auth.bp)

    # importa y registra el blueprint 'blog'
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app