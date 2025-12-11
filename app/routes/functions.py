from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models import Function
from app import db

bp = Blueprint('functions', __name__, url_prefix='/functions')

@bp.route('/')
def list():
    """函数库列表"""
    # 获取筛选参数
    language = request.args.get('language', 'python')
    category = request.args.get('category')
    sort_by = request.args.get('sort', 'category')  # category, frequency, name
    
    # 构建查询
    query = Function.query.filter_by(language=language)
    
    if category:
        query = query.filter_by(category=category)
    
    # 排序
    if sort_by == 'frequency':
        query = query.order_by(Function.frequency.desc())
    elif sort_by == 'name':
        query = query.order_by(Function.name)
    else:
        query = query.order_by(Function.category, Function.name)
    
    functions = query.all()
    
    # 获取所有分类
    categories = db.session.query(Function.category).filter_by(
        language=language
    ).distinct().all()
    categories = [c[0] for c in categories if c[0]]
    
    return render_template('functions/list.html',
                         functions=functions,
                         categories=categories,
                         current_language=language,
                         current_category=category,
                         current_sort=sort_by)

@bp.route('/<int:id>')
def detail(id):
    """函数详情"""
    function = Function.query.get_or_404(id)
    return render_template('functions/detail.html', function=function)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    """添加自定义函数"""
    if request.method == 'POST':
        name = request.form.get('name')
        language = request.form.get('language', 'python')
        category = request.form.get('category')
        syntax = request.form.get('syntax')
        description = request.form.get('description')
        example = request.form.get('example')
        
        if not name:
            flash('函数名不能为空', 'danger')
            return redirect(url_for('functions.create'))
        
        function = Function(
            name=name,
            language=language,
            category=category,
            syntax=syntax,
            description=description,
            example=example
        )
        
        db.session.add(function)
        db.session.commit()
        
        flash('函数添加成功！', 'success')
        return redirect(url_for('functions.detail', id=function.id))
    
    return render_template('functions/create.html')

@bp.route('/<int:id>/increment', methods=['POST'])
def increment_frequency(id):
    """增加函数使用频率"""
    function = Function.query.get_or_404(id)
    function.frequency += 1
    db.session.commit()
    return jsonify({'success': True, 'frequency': function.frequency})
