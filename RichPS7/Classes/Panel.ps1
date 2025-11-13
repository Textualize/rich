class RichPanel {
    [string]$Content
    [string]$Title
    [string]$Subtitle
    [string]$BoxStyle
    [RichStyle]$TitleStyle
    [RichStyle]$BorderStyle
    [RichStyle]$ContentStyle
    [int]$Width
    [int]$Padding
    [string]$TitleAlign
    [hashtable]$BoxChars

    RichPanel([string]$content) {
        $this.Content = $content
        $this.BoxStyle = "rounded"
        $this.Padding = 1
        $this.TitleAlign = "left"
        $this.Width = 0  # Auto-width
        $this.InitializeBoxChars()

        # Default styles
        $this.TitleStyle = [RichStyle]::new()
        $this.TitleStyle.Bold = $true
    }

    hidden [void] InitializeBoxChars() {
        # Reuse the same box drawing characters as Table
        $this.BoxChars = @{
            'rounded' = @{
                'top_left'     = '╭'
                'top_right'    = '╮'
                'bottom_left'  = '╰'
                'bottom_right' = '╯'
                'horizontal'   = '─'
                'vertical'     = '│'
            }
            'square' = @{
                'top_left'     = '┌'
                'top_right'    = '┐'
                'bottom_left'  = '└'
                'bottom_right' = '┘'
                'horizontal'   = '─'
                'vertical'     = '│'
            }
            'double' = @{
                'top_left'     = '╔'
                'top_right'    = '╗'
                'bottom_left'  = '╚'
                'bottom_right' = '╝'
                'horizontal'   = '═'
                'vertical'     = '║'
            }
            'heavy' = @{
                'top_left'     = '┏'
                'top_right'    = '┓'
                'bottom_left'  = '┗'
                'bottom_right' = '┛'
                'horizontal'   = '━'
                'vertical'     = '┃'
            }
            'simple' = @{
                'top_left'     = '+'
                'top_right'    = '+'
                'bottom_left'  = '+'
                'bottom_right' = '+'
                'horizontal'   = '-'
                'vertical'     = '|'
            }
        }
    }

    # Calculate the width of the panel
    hidden [int] CalculateWidth() {
        if ($this.Width -gt 0) {
            return $this.Width
        }

        # Calculate based on content
        $lines = $this.Content -split "`n"
        $maxWidth = 0

        foreach ($line in $lines) {
            if ($line.Length -gt $maxWidth) {
                $maxWidth = $line.Length
            }
        }

        # Add padding
        $maxWidth += ($this.Padding * 2)

        # Check title width
        if ($this.Title) {
            $titleWidth = $this.Title.Length + 4  # Add space for title decoration
            if ($titleWidth -gt $maxWidth) {
                $maxWidth = $titleWidth
            }
        }

        # Ensure minimum width
        if ($maxWidth -lt 10) {
            $maxWidth = 10
        }

        return $maxWidth
    }

    # Align text within given width
    hidden [string] AlignText([string]$text, [int]$width, [string]$align) {
        $len = $text.Length

        if ($len -ge $width) {
            return $text.Substring(0, $width)
        }

        $padding = $width - $len

        switch ($align) {
            'center' {
                $leftPad = [Math]::Floor($padding / 2)
                $rightPad = $padding - $leftPad
                return (' ' * $leftPad) + $text + (' ' * $rightPad)
            }
            'right' {
                return (' ' * $padding) + $text
            }
            default {  # left
                return $text + (' ' * $padding)
            }
        }
    }

    # Render the panel
    [string] Render() {
        $output = [System.Text.StringBuilder]::new()
        $box = $this.BoxChars[$this.BoxStyle]
        $width = $this.CalculateWidth()
        $innerWidth = $width - 2  # Subtract borders

        # Top border with title
        if ($this.Title) {
            $titleText = " $($this.Title) "
            if ($this.TitleStyle) {
                $titleText = $this.TitleStyle.Apply($titleText)
            }

            $titleLen = $this.Title.Length + 2
            $leftLen = switch ($this.TitleAlign) {
                'center' { [Math]::Max(1, [Math]::Floor(($innerWidth - $titleLen) / 2)) }
                'right'  { [Math]::Max(1, $innerWidth - $titleLen - 1) }
                default  { 1 }  # left
            }
            $rightLen = [Math]::Max(1, $innerWidth - $titleLen - $leftLen)

            $topLine = $box.top_left + ($box.horizontal * $leftLen) + $titleText + ($box.horizontal * $rightLen) + $box.top_right
        } else {
            $topLine = $box.top_left + ($box.horizontal * $innerWidth) + $box.top_right
        }

        if ($this.BorderStyle) {
            $topLine = $this.BorderStyle.Apply($topLine)
        }
        [void]$output.AppendLine($topLine)

        # Content lines
        $lines = $this.Content -split "`n"
        $contentWidth = $innerWidth - ($this.Padding * 2)

        foreach ($line in $lines) {
            $paddedLine = (' ' * $this.Padding) + $line.PadRight($contentWidth) + (' ' * $this.Padding)

            if ($this.ContentStyle) {
                $paddedLine = $this.ContentStyle.Apply($paddedLine)
            }

            $bordered = $box.vertical + $paddedLine + $box.vertical

            if ($this.BorderStyle) {
                # Apply border style to the border characters only
                $bordered = $this.BorderStyle.Apply($box.vertical) + $paddedLine + $this.BorderStyle.Apply($box.vertical)
            }

            [void]$output.AppendLine($bordered)
        }

        # Bottom border with subtitle
        if ($this.Subtitle) {
            $subtitleText = " $($this.Subtitle) "
            $subtitleLen = $this.Subtitle.Length + 2
            $leftLen = [Math]::Max(1, [Math]::Floor(($innerWidth - $subtitleLen) / 2))
            $rightLen = [Math]::Max(1, $innerWidth - $subtitleLen - $leftLen)

            $bottomLine = $box.bottom_left + ($box.horizontal * $leftLen) + $subtitleText + ($box.horizontal * $rightLen) + $box.bottom_right
        } else {
            $bottomLine = $box.bottom_left + ($box.horizontal * $innerWidth) + $box.bottom_right
        }

        if ($this.BorderStyle) {
            $bottomLine = $this.BorderStyle.Apply($bottomLine)
        }
        [void]$output.Append($bottomLine)

        return $output.ToString()
    }
}

# Helper function to create and render a panel
function New-RichPanel {
    param(
        [Parameter(Mandatory, Position = 0)]
        [string]$Content,

        [string]$Title,
        [string]$Subtitle,
        [string]$BoxStyle = "rounded",
        [int]$Width = 0,
        [int]$Padding = 1,
        [string]$TitleAlign = "left",
        [RichStyle]$TitleStyle,
        [RichStyle]$BorderStyle,
        [RichStyle]$ContentStyle
    )

    $panel = [RichPanel]::new($Content)

    if ($Title) { $panel.Title = $Title }
    if ($Subtitle) { $panel.Subtitle = $Subtitle }
    $panel.BoxStyle = $BoxStyle
    $panel.Width = $Width
    $panel.Padding = $Padding
    $panel.TitleAlign = $TitleAlign

    if ($TitleStyle) { $panel.TitleStyle = $TitleStyle }
    if ($BorderStyle) { $panel.BorderStyle = $BorderStyle }
    if ($ContentStyle) { $panel.ContentStyle = $ContentStyle }

    return $panel
}
