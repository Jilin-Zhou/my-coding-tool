import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///coding_tool.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # AI 分析配置（可选）
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    OPENAI_MODEL = 'gpt-4o-mini'
    
    # 默认语言设置
    DEFAULT_LANGUAGE = 'python'
