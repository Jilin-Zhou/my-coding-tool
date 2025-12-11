from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models import Problem, Tag, Function
from app import db
from app.services.review import ReviewService
from app.services.code_parser import CodeParser
import markdown

bp = Blueprint('problems', __name__, url_prefix='/problems')

@bp.route('/')
def list():
    """题目列表"""
    # 获取筛选参数
    difficulty = request.args.get('difficulty')
    source = request.args.get('source')
    tag_id = request.args.get('tag')
    search = request.args.get('search')
    
    # 构建查询
    query = Problem.query
    
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    
    if source:
        query = query.filter_by(source=source)
    
    if tag_id:
        tag = Tag.query.get(tag_id)
        if tag:
            query = query.filter(Problem.tags.contains(tag))
    
    if search:
        search_pattern = f'%{search}%'
        query = query.filter(
            db.or_(
                Problem.title.like(search_pattern),
                Problem.description.like(search_pattern)
            )
        )
    
    problems = query.order_by(Problem.created_at.desc()).all()
    
    # 获取所有标签和来源用于筛选
    all_tags = Tag.query.all()
    all_sources = db.session.query(Problem.source).distinct().all()
    all_sources = [s[0] for s in all_sources if s[0]]
    
    return render_template('problems/list.html',
                         problems=problems,
                         all_tags=all_tags,
                         all_sources=all_sources,
                         current_difficulty=difficulty,
                         current_source=source,
                         current_tag=tag_id,
                         current_search=search)

@bp.route('/<int:id>')
def detail(id):
    """题目详情"""
    problem = Problem.query.get_or_404(id)
    
    # 将 Markdown 转换为 HTML
    if problem.description:
        problem.description_html = markdown.markdown(problem.description, extensions=['fenced_code', 'codehilite'])
    else:
        problem.description_html = ''
    
    if problem.my_thoughts:
        problem.my_thoughts_html = markdown.markdown(problem.my_thoughts, extensions=['fenced_code', 'codehilite'])
    else:
        problem.my_thoughts_html = ''
    
    return render_template('problems/detail.html', problem=problem)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    """创建新题目"""
    if request.method == 'POST':
        # 获取表单数据
        title = request.form.get('title')
        source = request.form.get('source')
        problem_number = request.form.get('problem_number')
        difficulty = request.form.get('difficulty')
        description = request.form.get('description')
        my_thoughts = request.form.get('my_thoughts')
        my_solution = request.form.get('my_solution')
        time_complexity = request.form.get('time_complexity')
        space_complexity = request.form.get('space_complexity')
        tag_ids = request.form.getlist('tags')
        function_ids = request.form.getlist('functions')
        
        # 验证必填字段
        if not title:
            flash('标题不能为空', 'danger')
            return redirect(url_for('problems.create'))
        
        # 创建题目
        problem = Problem(
            title=title,
            source=source,
            problem_number=problem_number,
            difficulty=difficulty,
            description=description,
            my_thoughts=my_thoughts,
            my_solution=my_solution,
            time_complexity=time_complexity,
            space_complexity=space_complexity
        )
        
        # 添加标签
        for tag_id in tag_ids:
            tag = Tag.query.get(tag_id)
            if tag:
                problem.tags.append(tag)
        
        # 添加函数关联
        if function_ids:
            functions = Function.query.filter(Function.id.in_(function_ids)).all()
            for function in functions:
                problem.functions.append(function)
                # 增加函数使用频率
                function.frequency += 1
        
        db.session.add(problem)
        db.session.commit()
        
        # 创建复习计划
        ReviewService.create_review_schedule(problem.id)
        
        flash('题目添加成功！', 'success')
        return redirect(url_for('problems.detail', id=problem.id))
    
    # GET 请求，显示表单
    all_tags = Tag.query.all()
    all_functions = Function.query.filter_by(language='python').order_by(Function.category, Function.name).all()
    return render_template('problems/create.html', all_tags=all_tags, all_functions=all_functions)

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    """编辑题目"""
    problem = Problem.query.get_or_404(id)
    
    if request.method == 'POST':
        # 更新题目信息
        problem.title = request.form.get('title')
        problem.source = request.form.get('source')
        problem.problem_number = request.form.get('problem_number')
        problem.difficulty = request.form.get('difficulty')
        problem.description = request.form.get('description')
        problem.my_thoughts = request.form.get('my_thoughts')
        problem.my_solution = request.form.get('my_solution')
        problem.time_complexity = request.form.get('time_complexity')
        problem.space_complexity = request.form.get('space_complexity')
        
        # 更新标签
        tag_ids = request.form.getlist('tags')
        problem.tags = []
        for tag_id in tag_ids:
            tag = Tag.query.get(tag_id)
            if tag:
                problem.tags.append(tag)
        
        # 更新函数关联
        function_ids = request.form.getlist('functions')
        old_functions = set(f.id for f in problem.functions)
        new_functions = set(int(fid) for fid in function_ids)
        
        # 减少移除函数的频率
        removed_functions = old_functions - new_functions
        if removed_functions:
            removed_funcs = Function.query.filter(Function.id.in_(removed_functions)).all()
            for func in removed_funcs:
                if func.frequency > 0:
                    func.frequency -= 1
        
        # 增加新添加函数的频率
        added_functions = new_functions - old_functions
        if added_functions:
            added_funcs = Function.query.filter(Function.id.in_(added_functions)).all()
            for func in added_funcs:
                func.frequency += 1
        
        # 更新关联
        problem.functions = []
        if function_ids:
            functions = Function.query.filter(Function.id.in_(new_functions)).all()
            for func in functions:
                problem.functions.append(func)
        
        db.session.commit()
        flash('题目更新成功！', 'success')
        return redirect(url_for('problems.detail', id=problem.id))
    
    # GET 请求，显示编辑表单
    all_tags = Tag.query.all()
    all_functions = Function.query.filter_by(language='python').order_by(Function.category, Function.name).all()
    return render_template('problems/edit.html', problem=problem, all_tags=all_tags, all_functions=all_functions)

@bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """删除题目"""
    problem = Problem.query.get_or_404(id)
    db.session.delete(problem)
    db.session.commit()
    flash('题目已删除', 'info')
    return redirect(url_for('problems.list'))

@bp.route('/parse-code', methods=['POST'])
def parse_code():
    """解析代码，提取使用的函数"""
    code = request.json.get('code', '')
    parser = CodeParser()
    suggestions = parser.get_function_suggestions(code)
    
    # 检查每个函数是否已在库中
    for suggestion in suggestions:
        existing = Function.query.filter_by(
            name=suggestion['name'], 
            language='python'
        ).first()
        suggestion['in_library'] = existing is not None
        suggestion['function_id'] = existing.id if existing else None
    
    return jsonify({'success': True, 'suggestions': suggestions})
