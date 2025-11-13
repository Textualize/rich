# RichPS7

**Beautiful terminal formatting for PowerShell 7**

RichPS7 is a PowerShell 7 port of Python's popular [Rich](https://github.com/Textualize/rich) library. It brings beautiful terminal formatting, colors, tables, panels, and progress bars to your PowerShell scripts.

![PowerShell Version](https://img.shields.io/badge/PowerShell-7.0+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- 🎨 **Rich Colors**: RGB, hex codes, and named colors with full ANSI support
- ✨ **Text Styling**: Bold, italic, underline, strikethrough, and dim text
- 📊 **Tables**: Beautiful tables with multiple box styles and alignment options
- 📦 **Panels**: Bordered panels with titles, subtitles, and custom styles
- 📈 **Progress Bars**: Live-updating progress bars with ETA estimation
- 🖥️ **Console**: Powerful console abstraction with themed output
- 🌈 **Cross-platform**: Works on Windows, macOS, and Linux

## Requirements

- PowerShell 7.0 or higher
- A terminal with ANSI color support (Windows Terminal, iTerm2, etc.)

## Installation

### Option 1: Direct Import

1. Clone or download this repository
2. Import the module:

```powershell
Import-Module ./RichPS7/RichPS7.psd1
```

### Option 2: Install to PowerShell Modules Directory

1. Copy the `RichPS7` folder to your PowerShell modules directory:

```powershell
# Windows
Copy-Item -Recurse ./RichPS7 "$env:USERPROFILE\Documents\PowerShell\Modules\"

# macOS/Linux
Copy-Item -Recurse ./RichPS7 "~/.local/share/powershell/Modules/"
```

2. Import the module:

```powershell
Import-Module RichPS7
```

### Option 3: Add to Profile

Add the import statement to your PowerShell profile for automatic loading:

```powershell
# Open your profile
notepad $PROFILE

# Add this line:
Import-Module RichPS7
```

## Quick Start

```powershell
# Import the module
Import-Module RichPS7

# Print colored text
Write-Rich "Hello, World!" -Color (New-RichColor 'cyan') -Bold

# Create a table
$table = New-RichTable -Title "System Info"
$table.AddColumn("Property")
$table.AddColumn("Value")
$table.AddRow(@("OS", $PSVersionTable.OS))
$table.AddRow(@("PowerShell", $PSVersionTable.PSVersion))
Write-Host $table.Render()

# Create a panel
$panel = New-RichPanel -Content "Important message!" -Title "Alert" -BoxStyle "double"
Write-Host $panel.Render()

# Show a progress bar
Invoke-RichProgress -Description "Processing" -Collection (1..50) -ScriptBlock {
    param($item)
    Start-Sleep -Milliseconds 50
}
```

## Usage Guide

### Colors

RichPS7 supports multiple ways to specify colors:

```powershell
# Named colors
$red = New-RichColor 'red'
$blue = New-RichColor 'blue'
$brightGreen = New-RichColor 'bright_green'

# Hex colors
$orange = New-RichColor '#FFA500'
$purple = New-RichColor '#9B59B6'

# RGB colors
$custom = [RichColor]::new(255, 128, 64)

# Use colors
Write-Rich "Colored text!" -Color $red
```

**Available named colors:**
- Basic: `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`
- Bright: `bright_black`, `bright_red`, `bright_green`, `bright_yellow`, `bright_blue`, `bright_magenta`, `bright_cyan`, `bright_white`
- Others: `gray`, `grey`, `orange`, `purple`, `pink`

### Text Styling

Apply various text styles to your output:

```powershell
# Individual styles
Write-Rich "Bold text" -Bold
Write-Rich "Italic text" -Italic
Write-Rich "Underlined text" -Underline

# Combined styles
Write-Rich "Bold and Italic" -Bold -Italic

# Using style objects
$style = New-RichStyle -ForegroundColor (New-RichColor 'cyan') -Bold -Underline
Write-Rich "Styled text" -Style $style

# Foreground and background colors
$style = New-RichStyle `
    -ForegroundColor (New-RichColor 'yellow') `
    -BackgroundColor (New-RichColor 'blue') `
    -Bold
Write-Rich "Yellow on blue" -Style $style
```

### Console

The console object provides themed output and utilities:

```powershell
$console = Get-RichConsole

# Themed messages
$console.Info("Information message")
$console.Warning("Warning message")
$console.Error("Error message")
$console.Success("Success message")

# Rules (horizontal lines)
$console.Rule()
$console.Rule("Section Title")
$console.Rule("Colored Rule", (New-RichColor 'cyan'))

# Utilities
$console.NewLine()
$console.NewLine(3)  # Multiple blank lines
$console.Clear()     # Clear screen
```

### Tables

Create beautiful tables with various options:

```powershell
# Basic table
$table = New-RichTable
$table.AddColumn("Name")
$table.AddColumn("Age")
$table.AddRow(@("Alice", "30"))
$table.AddRow(@("Bob", "25"))
Write-Host $table.Render()

# Table with title and custom box style
$table = New-RichTable -Title "Users" -BoxStyle "double"

# Columns with alignment
$table.AddColumn("Product", @{ Align = 'left' })
$table.AddColumn("Price", @{ Align = 'right' })
$table.AddColumn("Qty", @{ Align = 'center' })

# Add rows
$table.AddRow(@("Widget", "$19.99", "42"))
$table.AddRow(@("Gadget", "$29.99", "17"))

Write-Host $table.Render()

# Table with row separators
$table = New-RichTable -ShowLines
# ... add columns and rows ...
Write-Host $table.Render()

# Available box styles: 'rounded', 'square', 'double', 'simple'
```

### Panels

Create bordered panels for highlighting content:

```powershell
# Simple panel
$panel = New-RichPanel -Content "Hello, World!"
Write-Host $panel.Render()

# Panel with title
$panel = New-RichPanel -Content "Important info" -Title "Alert"
Write-Host $panel.Render()

# Panel with subtitle
$panel = New-RichPanel `
    -Content "Content here" `
    -Title "Main Title" `
    -Subtitle "Subtitle"
Write-Host $panel.Render()

# Multi-line content
$content = @"
Line 1
Line 2
Line 3
"@
$panel = New-RichPanel -Content $content -Title "Multi-line"
Write-Host $panel.Render()

# Custom styling
$titleStyle = New-RichStyle -ForegroundColor (New-RichColor 'yellow') -Bold
$borderStyle = New-RichStyle -ForegroundColor (New-RichColor 'cyan')

$panel = New-RichPanel `
    -Content "Styled panel" `
    -Title "Custom" `
    -TitleStyle $titleStyle `
    -BorderStyle $borderStyle `
    -BoxStyle "double"
Write-Host $panel.Render()

# Box styles: 'rounded', 'square', 'double', 'heavy', 'simple'
# Title alignment: 'left', 'center', 'right'
```

### Progress Bars

Show progress for long-running operations:

```powershell
# Simple progress with Invoke-RichProgress
$items = 1..100
Invoke-RichProgress -Description "Processing items" -Collection $items -ScriptBlock {
    param($item)
    # Do work here
    Start-Sleep -Milliseconds 50
}

# Manual progress control
$progress = New-RichProgress
$task = $progress.AddTask("Downloading", 100)

$progress.Start()
try {
    for ($i = 0; $i -lt 100; $i++) {
        $task.Advance(1)
        $progress.Refresh()
        Start-Sleep -Milliseconds 50
    }
} finally {
    $progress.Stop()
}

# Multiple progress bars
$progress = New-RichProgress
$task1 = $progress.AddTask("Task 1", 50)
$task2 = $progress.AddTask("Task 2", 100)
$task3 = $progress.AddTask("Task 3", 75)

$progress.Start()
try {
    while (-not $progress.IsComplete()) {
        # Update tasks as needed
        if (-not $task1.IsComplete) { $task1.Advance(1) }
        if (-not $task2.IsComplete) { $task2.Advance(2) }
        if (-not $task3.IsComplete) { $task3.Advance(1) }

        $progress.Refresh()
        Start-Sleep -Milliseconds 50
    }
} finally {
    $progress.Stop()
}

# Custom colors
$task.CompleteColor = New-RichColor 'cyan'
$task.RemainingColor = New-RichColor 'bright_black'
```

## Examples

Check out the `Examples` directory for complete demonstrations:

- `01-Colors.ps1` - Color and styling examples
- `02-Tables.ps1` - Table formatting examples
- `03-Panels.ps1` - Panel examples with various styles
- `04-Progress.ps1` - Progress bar examples
- `05-Complete-Demo.ps1` - Complete feature demonstration

Run an example:

```powershell
./RichPS7/Examples/05-Complete-Demo.ps1
```

## API Reference

### Functions

- `New-RichColor` - Create a color from name, hex, or RGB
- `New-RichStyle` - Create a text style with colors and attributes
- `Get-RichConsole` - Get the global console instance
- `Write-Rich` - Write styled text to the console
- `New-RichTable` - Create a new table
- `New-RichPanel` - Create a new panel
- `New-RichProgress` - Create a progress tracker
- `Invoke-RichProgress` - Simple progress tracking helper

### Classes

- `RichColor` - Color representation with ANSI code generation
- `RichStyle` - Text style with color and attributes
- `RichConsole` - Console output handler
- `RichTable` - Table renderer
- `RichPanel` - Panel renderer
- `RichProgress` - Progress tracker
- `RichProgressBar` - Individual progress bar

## Comparison with Python Rich

This PowerShell port includes the core features from Python's Rich library:

| Feature | Python Rich | RichPS7 |
|---------|-------------|---------|
| Colors (RGB/Hex/Named) | ✅ | ✅ |
| Text Styling | ✅ | ✅ |
| Tables | ✅ | ✅ |
| Panels | ✅ | ✅ |
| Progress Bars | ✅ | ✅ |
| Console | ✅ | ✅ |
| Syntax Highlighting | ✅ | ⏳ (future) |
| Markdown Rendering | ✅ | ⏳ (future) |
| Tracebacks | ✅ | ⏳ (future) |
| Tree Views | ✅ | ⏳ (future) |
| Live Display | ✅ | 🔶 (partial) |

✅ = Implemented | ⏳ = Planned | 🔶 = Partially implemented

## Contributing

Contributions are welcome! This is a community port of the Rich library.

## License

MIT License - see LICENSE file for details

## Credits

- Original Python Rich library by [Will McGugan](https://github.com/willmcgugan)
- Python Rich: https://github.com/Textualize/rich

## Links

- [Python Rich Documentation](https://rich.readthedocs.io/)
- [PowerShell Documentation](https://docs.microsoft.com/powershell/)

---

Made with ❤️ for the PowerShell community
