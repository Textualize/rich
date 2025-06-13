from typing import Dict, List, Optional, Union, Tuple, Pattern
import re
from rich.text import Text
from rich.style import Style


class MathRenderer:
    """Renders LaTeX-style math expressions as Unicode text."""

    def __init__(self) -> None:
        """Initialize the math renderer with symbol mappings."""
        # Symbol mappings for LaTeX commands to Unicode
        self.symbols: Dict[str, str] = {
            # Greek letters
            "\\alpha": "α",
            "\\beta": "β",
            "\\gamma": "γ",
            "\\delta": "δ",
            "\\epsilon": "ε",
            "\\zeta": "ζ",
            "\\eta": "η",
            "\\theta": "θ",
            "\\iota": "ι",
            "\\kappa": "κ",
            "\\lambda": "λ",
            "\\mu": "μ",
            "\\nu": "ν",
            "\\xi": "ξ",
            "\\pi": "π",
            "\\rho": "ρ",
            "\\sigma": "σ",
            "\\tau": "τ",
            "\\upsilon": "υ",
            "\\phi": "φ",
            "\\chi": "χ",
            "\\psi": "ψ",
            "\\omega": "ω",
            # Uppercase Greek letters
            "\\Alpha": "Α",
            "\\Beta": "Β",
            "\\Gamma": "Γ",
            "\\Delta": "Δ",
            "\\Epsilon": "Ε",
            "\\Zeta": "Ζ",
            "\\Eta": "Η",
            "\\Theta": "Θ",
            "\\Iota": "Ι",
            "\\Kappa": "Κ",
            "\\Lambda": "Λ",
            "\\Mu": "Μ",
            "\\Nu": "Ν",
            "\\Xi": "Ξ",
            "\\Pi": "Π",
            "\\Rho": "Ρ",
            "\\Sigma": "Σ",
            "\\Tau": "Τ",
            "\\Upsilon": "Υ",
            "\\Phi": "Φ",
            "\\Chi": "Χ",
            "\\Psi": "Ψ",
            "\\Omega": "Ω",
            # Operators and symbols
            "\\times": "×",
            "\\div": "÷",
            "\\pm": "±",
            "\\mp": "∓",
            "\\cdot": "·",
            "\\ast": "∗",
            "\\leq": "≤",
            "\\geq": "≥",
            "\\neq": "≠",
            "\\approx": "≈",
            "\\equiv": "≡",
            "\\sum": "∑",
            "\\prod": "∏",
            "\\int": "∫",
            "\\partial": "∂",
            "\\infty": "∞",
            "\\nabla": "∇",
            "\\forall": "∀",
            "\\exists": "∃",
            "\\nexists": "∄",
            "\\in": "∈",
            "\\notin": "∉",
            "\\subset": "⊂",
            "\\supset": "⊃",
            "\\cup": "∪",
            "\\cap": "∩",
            "\\emptyset": "∅",
            "\\rightarrow": "→",
            "\\leftarrow": "←",
            "\\Rightarrow": "⇒",
            "\\Leftarrow": "⇐",
            # Additional symbols
            "\\sqrt": "√",
            "\\propto": "∝",
            "\\angle": "∠",
            "\\triangle": "△",
            "\\square": "□",
        }

        # Regex patterns for math commands
        self.command_pattern: Pattern = re.compile(r"\\([a-zA-Z]+|.)")

        # Patterns for superscripts and subscripts
        self.superscript_map = {
            "0": "⁰",
            "1": "¹",
            "2": "²",
            "3": "³",
            "4": "⁴",
            "5": "⁵",
            "6": "⁶",
            "7": "⁷",
            "8": "⁸",
            "9": "⁹",
            "+": "⁺",
            "-": "⁻",
            "=": "⁼",
            "(": "⁽",
            ")": "⁾",
            "a": "ᵃ",
            "b": "ᵇ",
            "c": "ᶜ",
            "d": "ᵈ",
            "e": "ᵉ",
            "f": "ᶠ",
            "g": "ᵍ",
            "h": "ʰ",
            "i": "ⁱ",
            "j": "ʲ",
            "k": "ᵏ",
            "l": "ˡ",
            "m": "ᵐ",
            "n": "ⁿ",
            "o": "ᵒ",
            "p": "ᵖ",
            "r": "ʳ",
            "s": "ˢ",
            "t": "ᵗ",
            "u": "ᵘ",
            "v": "ᵛ",
            "w": "ʷ",
            "x": "ˣ",
            "y": "ʸ",
            "z": "ᶻ",
        }

        self.subscript_map = {
            "0": "₀",
            "1": "₁",
            "2": "₂",
            "3": "₃",
            "4": "₄",
            "5": "₅",
            "6": "₆",
            "7": "₇",
            "8": "₈",
            "9": "₉",
            "+": "₊",
            "-": "₋",
            "=": "₌",
            "(": "₍",
            ")": "₎",
            "a": "ₐ",
            "e": "ₑ",
            "h": "ₕ",
            "i": "ᵢ",
            "j": "ⱼ",
            "k": "ₖ",
            "l": "ₗ",
            "m": "ₘ",
            "n": "ₙ",
            "o": "ₒ",
            "p": "ₚ",
            "r": "ᵣ",
            "s": "ₛ",
            "t": "ₜ",
            "u": "ᵤ",
            "v": "ᵥ",
            "x": "ₓ",
        }

    def _convert_superscript(self, text: str) -> str:
        """Convert text to superscript characters."""
        result = ""
        for char in text:
            result += self.superscript_map.get(char, char)
        return result

    def _convert_subscript(self, text: str) -> str:
        """Convert text to subscript characters."""
        result = ""
        for char in text:
            result += self.subscript_map.get(char, char)
        return result

    def render_to_text(self, expression: str, style: Optional[Style] = None) -> Text:
        """Render a LaTeX math expression as a Rich Text object.

        Args:
            expression: LaTeX math expression
            style: Optional style to apply to the rendered expression

        Returns:
            Rich Text object containing the rendered expression
        """
        rendered_str = self.render_expression(expression)
        return Text(rendered_str, style=style)

    def render_expression(self, expression: str) -> str:
        """Convert a LaTeX math expression to Unicode text.

        Args:
            expression: LaTeX math expression

        Returns:
            Unicode representation of the math expression
        """
        # Process the expression and convert to Unicode
        result = expression.strip()

        # Replace LaTeX commands with Unicode symbols
        def replace_command(match):
            command = match.group(1)
            replacement = self.symbols.get("\\" + command, f"\\{command}")
            return replacement

        result = self.command_pattern.sub(replace_command, result)
        
        # For operators that should not have spaces
        unspaced_symbols = ["×", "÷", "±", "∓", "·", "∗", "^", "√"]
        
        # First, normalize unspaced operators
        for symbol in unspaced_symbols:
            # Remove spaces before and after these operators
            result = result.replace(f" {symbol} ", symbol)
            result = result.replace(f"{symbol} ", symbol)
            result = result.replace(f" {symbol}", symbol)
        
        # Process superscripts (^)
        superscript_pattern = re.compile(r"\^{([^}]+)}|\^([a-zA-Z0-9])")

        def replace_superscript(match):
            text = match.group(1) if match.group(1) else match.group(2)
            return self._convert_superscript(text)

        result = superscript_pattern.sub(replace_superscript, result)

        # Process subscripts (_)
        subscript_pattern = re.compile(r"_{([^}]+)}_([a-zA-Z0-9])")

        def replace_subscript(match):
            text = match.group(1) if match.group(1) else match.group(2)
            return self._convert_subscript(text)

        result = subscript_pattern.sub(replace_subscript, result)

        # Handle fractions (very basic)
        fraction_pattern = re.compile(r"\\frac{([^}]+)}{([^}]+)}")

        def replace_fraction(match):
            numerator = match.group(1)
            denominator = match.group(2)
            return f"{numerator}/{denominator}"

        result = fraction_pattern.sub(replace_fraction, result)

        return result