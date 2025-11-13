class RichColor {
    [int]$Red
    [int]$Green
    [int]$Blue
    [string]$Name

    # Constructor for RGB
    RichColor([int]$r, [int]$g, [int]$b) {
        $this.Red = [Math]::Max(0, [Math]::Min(255, $r))
        $this.Green = [Math]::Max(0, [Math]::Min(255, $g))
        $this.Blue = [Math]::Max(0, [Math]::Min(255, $b))
        $this.Name = ""
    }

    # Constructor for named color
    RichColor([string]$name) {
        $this.Name = $name.ToLower()
        $rgb = $this.ParseNamedColor($name)
        $this.Red = $rgb[0]
        $this.Green = $rgb[1]
        $this.Blue = $rgb[2]
    }

    # Parse named colors
    hidden [int[]] ParseNamedColor([string]$name) {
        $colors = @{
            'black'   = @(0, 0, 0)
            'red'     = @(255, 0, 0)
            'green'   = @(0, 255, 0)
            'yellow'  = @(255, 255, 0)
            'blue'    = @(0, 0, 255)
            'magenta' = @(255, 0, 255)
            'cyan'    = @(0, 255, 255)
            'white'   = @(255, 255, 255)
            'bright_black'   = @(128, 128, 128)
            'bright_red'     = @(255, 128, 128)
            'bright_green'   = @(128, 255, 128)
            'bright_yellow'  = @(255, 255, 128)
            'bright_blue'    = @(128, 128, 255)
            'bright_magenta' = @(255, 128, 255)
            'bright_cyan'    = @(128, 255, 255)
            'bright_white'   = @(255, 255, 255)
            'grey'    = @(128, 128, 128)
            'gray'    = @(128, 128, 128)
            'orange'  = @(255, 165, 0)
            'purple'  = @(128, 0, 128)
            'pink'    = @(255, 192, 203)
        }

        $normalizedName = $name.ToLower().Replace(' ', '_').Replace('-', '_')
        if ($colors.ContainsKey($normalizedName)) {
            return $colors[$normalizedName]
        }

        # Try to parse hex color (#RGB or #RRGGBB)
        if ($name -match '^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$') {
            $hex = $name.Substring(1)
            if ($hex.Length -eq 3) {
                $r = [Convert]::ToInt32($hex[0].ToString() * 2, 16)
                $g = [Convert]::ToInt32($hex[1].ToString() * 2, 16)
                $b = [Convert]::ToInt32($hex[2].ToString() * 2, 16)
            } else {
                $r = [Convert]::ToInt32($hex.Substring(0, 2), 16)
                $g = [Convert]::ToInt32($hex.Substring(2, 2), 16)
                $b = [Convert]::ToInt32($hex.Substring(4, 2), 16)
            }
            return @($r, $g, $b)
        }

        # Default to white if unknown
        return @(255, 255, 255)
    }

    # Get ANSI escape code for foreground color
    [string] GetForegroundCode() {
        return "`e[38;2;$($this.Red);$($this.Green);$($this.Blue)m"
    }

    # Get ANSI escape code for background color
    [string] GetBackgroundCode() {
        return "`e[48;2;$($this.Red);$($this.Green);$($this.Blue)m"
    }

    # Convert to hex string
    [string] ToHex() {
        return "#{0:X2}{1:X2}{2:X2}" -f $this.Red, $this.Green, $this.Blue
    }

    [string] ToString() {
        if ($this.Name) {
            return $this.Name
        }
        return $this.ToHex()
    }
}

# Helper function to create color from various inputs
function New-RichColor {
    param(
        [Parameter(ValueFromPipeline)]
        $Color
    )

    if ($Color -is [RichColor]) {
        return $Color
    }

    if ($Color -is [string]) {
        return [RichColor]::new($Color)
    }

    if ($Color -is [array] -and $Color.Count -eq 3) {
        return [RichColor]::new($Color[0], $Color[1], $Color[2])
    }

    return [RichColor]::new("white")
}
