from datetime import datetime
from app import db

# 多对多关系：题目和标签
problem_tags = db.Table('problem_tags',
    db.Column('problem_id', db.Integer, db.ForeignKey('problem.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

# 多对多关系：题目和函数
problem_functions = db.Table('problem_functions',
    db.Column('problem_id', db.Integer, db.ForeignKey('problem.id'), primary_key=True),
    db.Column('function_id', db.Integer, db.ForeignKey('function.id'), primary_key=True)
)

class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    source = db.Column(db.String(50))  # LeetCode, Codeforces, etc.
    problem_number = db.Column(db.String(20))  # 题号
    difficulty = db.Column(db.String(20))  # Easy, Medium, Hard
    description = db.Column(db.Text)  # 题目描述（支持 Markdown）
    my_thoughts = db.Column(db.Text)  # 我的思路
    my_solution = db.Column(db.Text)  # 我的解答（代码）
    time_complexity = db.Column(db.String(50))  # 时间复杂度
    space_complexity = db.Column(db.String(50))  # 空间复杂度
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    tags = db.relationship('Tag', secondary=problem_tags, lazy='subquery',
                          backref=db.backref('problems', lazy=True))
    functions = db.relationship('Function', secondary=problem_functions, lazy='subquery',
                               backref=db.backref('problems', lazy=True))
    reviews = db.relationship('Review', backref='problem', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Problem {self.title}>'

class Function(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # 函数名
    language = db.Column(db.String(20), default='python')  # 语言：python/java/cpp
    category = db.Column(db.String(50))  # 分类
    syntax = db.Column(db.Text)  # 语法
    description = db.Column(db.Text)  # 描述
    example = db.Column(db.Text)  # 示例代码
    frequency = db.Column(db.Integer, default=0)  # 使用频率
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Function {self.name}>'

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    color = db.Column(db.String(20), default='primary')  # Bootstrap 颜色类
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Tag {self.name}>'

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    problem_id = db.Column(db.Integer, db.ForeignKey('problem.id'), nullable=False)
    next_review_date = db.Column(db.DateTime, nullable=False)
    review_count = db.Column(db.Integer, default=0)
    last_reviewed = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Review for Problem {self.problem_id}>'
