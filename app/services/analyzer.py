import os
from config import Config

class BasicAnalyzer:
    """基于关键词匹配的基础分析器"""
    
    def __init__(self):
        self.patterns = {
            "双指针": {
                "keywords": ["两数之和", "三数之和", "容器", "接雨水", "回文", "有序数组", "对撞", "快慢指针"],
                "python_functions": ["双指针模板: left, right = 0, len(nums)-1"],
                "templates": ["while left < right:\n    # 根据条件移动指针\n    if condition:\n        left += 1\n    else:\n        right -= 1"]
            },
            "滑动窗口": {
                "keywords": ["子串", "子数组", "连续", "窗口", "最长", "最短", "不重复"],
                "python_functions": ["collections.defaultdict", "collections.Counter"],
                "templates": ["left = 0\nfor right in range(len(s)):\n    # 扩展窗口\n    window[s[right]] += 1\n    while 窗口需要收缩:\n        # 收缩窗口\n        window[s[left]] -= 1\n        left += 1"]
            },
            "二分查找": {
                "keywords": ["查找", "搜索", "有序", "排序", "旋转", "目标值", "log"],
                "python_functions": ["bisect.bisect_left()", "bisect.bisect_right()"],
                "templates": ["left, right = 0, len(nums) - 1\nwhile left <= right:\n    mid = (left + right) // 2\n    if nums[mid] == target:\n        return mid\n    elif nums[mid] < target:\n        left = mid + 1\n    else:\n        right = mid - 1"]
            },
            "动态规划": {
                "keywords": ["最大", "最小", "方案数", "路径", "背包", "子序列", "编辑距离", "最优", "计数"],
                "python_functions": ["@functools.lru_cache", "dp 数组初始化"],
                "templates": ["# 一维DP\ndp = [0] * (n + 1)\nfor i in range(1, n + 1):\n    dp[i] = max(dp[i-1], ...)\n\n# 二维DP\ndp = [[0] * (m + 1) for _ in range(n + 1)]\nfor i in range(1, n + 1):\n    for j in range(1, m + 1):\n        dp[i][j] = ..."]
            },
            "BFS": {
                "keywords": ["最短路径", "层序遍历", "最小步数", "广度优先", "队列"],
                "python_functions": ["collections.deque"],
                "templates": ["from collections import deque\nqueue = deque([start])\nvisited = {start}\nwhile queue:\n    node = queue.popleft()\n    for neighbor in get_neighbors(node):\n        if neighbor not in visited:\n            visited.add(neighbor)\n            queue.append(neighbor)"]
            },
            "DFS/回溯": {
                "keywords": ["全排列", "组合", "子集", "路径总数", "深度优先", "递归", "回溯"],
                "python_functions": ["递归函数", "visited 数组"],
                "templates": ["def dfs(path, ...):\n    if 满足结束条件:\n        result.append(path.copy())\n        return\n    for choice in choices:\n        # 做选择\n        path.append(choice)\n        dfs(path, ...)\n        # 撤销选择\n        path.pop()"]
            },
            "哈希表": {
                "keywords": ["查找", "计数", "频率", "去重", "映射", "字典"],
                "python_functions": ["dict", "collections.Counter", "collections.defaultdict", "set"],
                "templates": ["# Counter 计数\nfrom collections import Counter\ncount = Counter(nums)\n\n# defaultdict 默认值\nfrom collections import defaultdict\nmap = defaultdict(int)\n\n# 普通字典\nmap = {}\nfor num in nums:\n    map[num] = map.get(num, 0) + 1"]
            },
            "栈": {
                "keywords": ["括号", "单调栈", "后进先出", "匹配", "消消乐"],
                "python_functions": ["list 作为栈", "stack.append()", "stack.pop()"],
                "templates": ["stack = []\nfor item in items:\n    if condition:\n        stack.append(item)\n    else:\n        if stack:\n            stack.pop()"]
            },
            "堆/优先队列": {
                "keywords": ["最大k个", "最小k个", "第k大", "中位数", "优先级"],
                "python_functions": ["heapq.heappush()", "heapq.heappop()", "heapq.nlargest()", "heapq.nsmallest()"],
                "templates": ["import heapq\nheap = []\nheapq.heappush(heap, item)\nmin_item = heapq.heappop(heap)\n\n# 最大堆（取负数）\nheapq.heappush(heap, -item)\nmax_item = -heapq.heappop(heap)"]
            },
            "树": {
                "keywords": ["二叉树", "树", "节点", "左右子树", "根节点", "叶子节点"],
                "python_functions": ["递归遍历", "层序遍历(BFS)"],
                "templates": ["# 递归\ndef traverse(root):\n    if not root:\n        return\n    # 前序位置\n    traverse(root.left)\n    # 中序位置\n    traverse(root.right)\n    # 后序位置"]
            },
            "图": {
                "keywords": ["图", "节点", "边", "连通", "环", "拓扑排序", "最短路"],
                "python_functions": ["collections.defaultdict(list)", "visited 集合"],
                "templates": ["# 邻接表表示\ngraph = defaultdict(list)\nfor u, v in edges:\n    graph[u].append(v)\n\n# DFS遍历图\nvisited = set()\ndef dfs(node):\n    if node in visited:\n        return\n    visited.add(node)\n    for neighbor in graph[node]:\n        dfs(neighbor)"]
            },
            "贪心": {
                "keywords": ["最优", "局部最优", "区间", "排序", "选择"],
                "python_functions": ["sorted()", "sort()"],
                "templates": ["# 贪心通用模板\n# 1. 排序\nitems.sort(key=lambda x: x[1])\n# 2. 遍历并做出局部最优选择\nfor item in items:\n    if 满足贪心策略:\n        选择该项"]
            },
            "并查集": {
                "keywords": ["连通性", "合并", "查找", "集合", "朋友圈", "岛屿"],
                "python_functions": ["UnionFind 类"],
                "templates": ["class UnionFind:\n    def __init__(self, n):\n        self.parent = list(range(n))\n    \n    def find(self, x):\n        if self.parent[x] != x:\n            self.parent[x] = self.find(self.parent[x])\n        return self.parent[x]\n    \n    def union(self, x, y):\n        px, py = self.find(x), self.find(y)\n        if px != py:\n            self.parent[px] = py"]
            },
            "字符串处理": {
                "keywords": ["字符串", "字符", "拼接", "分割", "匹配", "KMP"],
                "python_functions": ["str.join()", "str.split()", "str.replace()", "正则表达式"],
                "templates": ["# 字符串常用操作\n# 分割\nwords = s.split()\n# 连接\nresult = ''.join(chars)\n# 字符计数\nfrom collections import Counter\ncount = Counter(s)"]
            }
        }
    
    def analyze(self, title, description):
        """分析题目并返回推荐的算法和函数"""
        text = (title + " " + description).lower()
        
        matches = []
        for algo_type, pattern in self.patterns.items():
            # 检查是否匹配关键词
            if any(keyword in text for keyword in pattern["keywords"]):
                matches.append({
                    "type": algo_type,
                    "functions": pattern["python_functions"],
                    "templates": pattern["templates"]
                })
        
        if not matches:
            return {
                "algorithm_types": ["未识别"],
                "recommended_functions": [],
                "templates": [],
                "analysis_type": "basic"
            }
        
        return {
            "algorithm_types": [m["type"] for m in matches],
            "recommended_functions": [f for m in matches for f in m["functions"]],
            "templates": matches,  # 包含完整信息
            "analysis_type": "basic"
        }

class AIAnalyzer:
    """基于 OpenAI API 的增强分析器"""
    
    def __init__(self):
        self.api_key = Config.OPENAI_API_KEY
        self.model = Config.OPENAI_MODEL
    
    def is_available(self):
        """检查 AI 分析是否可用"""
        return bool(self.api_key)
    
    def analyze(self, title, description, my_solution=""):
        """使用 OpenAI API 分析题目"""
        if not self.is_available():
            return None
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            
            prompt = f"""作为算法专家，请分析以下编程题目：

标题：{title}
描述：{description}
{'我的解答：' + my_solution if my_solution else ''}

请提供：
1. 主要使用的算法/数据结构（如：动态规划、双指针等）
2. 推荐的 Python 函数和库
3. 解题思路要点
4. 时间和空间复杂度分析

请以简洁的中文回答，使用 Markdown 格式。"""
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的算法题目分析助手，擅长分析编程题目并提供解题建议。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return {
                "analysis": response.choices[0].message.content,
                "analysis_type": "ai"
            }
        except Exception as e:
            print(f"AI 分析失败: {e}")
            return None

class HybridAnalyzer:
    """混合分析器：结合基础分析和 AI 分析"""
    
    def __init__(self):
        self.basic_analyzer = BasicAnalyzer()
        self.ai_analyzer = AIAnalyzer()
    
    def analyze(self, title, description, my_solution="", use_ai=False):
        """
        分析题目
        
        Args:
            title: 题目标题
            description: 题目描述
            my_solution: 我的解答（可选）
            use_ai: 是否使用 AI 分析
        
        Returns:
            分析结果字典
        """
        # 总是执行基础分析
        basic_result = self.basic_analyzer.analyze(title, description)
        
        # 如果请求 AI 分析且可用，则尝试 AI 分析
        if use_ai and self.ai_analyzer.is_available():
            ai_result = self.ai_analyzer.analyze(title, description, my_solution)
            if ai_result:
                # 合并基础分析和 AI 分析结果
                return {
                    **basic_result,
                    "ai_analysis": ai_result["analysis"],
                    "analysis_type": "hybrid"
                }
        
        return basic_result
