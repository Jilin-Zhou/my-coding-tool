from flask import Blueprint, render_template, request, jsonify
from app.services.analyzer import HybridAnalyzer

bp = Blueprint('analysis', __name__, url_prefix='/analysis')

@bp.route('/')
def index():
    """智能分析页面"""
    return render_template('analysis.html')

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
    
    analyzer = HybridAnalyzer()
    result = analyzer.analyze(title, description, my_solution, use_ai)
    
    return jsonify(result)
