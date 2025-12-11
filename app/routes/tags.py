from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models import Tag, Problem
from app import db

bp = Blueprint('tags', __name__, url_prefix='/tags')

@bp.route('/')
def list():
    """标签列表"""
    tags = Tag.query.order_by(Tag.name).all()
    
    # 统计每个标签的使用次数
    tag_stats = []
    for tag in tags:
        count = len(tag.problems)
        tag_stats.append({
            'tag': tag,
            'count': count
        })
    
    return render_template('tags/list.html', tag_stats=tag_stats)

@bp.route('/create', methods=['POST'])
def create():
    """创建新标签"""
    name = request.form.get('name')
    color = request.form.get('color', 'primary')
    
    if not name:
        flash('标签名不能为空', 'danger')
        return redirect(url_for('tags.list'))
    
    # 检查是否已存在
    existing = Tag.query.filter_by(name=name).first()
    if existing:
        flash('标签已存在', 'warning')
        return redirect(url_for('tags.list'))
    
    tag = Tag(name=name, color=color)
    db.session.add(tag)
    db.session.commit()
    
    flash('标签创建成功！', 'success')
    return redirect(url_for('tags.list'))

@bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """删除标签"""
    tag = Tag.query.get_or_404(id)
    db.session.delete(tag)
    db.session.commit()
    flash('标签已删除', 'info')
    return redirect(url_for('tags.list'))

@bp.route('/<int:id>/edit', methods=['POST'])
def edit(id):
    """编辑标签"""
    tag = Tag.query.get_or_404(id)
    
    name = request.form.get('name')
    color = request.form.get('color')
    
    if name:
        tag.name = name
    if color:
        tag.color = color
    
    db.session.commit()
    flash('标签更新成功！', 'success')
    return redirect(url_for('tags.list'))
