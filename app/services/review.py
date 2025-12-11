from datetime import datetime, timedelta
from app.models import Review, Problem
from app import db

class ReviewService:
    """复习提醒服务 - 基于艾宾浩斯遗忘曲线"""
    
    # 艾宾浩斯遗忘曲线复习间隔（天）
    REVIEW_INTERVALS = [1, 2, 4, 7, 15, 30]
    
    @staticmethod
    def create_review_schedule(problem_id):
        """为新题目创建复习计划"""
        # 检查是否已存在复习计划
        existing = Review.query.filter_by(problem_id=problem_id).first()
        if existing:
            return existing
        
        # 创建新的复习计划，第一次复习为明天
        next_review = datetime.utcnow() + timedelta(days=ReviewService.REVIEW_INTERVALS[0])
        review = Review(
            problem_id=problem_id,
            next_review_date=next_review,
            review_count=0
        )
        db.session.add(review)
        db.session.commit()
        return review
    
    @staticmethod
    def mark_reviewed(review_id):
        """标记题目已复习，更新下次复习时间"""
        review = Review.query.get(review_id)
        if not review:
            return None
        
        review.last_reviewed = datetime.utcnow()
        review.review_count += 1
        
        # 计算下次复习时间
        if review.review_count < len(ReviewService.REVIEW_INTERVALS):
            days = ReviewService.REVIEW_INTERVALS[review.review_count]
        else:
            # 超过预定义间隔后，每30天复习一次
            days = 30
        
        review.next_review_date = datetime.utcnow() + timedelta(days=days)
        db.session.commit()
        return review
    
    @staticmethod
    def get_due_reviews():
        """获取需要复习的题目列表"""
        now = datetime.utcnow()
        due_reviews = Review.query.filter(Review.next_review_date <= now).all()
        
        results = []
        for review in due_reviews:
            problem = Problem.query.get(review.problem_id)
            if problem:
                results.append({
                    'review_id': review.id,
                    'problem': problem,
                    'review_count': review.review_count,
                    'next_review_date': review.next_review_date,
                    'last_reviewed': review.last_reviewed
                })
        
        return results
    
    @staticmethod
    def get_upcoming_reviews(days=7):
        """获取未来几天需要复习的题目"""
        now = datetime.utcnow()
        future = now + timedelta(days=days)
        
        upcoming = Review.query.filter(
            Review.next_review_date > now,
            Review.next_review_date <= future
        ).order_by(Review.next_review_date).all()
        
        results = []
        for review in upcoming:
            problem = Problem.query.get(review.problem_id)
            if problem:
                results.append({
                    'review_id': review.id,
                    'problem': problem,
                    'review_count': review.review_count,
                    'next_review_date': review.next_review_date,
                    'last_reviewed': review.last_reviewed
                })
        
        return results
