"""
This example demonstrates the justify and justify_headers arguments in Markdown.
"""

from rich.console import Console
from rich.markdown import Markdown

console = Console(width=60)

markdown_content = """
# Main Title

This is a paragraph under the main title. The justification of this paragraph and the header can be controlled independently.

## Section Title

This is another paragraph that demonstrates how different justification settings can create different visual layouts.

### Subsection Title

Final paragraph showing the combined effect of paragraph and header justification settings.
"""

print("=== Default justification (headers: center, paragraphs: left) ===")
md_default = Markdown(markdown_content)
console.print(md_default)
print()

print("=== Left-justified headers, center-justified paragraphs ===")
md_left_center = Markdown(markdown_content, justify="center", justify_headers="left")
console.print(md_left_center)
print()

print("=== Right-justified headers, right-justified paragraphs ===")
md_right_right = Markdown(markdown_content, justify="right", justify_headers="right")
console.print(md_right_right)
print()

print("=== Center-justified headers, left-justified paragraphs ===")
md_center_left = Markdown(markdown_content, justify="left", justify_headers="center")
console.print(md_center_left)
print()
