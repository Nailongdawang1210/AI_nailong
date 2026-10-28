import sys
from pathlib import Path

# 把项目根目录加进模块搜索路径，这样无论从哪个目录、用哪种方式运行都能 import 到 agent 包
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent import def1  # noqa: E402  （必须在 sys.path 处理之后导入）

print(def1.LOVE)
