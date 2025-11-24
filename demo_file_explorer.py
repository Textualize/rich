from rich.console import Console
from rich.panel import Panel
from rich.file_explorer import FileExplorer  # 방금 만든 모듈

console = Console()

# 1. 현재 디렉토리(.) 탐색
console.print(Panel(FileExplorer("."), title="📂 현재 프로젝트 구조", border_style="blue"))

# 2. 특정 폴더 무시하고 탐색 (예: __pycache__, .git)
# ignore_list = [".git", "__pycache__", ".vscode"]
# console.print(Panel(FileExplorer(".", ignore=ignore_list), title="Clean View", border_style="green"))
