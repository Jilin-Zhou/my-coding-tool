from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models import AIConfig
from app import db
from app.services.ai_providers import AI_PROVIDERS
from app.services.analyzer import AIAnalyzer

bp = Blueprint('ai_config', __name__, url_prefix='/ai-config')

@bp.route('/')
def settings():
    """AI 设置页面"""
    config = AIConfig.query.filter_by(is_active=True).first()
    return render_template('ai_config/settings.html', 
                          config=config, 
                          providers=AI_PROVIDERS)

@bp.route('/save', methods=['POST'])
def save():
    """保存 AI 配置"""
    provider = request.form.get('provider')
    api_key = request.form.get('api_key')
    model = request.form.get('model')
    base_url = request.form.get('base_url', '').strip()  # 用于 custom 供应商
    
    if not provider or not api_key or not model:
        flash('请填写所有必填字段', 'danger')
        return redirect(url_for('ai_config.settings'))
    
    # 将其他配置设为非活跃
    AIConfig.query.update({'is_active': False})
    
    # 查找或创建配置
    config = AIConfig.query.filter_by(provider=provider).first()
    if config:
        config.api_key = api_key
        config.model = model
        config.base_url = base_url if base_url else None
        config.is_active = True
    else:
        config = AIConfig(
            provider=provider,
            api_key=api_key,
            model=model,
            base_url=base_url if base_url else None,
            is_active=True
        )
        db.session.add(config)
    
    db.session.commit()
    flash('AI 配置已保存！', 'success')
    return redirect(url_for('ai_config.settings'))

@bp.route('/test', methods=['POST'])
def test_connection():
    """测试 API 连接"""
    data = request.get_json()
    provider = data.get('provider')
    api_key = data.get('api_key')
    model = data.get('model')
    base_url = data.get('base_url', '').strip()
    
    if not provider or not api_key or not model:
        return jsonify({'success': False, 'message': '请填写所有必填字段'})
    
    # 创建临时配置进行测试
    class TempConfig:
        pass
    
    temp_config = TempConfig()
    temp_config.provider = provider
    temp_config.api_key = api_key
    temp_config.model = model
    temp_config.base_url = base_url if base_url else None
    
    analyzer = AIAnalyzer(temp_config)
    result = analyzer.test_connection()
    
    return jsonify(result)

@bp.route('/models/<provider>')
def get_models(provider):
    """获取指定供应商的模型列表"""
    if provider in AI_PROVIDERS:
        return jsonify(AI_PROVIDERS[provider]['models'])
    return jsonify([])

@bp.route('/delete', methods=['POST'])
def delete():
    """删除当前 AI 配置"""
    config = AIConfig.query.filter_by(is_active=True).first()
    if config:
        db.session.delete(config)
        db.session.commit()
        flash('AI 配置已删除', 'info')
    return redirect(url_for('ai_config.settings'))
