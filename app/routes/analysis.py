from flask import Blueprint, render_template, request, jsonify
from app.services.analyzer import HybridAnalyzer
from app.models import AIConfig

bp = Blueprint('analysis', __name__, url_prefix='/analysis')

@bp.route('/')
def index():
    """智能分析页面"""
    # 获取当前活跃的 AI 配置
    ai_config = AIConfig.query.filter_by(is_active=True).first()
    return render_template('analysis.html', ai_config=ai_config)

@bp.route('/analyze', methods=['POST'])
def analyze():
    """执行题目分析"""
    data = request.get_json()
    
    title = data.get('title', '')
    description = data.get('description', '')
    my_solution = data.get('my_solution', '')
    use_ai = data.get('use_ai', False)
    
    if not title and not description:
        return jsonify({'error': '请提供题目标题或描述'}), 400
    
    # 获取当前活跃的 AI 配置
    ai_config = AIConfig.query.filter_by(is_active=True).first()
    
    # 如果请求使用 AI 但没有配置，返回提示
    if use_ai and not ai_config:
        return jsonify({'error': '请先配置 AI 供应商和 API Key', 'redirect': '/ai-config/'}), 400
    
    analyzer = HybridAnalyzer(ai_config)
    result = analyzer.analyze(title, description, my_solution, use_ai)
    
    return jsonify(result)
