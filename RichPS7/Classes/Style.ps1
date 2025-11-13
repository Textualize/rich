class RichStyle {
    [RichColor]$ForegroundColor
    [RichColor]$BackgroundColor
    [bool]$Bold
    [bool]$Italic
    [bool]$Underline
    [bool]$Strike
    [bool]$Dim

    RichStyle() {
        $this.Bold = $false
        $this.Italic = $false
        $this.Underline = $false
        $this.Strike = $false
        $this.Dim = $false
    }

    # Get the complete ANSI code for this style
    [string] GetAnsiCode() {
        $codes = @()

        # Text attributes
        if ($this.Bold) { $codes += "1" }
        if ($this.Dim) { $codes += "2" }
        if ($this.Italic) { $codes += "3" }
        if ($this.Underline) { $codes += "4" }
        if ($this.Strike) { $codes += "9" }

        # Build the complete escape sequence
        $result = ""

        if ($codes.Count -gt 0) {
            $result += "`e[$($codes -join ';')m"
        }

        if ($this.ForegroundColor) {
            $result += $this.ForegroundColor.GetForegroundCode()
        }

        if ($this.BackgroundColor) {
            $result += $this.BackgroundColor.GetBackgroundCode()
        }

        return $result
    }

    # Reset code
    static [string] GetResetCode() {
        return "`e[0m"
    }

    # Apply style to text
    [string] Apply([string]$text) {
        $code = $this.GetAnsiCode()
        if ($code) {
            return "$code$text$([RichStyle]::GetResetCode())"
        }
        return $text
    }

    # Combine with another style
    [RichStyle] Combine([RichStyle]$other) {
        $result = [RichStyle]::new()

        # Copy from this style
        $result.ForegroundColor = $this.ForegroundColor
        $result.BackgroundColor = $this.BackgroundColor
        $result.Bold = $this.Bold
        $result.Italic = $this.Italic
        $result.Underline = $this.Underline
        $result.Strike = $this.Strike
        $result.Dim = $this.Dim

        # Override with other style
        if ($other.ForegroundColor) { $result.ForegroundColor = $other.ForegroundColor }
        if ($other.BackgroundColor) { $result.BackgroundColor = $other.BackgroundColor }
        if ($other.Bold) { $result.Bold = $true }
        if ($other.Italic) { $result.Italic = $true }
        if ($other.Underline) { $result.Underline = $true }
        if ($other.Strike) { $result.Strike = $true }
        if ($other.Dim) { $result.Dim = $true }

        return $result
    }
}

# Helper function to create styles easily
function New-RichStyle {
    param(
        [RichColor]$ForegroundColor,
        [RichColor]$BackgroundColor,
        [switch]$Bold,
        [switch]$Italic,
        [switch]$Underline,
        [switch]$Strike,
        [switch]$Dim
    )

    $style = [RichStyle]::new()

    if ($ForegroundColor) { $style.ForegroundColor = $ForegroundColor }
    if ($BackgroundColor) { $style.BackgroundColor = $BackgroundColor }
    if ($Bold) { $style.Bold = $true }
    if ($Italic) { $style.Italic = $true }
    if ($Underline) { $style.Underline = $true }
    if ($Strike) { $style.Strike = $true }
    if ($Dim) { $style.Dim = $true }

    return $style
}
