"""
AI 供应商配置
"""

AI_PROVIDERS = {
    'openai': {
        'name': 'OpenAI',
        'base_url': 'https://api.openai.com/v1',
        'models': [
            {'id': 'gpt-4o', 'name': 'GPT-4o (推荐)', 'description': '最强大，速度快'},
            {'id': 'gpt-4o-mini', 'name': 'GPT-4o Mini', 'description': '性价比高'},
            {'id': 'gpt-4-turbo', 'name': 'GPT-4 Turbo', 'description': '强大但较慢'},
            {'id': 'gpt-3.5-turbo', 'name': 'GPT-3.5 Turbo', 'description': '经济实惠'},
        ],
        'api_key_placeholder': 'sk-...',
        'api_key_help': '从 https://platform.openai.com/api-keys 获取'
    },
    'gemini': {
        'name': 'Google Gemini',
        'base_url': 'https://generativelanguage.googleapis.com/v1beta',
        'models': [
            {'id': 'gemini-1.5-pro', 'name': 'Gemini 1.5 Pro', 'description': '最强大'},
            {'id': 'gemini-1.5-flash', 'name': 'Gemini 1.5 Flash', 'description': '快速响应'},
            {'id': 'gemini-1.0-pro', 'name': 'Gemini 1.0 Pro', 'description': '稳定可靠'},
        ],
        'api_key_placeholder': 'AIza...',
        'api_key_help': '从 https://aistudio.google.com/apikey 获取'
    },
    'openrouter': {
        'name': 'OpenRouter',
        'base_url': 'https://openrouter.ai/api/v1',
        'models': [
            {'id': 'anthropic/claude-3.5-sonnet', 'name': 'Claude 3.5 Sonnet', 'description': '强大的编程助手'},
            {'id': 'anthropic/claude-3-haiku', 'name': 'Claude 3 Haiku', 'description': '快速经济'},
            {'id': 'openai/gpt-4o', 'name': 'GPT-4o (via OpenRouter)', 'description': 'OpenAI 模型'},
            {'id': 'openai/gpt-4o-mini', 'name': 'GPT-4o Mini (via OpenRouter)', 'description': '经济实惠'},
            {'id': 'google/gemini-pro-1.5', 'name': 'Gemini Pro 1.5', 'description': 'Google 模型'},
            {'id': 'meta-llama/llama-3.1-70b-instruct', 'name': 'Llama 3.1 70B', 'description': '开源强模型'},
            {'id': 'deepseek/deepseek-chat', 'name': 'DeepSeek Chat', 'description': '性价比高'},
        ],
        'api_key_placeholder': 'sk-or-...',
        'api_key_help': '从 https://openrouter.ai/keys 获取'
    },
    'custom': {
        'name': '自定义 (OpenAI 兼容)',
        'base_url': '',  # 用户自定义
        'models': [],  # 用户自定义
        'api_key_placeholder': '',
        'api_key_help': '输入兼容 OpenAI API 的服务端点',
        'allow_custom_url': True,
        'allow_custom_model': True
    }
}
