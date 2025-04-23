import pytest
from rich.math_render import MathRenderer
from rich.markdown import Markdown
from rich.console import Console
from rich.text import Text
from rich.style import Style
from io import StringIO

def test_math_renderer_symbols():
    """Test that the math renderer correctly converts LaTeX symbols to Unicode."""
    renderer = MathRenderer()
    
    # Test Greek letters
    assert renderer.render_expression("\\alpha") == "α"
    assert renderer.render_expression("\\beta") == "β"
    assert renderer.render_expression("\\gamma") == "γ"
    
    # Test operators
    assert renderer.render_expression("\\times") == "×"
    assert renderer.render_expression("\\leq") == "≤"
    assert renderer.render_expression("\\geq") == "≥"
    
    # Test compound expressions
    assert renderer.render_expression("a\\times b") == "a×b"

def test_math_renderer_superscripts():
    """Test that the math renderer correctly handles superscripts."""
    renderer = MathRenderer()
    
    # Test simple superscripts
    assert "²" in renderer.render_expression("x^2")
    assert "²" in renderer.render_expression("x^{2}")
    
    # Test compound superscripts
    result = renderer.render_expression("x^{23}")
    assert "²³" in result

def test_math_inline_markdown():
    """Test that inline math expressions work in markdown."""
    console = Console(file=StringIO(), width=100)
    
    markdown = Markdown("This is an inline expression $E = mc^2$ in text.")
    console.print(markdown)
    output = console.file.getvalue()
    
    # Check that the expression is rendered with spacing preserved
    assert "E = mc²" in output  
    assert "expression" in output
    assert "in text" in output

def test_space_normalization():
    """Test that space normalization handles different operators correctly."""
    renderer = MathRenderer()
    
    # Test that equals preserves spaces
    assert renderer.render_expression("E = mc^2") == "E = mc²"
    assert renderer.render_expression("y = x + 3") == "y = x + 3"
    
    # Test that multiplication removes spaces
    assert renderer.render_expression("a × b") == "a×b"
    assert renderer.render_expression("a\\times b") == "a×b"
    
    # Test mixed operators
    assert renderer.render_expression("F = m × a") == "F = m×a"

def test_complex_expressions():
    """Test more complex mathematical expressions."""
    renderer = MathRenderer()
    
    # Test complex equation with multiple operators
    result = renderer.render_expression("f(x) = x^2 + 2\\times x + 1")
    assert result == "f(x) = x² + 2×x + 1"
    
    # Test Greek letters with spaces
    result = renderer.render_expression("\\alpha = \\beta + \\gamma")
    assert result == "α = β + γ"