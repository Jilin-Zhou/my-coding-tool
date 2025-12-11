from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    
    # 注册蓝图
    from app.routes import main, problems, functions, tags, analysis, stats, review
    app.register_blueprint(main.bp)
    app.register_blueprint(problems.bp)
    app.register_blueprint(functions.bp)
    app.register_blueprint(tags.bp)
    app.register_blueprint(analysis.bp)
    app.register_blueprint(stats.bp)
    app.register_blueprint(review.bp)
    
    return app
