import os
from flask import Flask
from .models import db
from .routes import main_bp, recipe_bp

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    # 預設設定
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'recipe_app.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # 確保 instance 資料夾存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 初始化 SQLAlchemy
    db.init_app(app)

    # 啟動時建立資料表
    with app.app_context():
        db.create_all()

    # 註冊 Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(recipe_bp)

    return app
