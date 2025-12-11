"""
数据库初始化脚本
初始化数据库并添加预置的 Python 高频函数
"""

from app import create_app, db
from app.models import Function
from datetime import datetime

# 预置的 Python 高频函数数据
PRESET_FUNCTIONS = [
    # 排序
    {
        'name': 'sorted()',
        'language': 'python',
        'category': '排序',
        'syntax': 'sorted(iterable, key=None, reverse=False)',
        'description': '返回排序后的新列表，不改变原列表',
        'example': '# 基本排序\nnums = [3, 1, 4, 1, 5]\nsorted_nums = sorted(nums)  # [1, 1, 3, 4, 5]\n\n# 自定义排序\nstudents = [(\'Alice\', 25), (\'Bob\', 20)]\nsorted_students = sorted(students, key=lambda x: x[1])  # 按年龄排序'
    },
    {
        'name': 'list.sort()',
        'language': 'python',
        'category': '排序',
        'syntax': 'list.sort(key=None, reverse=False)',
        'description': '原地排序列表，改变原列表',
        'example': 'nums = [3, 1, 4, 1, 5]\nnums.sort()  # nums 变为 [1, 1, 3, 4, 5]\n\n# 降序排序\nnums.sort(reverse=True)'
    },
    # 哈希
    {
        'name': 'collections.Counter',
        'language': 'python',
        'category': '哈希',
        'syntax': 'Counter(iterable)',
        'description': '计数器，统计元素频率',
        'example': 'from collections import Counter\n\nnums = [1, 2, 2, 3, 3, 3]\ncount = Counter(nums)  # Counter({3: 3, 2: 2, 1: 1})\n\n# 最常见的元素\nmost_common = count.most_common(2)  # [(3, 3), (2, 2)]'
    },
    {
        'name': 'collections.defaultdict',
        'language': 'python',
        'category': '哈希',
        'syntax': 'defaultdict(default_factory)',
        'description': '带默认值的字典',
        'example': 'from collections import defaultdict\n\n# 默认值为 int (0)\ncount = defaultdict(int)\nfor num in [1, 2, 2, 3]:\n    count[num] += 1\n\n# 默认值为 list\ngraph = defaultdict(list)\ngraph[1].append(2)'
    },
    # 堆
    {
        'name': 'heapq.heappush()',
        'language': 'python',
        'category': '堆',
        'syntax': 'heapq.heappush(heap, item)',
        'description': '将元素推入堆（最小堆）',
        'example': 'import heapq\n\nheap = []\nheapq.heappush(heap, 3)\nheapq.heappush(heap, 1)\nheapq.heappush(heap, 2)\nprint(heap[0])  # 1 (最小元素)'
    },
    {
        'name': 'heapq.heappop()',
        'language': 'python',
        'category': '堆',
        'syntax': 'heapq.heappop(heap)',
        'description': '弹出堆顶最小元素',
        'example': 'import heapq\n\nheap = [1, 2, 3]\nmin_item = heapq.heappop(heap)  # 1\nprint(heap)  # [2, 3]'
    },
    {
        'name': 'heapq.nlargest()',
        'language': 'python',
        'category': '堆',
        'syntax': 'heapq.nlargest(n, iterable, key=None)',
        'description': '返回最大的 n 个元素',
        'example': 'import heapq\n\nnums = [1, 8, 2, 23, 7]\ntop3 = heapq.nlargest(3, nums)  # [23, 8, 7]'
    },
    {
        'name': 'heapq.nsmallest()',
        'language': 'python',
        'category': '堆',
        'syntax': 'heapq.nsmallest(n, iterable, key=None)',
        'description': '返回最小的 n 个元素',
        'example': 'import heapq\n\nnums = [1, 8, 2, 23, 7]\nbottom3 = heapq.nsmallest(3, nums)  # [1, 2, 7]'
    },
    # 队列
    {
        'name': 'collections.deque',
        'language': 'python',
        'category': '队列',
        'syntax': 'deque(iterable, maxlen=None)',
        'description': '双端队列，O(1) 时间复杂度的两端操作',
        'example': 'from collections import deque\n\nq = deque([1, 2, 3])\nq.append(4)      # 右侧添加\nq.appendleft(0)  # 左侧添加\nq.pop()          # 右侧弹出\nq.popleft()      # 左侧弹出'
    },
    # 二分
    {
        'name': 'bisect.bisect_left()',
        'language': 'python',
        'category': '二分',
        'syntax': 'bisect_left(a, x, lo=0, hi=len(a))',
        'description': '在有序列表中查找插入点（左侧）',
        'example': 'import bisect\n\nnums = [1, 3, 3, 5]\nidx = bisect.bisect_left(nums, 3)  # 1\n# 插入位置使得所有 v < x 在左边'
    },
    {
        'name': 'bisect.bisect_right()',
        'language': 'python',
        'category': '二分',
        'syntax': 'bisect_right(a, x, lo=0, hi=len(a))',
        'description': '在有序列表中查找插入点（右侧）',
        'example': 'import bisect\n\nnums = [1, 3, 3, 5]\nidx = bisect.bisect_right(nums, 3)  # 3\n# 插入位置使得所有 v <= x 在左边'
    },
    {
        'name': 'bisect.insort()',
        'language': 'python',
        'category': '二分',
        'syntax': 'bisect.insort(a, x)',
        'description': '在有序列表中插入元素并保持有序',
        'example': 'import bisect\n\nnums = [1, 3, 5]\nbisect.insort(nums, 4)\nprint(nums)  # [1, 3, 4, 5]'
    },
    # 缓存
    {
        'name': '@functools.lru_cache',
        'language': 'python',
        'category': '缓存',
        'syntax': '@lru_cache(maxsize=None)',
        'description': '记忆化装饰器，缓存函数调用结果',
        'example': 'from functools import lru_cache\n\n@lru_cache(maxsize=None)\ndef fib(n):\n    if n < 2:\n        return n\n    return fib(n-1) + fib(n-2)\n\nprint(fib(100))  # 快速计算'
    },
    # 迭代
    {
        'name': 'itertools.permutations()',
        'language': 'python',
        'category': '迭代',
        'syntax': 'permutations(iterable, r=None)',
        'description': '生成全排列',
        'example': 'from itertools import permutations\n\nperms = list(permutations([1, 2, 3]))\n# [(1,2,3), (1,3,2), (2,1,3), (2,3,1), (3,1,2), (3,2,1)]\n\n# 指定长度\nperms2 = list(permutations([1,2,3], 2))\n# [(1,2), (1,3), (2,1), (2,3), (3,1), (3,2)]'
    },
    {
        'name': 'itertools.combinations()',
        'language': 'python',
        'category': '迭代',
        'syntax': 'combinations(iterable, r)',
        'description': '生成组合',
        'example': 'from itertools import combinations\n\ncombs = list(combinations([1, 2, 3], 2))\n# [(1, 2), (1, 3), (2, 3)]'
    },
    {
        'name': 'itertools.product()',
        'language': 'python',
        'category': '迭代',
        'syntax': 'product(*iterables, repeat=1)',
        'description': '生成笛卡尔积',
        'example': 'from itertools import product\n\nprods = list(product([1, 2], [3, 4]))\n# [(1, 3), (1, 4), (2, 3), (2, 4)]\n\n# 自身笛卡尔积\nprods2 = list(product([0, 1], repeat=3))\n# 所有长度为3的二进制序列'
    },
    {
        'name': 'itertools.accumulate()',
        'language': 'python',
        'category': '迭代',
        'syntax': 'accumulate(iterable, func=operator.add)',
        'description': '累积计算，常用于前缀和',
        'example': 'from itertools import accumulate\nimport operator\n\nnums = [1, 2, 3, 4]\nprefix_sum = list(accumulate(nums))  # [1, 3, 6, 10]\n\n# 前缀积\nprefix_prod = list(accumulate(nums, operator.mul))  # [1, 2, 6, 24]'
    },
    # 字符串
    {
        'name': 'str.join()',
        'language': 'python',
        'category': '字符串',
        'syntax': 'separator.join(iterable)',
        'description': '用分隔符连接字符串',
        'example': 'words = [\'hello\', \'world\']\nsentence = \' \'.join(words)  # \'hello world\'\n\nchars = [\'a\', \'b\', \'c\']\nstring = \'\'.join(chars)  # \'abc\''
    },
    {
        'name': 'str.split()',
        'language': 'python',
        'category': '字符串',
        'syntax': 'str.split(sep=None, maxsplit=-1)',
        'description': '分割字符串',
        'example': 'sentence = \'hello world\'\nwords = sentence.split()  # [\'hello\', \'world\']\n\ndata = \'a,b,c\'\nparts = data.split(\',\')  # [\'a\', \'b\', \'c\']'
    },
    # 集合
    {
        'name': 'set operations',
        'language': 'python',
        'category': '集合',
        'syntax': 'set1 & set2, set1 | set2, set1 - set2',
        'description': '集合交并差运算',
        'example': 's1 = {1, 2, 3}\ns2 = {2, 3, 4}\n\nintersection = s1 & s2  # {2, 3}\nunion = s1 | s2         # {1, 2, 3, 4}\ndifference = s1 - s2    # {1}'
    },
    # 数学
    {
        'name': 'math.gcd()',
        'language': 'python',
        'category': '数学',
        'syntax': 'math.gcd(a, b)',
        'description': '计算最大公约数',
        'example': 'import math\n\ngcd = math.gcd(12, 18)  # 6\ngcd_multi = math.gcd(math.gcd(12, 18), 24)  # 多个数的GCD'
    },
    {
        'name': 'math.lcm()',
        'language': 'python',
        'category': '数学',
        'syntax': 'math.lcm(a, b)',
        'description': '计算最小公倍数（Python 3.9+）',
        'example': 'import math\n\nlcm = math.lcm(12, 18)  # 36'
    },
    {
        'name': 'math.inf',
        'language': 'python',
        'category': '数学',
        'syntax': 'float(\'inf\') 或 math.inf',
        'description': '表示无穷大',
        'example': 'import math\n\nmin_val = math.inf\nmax_val = -math.inf\n\n# 用于初始化最小/最大值\nfor num in nums:\n    min_val = min(min_val, num)'
    }
]

def init_database():
    """初始化数据库"""
    app = create_app()
    
    with app.app_context():
        # 删除所有表并重新创建
        print("创建数据库表...")
        db.drop_all()
        db.create_all()
        
        # 添加预置函数
        print("添加预置 Python 高频函数...")
        for func_data in PRESET_FUNCTIONS:
            function = Function(**func_data)
            db.session.add(function)
        
        db.session.commit()
        print(f"成功添加 {len(PRESET_FUNCTIONS)} 个预置函数！")
        
        print("\n数据库初始化完成！")
        print("运行 'python run.py' 启动应用")

if __name__ == '__main__':
    init_database()
