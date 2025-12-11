from flask import Blueprint, render_template, redirect, url_for, flash
from app.services.review import ReviewService

bp = Blueprint('review', __name__, url_prefix='/review')

@bp.route('/')
def index():
    """复习页面"""
    # 获取需要复习的题目
    due_reviews = ReviewService.get_due_reviews()
    
    # 获取未来7天的复习计划
    upcoming_reviews = ReviewService.get_upcoming_reviews(days=7)
    
    return render_template('review.html',
                         due_reviews=due_reviews,
                         upcoming_reviews=upcoming_reviews)

@bp.route('/<int:review_id>/mark', methods=['POST'])
def mark_reviewed(review_id):
    """标记已复习"""
    review = ReviewService.mark_reviewed(review_id)
    if review:
        flash('已标记为已复习，下次复习时间已更新', 'success')
    else:
        flash('复习记录不存在', 'danger')
    
    return redirect(url_for('review.index'))
