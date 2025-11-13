class RichConsole {
    [int]$Width
    [int]$Height
    [bool]$ColorSystem
    [object]$Theme

    RichConsole() {
        $this.UpdateSize()
        $this.ColorSystem = $this.DetectColorSupport()
        $this.Theme = @{
            'info'    = New-RichColor 'cyan'
            'warning' = New-RichColor 'yellow'
            'error'   = New-RichColor 'red'
            'success' = New-RichColor 'green'
        }
    }

    # Detect terminal size
    hidden [void] UpdateSize() {
        try {
            $this.Width = $Host.UI.RawUI.WindowSize.Width
            $this.Height = $Host.UI.RawUI.WindowSize.Height
        } catch {
            $this.Width = 80
            $this.Height = 24
        }
    }

    # Detect if terminal supports colors
    hidden [bool] DetectColorSupport() {
        # PowerShell 7+ has good ANSI support
        if ($PSVersionTable.PSVersion.Major -ge 7) {
            return $true
        }

        # Check if running in Windows Terminal or other modern terminals
        if ($env:WT_SESSION -or $env:TERM_PROGRAM) {
            return $true
        }

        return $false
    }

    # Print text with optional style
    [void] Print([string]$text) {
        Write-Host $text
    }

    [void] Print([string]$text, [RichStyle]$style) {
        if ($style) {
            Write-Host $style.Apply($text) -NoNewline
            Write-Host ""
        } else {
            Write-Host $text
        }
    }

    # Print with foreground color
    [void] Print([string]$text, [RichColor]$color) {
        $style = [RichStyle]::new()
        $style.ForegroundColor = $color
        $this.Print($text, $style)
    }

    # Print without newline
    [void] PrintNoNewline([string]$text) {
        Write-Host $text -NoNewline
    }

    [void] PrintNoNewline([string]$text, [RichStyle]$style) {
        if ($style) {
            Write-Host $style.Apply($text) -NoNewline
        } else {
            Write-Host $text -NoNewline
        }
    }

    # Print a line (rule)
    [void] Rule([string]$title) {
        $this.Rule($title, $null)
    }

    [void] Rule([string]$title, [RichColor]$color) {
        $this.UpdateSize()

        if ($title) {
            $titleLen = $title.Length + 2  # Add spaces around title
            $leftLen = [Math]::Floor(($this.Width - $titleLen) / 2)
            $rightLen = $this.Width - $titleLen - $leftLen

            $line = "─" * $leftLen + " $title " + "─" * $rightLen
        } else {
            $line = "─" * $this.Width
        }

        if ($color) {
            $style = [RichStyle]::new()
            $style.ForegroundColor = $color
            $this.Print($line, $style)
        } else {
            $this.Print($line)
        }
    }

    # Print styled text with theme
    [void] Info([string]$text) {
        $style = [RichStyle]::new()
        $style.ForegroundColor = $this.Theme['info']
        $this.Print($text, $style)
    }

    [void] Warning([string]$text) {
        $style = [RichStyle]::new()
        $style.ForegroundColor = $this.Theme['warning']
        $this.Print($text, $style)
    }

    [void] Error([string]$text) {
        $style = [RichStyle]::new()
        $style.ForegroundColor = $this.Theme['error']
        $this.Print($text, $style)
    }

    [void] Success([string]$text) {
        $style = [RichStyle]::new()
        $style.ForegroundColor = $this.Theme['success']
        $this.Print($text, $style)
    }

    # Clear the screen
    [void] Clear() {
        Clear-Host
    }

    # Print a blank line
    [void] NewLine() {
        Write-Host ""
    }

    [void] NewLine([int]$count) {
        for ($i = 0; $i -lt $count; $i++) {
            Write-Host ""
        }
    }
}

# Create a default console instance
$Global:RichConsole = [RichConsole]::new()

# Helper function to get the global console
function Get-RichConsole {
    return $Global:RichConsole
}

# Convenience function for printing
function Write-Rich {
    param(
        [Parameter(Mandatory, Position = 0)]
        [string]$Text,

        [Parameter(Position = 1)]
        [RichStyle]$Style,

        [RichColor]$Color,

        [switch]$Bold,
        [switch]$Italic,
        [switch]$Underline,
        [switch]$NoNewline
    )

    $console = Get-RichConsole

    # Build style if not provided
    if (-not $Style -and ($Color -or $Bold -or $Italic -or $Underline)) {
        $Style = [RichStyle]::new()
        if ($Color) { $Style.ForegroundColor = $Color }
        if ($Bold) { $Style.Bold = $true }
        if ($Italic) { $Style.Italic = $true }
        if ($Underline) { $Style.Underline = $true }
    }

    if ($NoNewline) {
        $console.PrintNoNewline($Text, $Style)
    } else {
        $console.Print($Text, $Style)
    }
}
