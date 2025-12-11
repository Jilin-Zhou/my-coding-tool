from flask import Blueprint, jsonify
from app.models import Problem, Tag, Function
from app import db
from sqlalchemy import func
from datetime import datetime, timedelta

bp = Blueprint('stats', __name__, url_prefix='/stats')

@bp.route('/overview')
def overview():
    """获取统计概览数据"""
    total_problems = Problem.query.count()
    
    # 难度分布
    difficulty_stats = db.session.query(
        Problem.difficulty,
        func.count(Problem.id)
    ).group_by(Problem.difficulty).all()
    
    # 标签分布
    tag_stats = db.session.query(
        Tag.name,
        func.count(Problem.id)
    ).join(Problem.tags).group_by(Tag.id).order_by(
        func.count(Problem.id).desc()
    ).limit(10).all()
    
    # 刷题趋势（最近30天）
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    trend_data = db.session.query(
        func.date(Problem.created_at),
        func.count(Problem.id)
    ).filter(
        Problem.created_at >= thirty_days_ago
    ).group_by(
        func.date(Problem.created_at)
    ).all()
    
    return jsonify({
        'total_problems': total_problems,
        'difficulty_stats': [{'difficulty': d[0] or '未分类', 'count': d[1]} for d in difficulty_stats],
        'tag_stats': [{'tag': t[0], 'count': t[1]} for t in tag_stats],
        'trend_data': [{'date': str(t[0]), 'count': t[1]} for t in trend_data]
    })

@bp.route('/functions/top')
def top_functions():
    """获取高频函数 Top 10"""
    top_funcs = Function.query.order_by(
        Function.frequency.desc()
    ).limit(10).all()
    
    return jsonify([{
        'id': f.id,
        'name': f.name,
        'category': f.category,
        'frequency': f.frequency
    } for f in top_funcs])
