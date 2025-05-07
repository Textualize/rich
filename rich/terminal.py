"""Terminal color support detection and fallback options."""

import os
import sys
from typing import Dict, Optional, Set, Tuple

# ANSI color codes
ANSI_COLORS = {
    'black': 30,
    'red': 31,
    'green': 32,
    'yellow': 33,
    'blue': 34,
    'magenta': 35,
    'cyan': 36,
    'white': 37,
    'bright_black': 90,
    'bright_red': 91,
    'bright_green': 92,
    'bright_yellow': 93,
    'bright_blue': 94,
    'bright_magenta': 95,
    'bright_cyan': 96,
    'bright_white': 97,
}

class TerminalColorSupport:
    """Detect and manage terminal color support."""
    
    def __init__(self) -> None:
        self._color_support: Optional[bool] = None
        self._supported_colors: Set[str] = set()
        self._fallback_colors: Dict[str, str] = {}
        
    def detect_color_support(self) -> bool:
        """Detect if the terminal supports colors."""
        if self._color_support is not None:
            return self._color_support
            
        # Check environment variables
        if 'NO_COLOR' in os.environ:
            self._color_support = False
            return False
            
        if 'FORCE_COLOR' in os.environ:
            self._color_support = True
            return True
            
        # Check if we're in a terminal
        if not sys.stdout.isatty():
            self._color_support = False
            return False
            
        # Check terminal type
        term = os.environ.get('TERM', '').lower()
        if term in ('dumb', 'unknown'):
            self._color_support = False
            return False
            
        # Windows specific checks
        if sys.platform == 'win32':
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                if kernel32.GetConsoleMode(kernel32.GetStdHandle(-11), None):
                    self._color_support = True
                    return True
            except Exception:
                pass
                
        # Default to True for modern terminals
        self._color_support = True
        return True
        
    def get_supported_colors(self) -> Set[str]:
        """Get the set of supported colors."""
        if not self._supported_colors:
            if self.detect_color_support():
                # Test each color
                for color in ANSI_COLORS:
                    if self._test_color(color):
                        self._supported_colors.add(color)
                        
        return self._supported_colors
        
    def _test_color(self, color: str) -> bool:
        """Test if a specific color is supported."""
        # Implementation would test actual color support
        # For now, return True for all colors if color support is enabled
        return self.detect_color_support()
        
    def get_fallback_color(self, color: str) -> str:
        """Get a fallback color if the requested color is not supported."""
        if color in self._fallback_colors:
            return self._fallback_colors[color]
            
        # Define fallback mappings
        fallbacks = {
            'bright_black': 'black',
            'bright_red': 'red',
            'bright_green': 'green',
            'bright_yellow': 'yellow',
            'bright_blue': 'blue',
            'bright_magenta': 'magenta',
            'bright_cyan': 'cyan',
            'bright_white': 'white',
        }
        
        fallback = fallbacks.get(color, 'white')
        self._fallback_colors[color] = fallback
        return fallback
        
    def get_color_code(self, color: str) -> Tuple[int, bool]:
        """Get the ANSI color code and whether it's supported."""
        if not self.detect_color_support():
            return (0, False)
            
        if color not in self.get_supported_colors():
            color = self.get_fallback_color(color)
            
        return (ANSI_COLORS[color], True)

# Global instance
terminal_color = TerminalColorSupport() 