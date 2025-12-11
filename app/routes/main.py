from flask import Blueprint, render_template
from app.models import Problem, Tag, Function
from app.services.review import ReviewService
from sqlalchemy import func
from datetime import datetime, timedelta

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Dashboard 主页"""
    # 统计数据
    total_problems = Problem.query.count()
    
    # 难度分布
    difficulty_stats = db.session.query(
        Problem.difficulty,
        func.count(Problem.id)
    ).group_by(Problem.difficulty).all()
    
    difficulty_data = {
        'labels': [d[0] if d[0] else '未分类' for d in difficulty_stats],
        'data': [d[1] for d in difficulty_stats]
    }
    
    # 最近7天刷题趋势
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_problems = Problem.query.filter(
        Problem.created_at >= seven_days_ago
    ).order_by(Problem.created_at.desc()).all()
    
    # 按日期分组
    daily_counts = {}
    for i in range(7):
        date = (datetime.utcnow() - timedelta(days=6-i)).strftime('%m-%d')
        daily_counts[date] = 0
    
    for problem in recent_problems:
        date = problem.created_at.strftime('%m-%d')
        if date in daily_counts:
            daily_counts[date] += 1
    
    trend_data = {
        'labels': list(daily_counts.keys()),
        'data': list(daily_counts.values())
    }
    
    # 标签分布（Top 10）
    tag_stats = db.session.query(
        Tag.name,
        func.count(Problem.id)
    ).join(Problem.tags).group_by(Tag.id).order_by(
        func.count(Problem.id).desc()
    ).limit(10).all()
    
    tag_data = {
        'labels': [t[0] for t in tag_stats],
        'data': [t[1] for t in tag_stats]
    }
    
    # 高频函数 Top 10
    top_functions = Function.query.order_by(
        Function.frequency.desc()
    ).limit(10).all()
    
    # 最近题目
    recent_problems_list = Problem.query.order_by(
        Problem.created_at.desc()
    ).limit(5).all()
    
    # 需要复习的题目
    due_reviews = ReviewService.get_due_reviews()
    
    return render_template('index.html',
                         total_problems=total_problems,
                         difficulty_data=difficulty_data,
                         trend_data=trend_data,
                         tag_data=tag_data,
                         top_functions=top_functions,
                         recent_problems=recent_problems_list,
                         due_reviews_count=len(due_reviews))

from app import db
