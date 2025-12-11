"""
应用启动入口
"""

from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # 确保数据库表存在
        db.create_all()
    
    # 启动开发服务器
    app.run(debug=True, host='0.0.0.0', port=5000)
