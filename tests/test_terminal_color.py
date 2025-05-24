"""Tests for terminal color support."""

import os
import sys
from unittest import mock

import pytest

from rich.terminal import TerminalColorSupport, terminal_color

def test_color_support_detection():
    """Test color support detection."""
    # Test NO_COLOR environment variable
    with mock.patch.dict(os.environ, {'NO_COLOR': '1'}):
        assert not terminal_color.detect_color_support()
        
    # Test FORCE_COLOR environment variable
    with mock.patch.dict(os.environ, {'FORCE_COLOR': '1'}):
        assert terminal_color.detect_color_support()
        
    # Test dumb terminal
    with mock.patch.dict(os.environ, {'TERM': 'dumb'}):
        assert not terminal_color.detect_color_support()
        
    # Test unknown terminal
    with mock.patch.dict(os.environ, {'TERM': 'unknown'}):
        assert not terminal_color.detect_color_support()

def test_supported_colors():
    """Test getting supported colors."""
    with mock.patch.object(terminal_color, 'detect_color_support', return_value=True):
        colors = terminal_color.get_supported_colors()
        assert isinstance(colors, set)
        assert len(colors) > 0

def test_fallback_colors():
    """Test fallback color mapping."""
    # Test bright color fallbacks
    assert terminal_color.get_fallback_color('bright_red') == 'red'
    assert terminal_color.get_fallback_color('bright_blue') == 'blue'
    
    # Test unknown color fallback
    assert terminal_color.get_fallback_color('unknown_color') == 'white'

def test_color_code():
    """Test getting color codes."""
    with mock.patch.object(terminal_color, 'detect_color_support', return_value=True):
        code, supported = terminal_color.get_color_code('red')
        assert code == 31  # ANSI code for red
        assert supported is True
        
    with mock.patch.object(terminal_color, 'detect_color_support', return_value=False):
        code, supported = terminal_color.get_color_code('red')
        assert code == 0
        assert supported is False

def test_windows_specific():
    """Test Windows-specific color support."""
    if sys.platform == 'win32':
        with mock.patch('ctypes.windll.kernel32.GetConsoleMode', return_value=1):
            assert terminal_color.detect_color_support()
            
        with mock.patch('ctypes.windll.kernel32.GetConsoleMode', return_value=0):
            assert not terminal_color.detect_color_support() 