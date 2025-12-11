"""
Python 代码解析器
自动从用户的解答代码中提取使用的函数和模块
"""
import re


class CodeParser:
    # 常见的刷题高频模块和函数映射
    KNOWN_FUNCTIONS = {
        'collections': ['Counter', 'defaultdict', 'deque', 'OrderedDict'],
        'heapq': ['heappush', 'heappop', 'heapify', 'nlargest', 'nsmallest'],
        'bisect': ['bisect_left', 'bisect_right', 'insort', 'insort_left'],
        'functools': ['lru_cache', 'reduce', 'cache'],
        'itertools': ['permutations', 'combinations', 'product', 'accumulate', 'groupby'],
        'math': ['gcd', 'lcm', 'inf', 'sqrt', 'ceil', 'floor'],
        'string': ['ascii_lowercase', 'ascii_uppercase', 'digits'],
        'operator': ['itemgetter', 'attrgetter'],
        're': ['match', 'search', 'findall', 'sub'],
    }
    
    def parse(self, code: str) -> dict:
        """
        解析代码，提取使用的函数
        返回: {'imports': [...], 'functions': [...], 'builtins': [...]}
        """
        result = {
            'imports': [],      # 导入的模块
            'functions': [],    # 使用的函数（带模块名）
            'builtins': []      # 使用的内置函数
        }
        
        # 1. 解析 import 语句
        import_patterns = [
            r'from\s+([\w.]+)\s+import\s+(.+)',  # from xxx import yyy
            r'import\s+([\w.]+)',                 # import xxx
        ]
        
        for pattern in import_patterns:
            matches = re.findall(pattern, code)
            for match in matches:
                if isinstance(match, tuple):
                    module, items = match
                    for item in items.split(','):
                        item = item.strip().split(' as ')[0].strip()
                        if item and item != '*':
                            func_name = f"{module}.{item}"
                            result['functions'].append(func_name)
                            if module not in result['imports']:
                                result['imports'].append(module)
                else:
                    if match not in result['imports']:
                        result['imports'].append(match)
        
        # 2. 检测常见内置函数
        builtin_functions = [
            'sorted', 'sort', 'enumerate', 'zip', 'map', 'filter',
            'sum', 'max', 'min', 'abs', 'len', 'range', 'reversed',
            'any', 'all', 'isinstance', 'list', 'dict', 'set', 'tuple'
        ]
        
        for func in builtin_functions:
            if re.search(rf'\b{func}\s*\(', code):
                if func not in result['builtins']:
                    result['builtins'].append(func)
        
        # 3. 检测特殊语法
        # 列表推导式
        if re.search(r'\[.+\s+for\s+.+\s+in\s+.+\]', code):
            if '列表推导式' not in result['builtins']:
                result['builtins'].append('列表推导式')
        
        # 字典推导式
        if re.search(r'\{.+:.+\s+for\s+.+\s+in\s+.+\}', code):
            if '字典推导式' not in result['builtins']:
                result['builtins'].append('字典推导式')
        
        # lambda
        if 'lambda' in code:
            if 'lambda' not in result['builtins']:
                result['builtins'].append('lambda')
        
        return result
    
    def get_function_suggestions(self, code: str) -> list:
        """
        返回建议添加到函数库的函数列表
        格式: [{'name': 'xxx', 'category': 'xxx', 'source': 'xxx'}, ...]
        """
        parsed = self.parse(code)
        suggestions = []
        seen = set()
        
        # 处理导入的函数
        for func in parsed['functions']:
            if func not in seen:
                suggestions.append({
                    'name': func,
                    'category': self._guess_category(func),
                    'source': 'import'
                })
                seen.add(func)
        
        # 处理内置函数
        for func in parsed['builtins']:
            if func not in seen:
                suggestions.append({
                    'name': func,
                    'category': '内置函数',
                    'source': 'builtin'
                })
                seen.add(func)
        
        return suggestions
    
    def _guess_category(self, func_name: str) -> str:
        """根据函数名猜测分类"""
        module = func_name.split('.')[0] if '.' in func_name else ''
        
        category_map = {
            'collections': '哈希/队列',
            'heapq': '堆',
            'bisect': '二分',
            'functools': '缓存',
            'itertools': '迭代',
            'math': '数学',
            're': '正则表达式',
            'string': '字符串',
            'operator': '运算符',
        }
        
        return category_map.get(module, '其他')
