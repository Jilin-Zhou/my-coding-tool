"""
应用启动入口
"""

import os
from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # 确保数据库表存在
        db.create_all()
    
    # 启动开发服务器
    # 注意：生产环境应使用 WSGI 服务器（如 gunicorn）而不是 Flask 内置服务器
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
