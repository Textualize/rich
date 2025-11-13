class RichTable {
    [string]$Title
    [System.Collections.ArrayList]$Columns
    [System.Collections.ArrayList]$Rows
    [string]$BoxStyle
    [RichStyle]$HeaderStyle
    [RichStyle]$RowStyle
    [bool]$ShowHeader
    [bool]$ShowLines
    [hashtable]$BoxChars

    RichTable() {
        $this.Columns = [System.Collections.ArrayList]::new()
        $this.Rows = [System.Collections.ArrayList]::new()
        $this.BoxStyle = "rounded"
        $this.ShowHeader = $true
        $this.ShowLines = $false
        $this.InitializeBoxChars()

        # Default header style
        $this.HeaderStyle = [RichStyle]::new()
        $this.HeaderStyle.Bold = $true
        $this.HeaderStyle.ForegroundColor = New-RichColor 'cyan'
    }

    hidden [void] InitializeBoxChars() {
        # Box drawing characters for different styles
        $this.BoxChars = @{
            'rounded' = @{
                'top_left'     = '╭'
                'top_right'    = '╮'
                'bottom_left'  = '╰'
                'bottom_right' = '╯'
                'horizontal'   = '─'
                'vertical'     = '│'
                'cross'        = '┼'
                'top_join'     = '┬'
                'bottom_join'  = '┴'
                'left_join'    = '├'
                'right_join'   = '┤'
            }
            'square' = @{
                'top_left'     = '┌'
                'top_right'    = '┐'
                'bottom_left'  = '└'
                'bottom_right' = '┘'
                'horizontal'   = '─'
                'vertical'     = '│'
                'cross'        = '┼'
                'top_join'     = '┬'
                'bottom_join'  = '┴'
                'left_join'    = '├'
                'right_join'   = '┤'
            }
            'double' = @{
                'top_left'     = '╔'
                'top_right'    = '╗'
                'bottom_left'  = '╚'
                'bottom_right' = '╝'
                'horizontal'   = '═'
                'vertical'     = '║'
                'cross'        = '╬'
                'top_join'     = '╦'
                'bottom_join'  = '╩'
                'left_join'    = '╠'
                'right_join'   = '╣'
            }
            'simple' = @{
                'top_left'     = '+'
                'top_right'    = '+'
                'bottom_left'  = '+'
                'bottom_right' = '+'
                'horizontal'   = '-'
                'vertical'     = '|'
                'cross'        = '+'
                'top_join'     = '+'
                'bottom_join'  = '+'
                'left_join'    = '+'
                'right_join'   = '+'
            }
        }
    }

    # Add a column
    [void] AddColumn([string]$name) {
        $this.AddColumn($name, @{})
    }

    [void] AddColumn([string]$name, [hashtable]$options) {
        $column = @{
            'Name'   = $name
            'Width'  = if ($options.Width) { $options.Width } else { $null }
            'Align'  = if ($options.Align) { $options.Align } else { 'left' }
            'Style'  = if ($options.Style) { $options.Style } else { $null }
        }
        [void]$this.Columns.Add($column)
    }

    # Add a row
    [void] AddRow([array]$cells) {
        [void]$this.Rows.Add($cells)
    }

    # Calculate column widths
    hidden [array] CalculateWidths() {
        $widths = @()

        for ($i = 0; $i -lt $this.Columns.Count; $i++) {
            $column = $this.Columns[$i]

            if ($column.Width) {
                $widths += $column.Width
            } else {
                # Calculate based on content
                $maxWidth = $column.Name.Length

                foreach ($row in $this.Rows) {
                    if ($i -lt $row.Count) {
                        $cellWidth = $row[$i].ToString().Length
                        if ($cellWidth -gt $maxWidth) {
                            $maxWidth = $cellWidth
                        }
                    }
                }

                $widths += $maxWidth
            }
        }

        return $widths
    }

    # Align text within a cell
    hidden [string] AlignText([string]$text, [int]$width, [string]$align) {
        $text = $text.ToString()
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

    # Render the table
    [string] Render() {
        $output = [System.Text.StringBuilder]::new()
        $widths = $this.CalculateWidths()
        $box = $this.BoxChars[$this.BoxStyle]

        # Top border
        [void]$output.Append($box.top_left)
        for ($i = 0; $i -lt $widths.Count; $i++) {
            [void]$output.Append($box.horizontal * ($widths[$i] + 2))
            if ($i -lt $widths.Count - 1) {
                [void]$output.Append($box.top_join)
            }
        }
        [void]$output.AppendLine($box.top_right)

        # Title (if present)
        if ($this.Title) {
            $totalWidth = ($widths | Measure-Object -Sum).Sum + ($widths.Count * 2) + ($widths.Count - 1)
            $titleText = $this.AlignText($this.Title, $totalWidth, 'center')
            [void]$output.Append($box.vertical)
            [void]$output.Append($titleText)
            [void]$output.AppendLine($box.vertical)

            # Separator after title
            [void]$output.Append($box.left_join)
            for ($i = 0; $i -lt $widths.Count; $i++) {
                [void]$output.Append($box.horizontal * ($widths[$i] + 2))
                if ($i -lt $widths.Count - 1) {
                    [void]$output.Append($box.cross)
                }
            }
            [void]$output.AppendLine($box.right_join)
        }

        # Header row
        if ($this.ShowHeader) {
            [void]$output.Append($box.vertical)
            for ($i = 0; $i -lt $this.Columns.Count; $i++) {
                $column = $this.Columns[$i]
                $text = $this.AlignText($column.Name, $widths[$i], $column.Align)

                if ($this.HeaderStyle) {
                    $text = $this.HeaderStyle.Apply($text)
                }

                [void]$output.Append(" $text ")
                [void]$output.Append($box.vertical)
            }
            [void]$output.AppendLine()

            # Separator after header
            [void]$output.Append($box.left_join)
            for ($i = 0; $i -lt $widths.Count; $i++) {
                [void]$output.Append($box.horizontal * ($widths[$i] + 2))
                if ($i -lt $widths.Count - 1) {
                    [void]$output.Append($box.cross)
                }
            }
            [void]$output.AppendLine($box.right_join)
        }

        # Data rows
        for ($rowIdx = 0; $rowIdx -lt $this.Rows.Count; $rowIdx++) {
            $row = $this.Rows[$rowIdx]

            [void]$output.Append($box.vertical)
            for ($i = 0; $i -lt $this.Columns.Count; $i++) {
                $column = $this.Columns[$i]
                $cellValue = if ($i -lt $row.Count) { $row[$i] } else { "" }
                $text = $this.AlignText($cellValue, $widths[$i], $column.Align)

                if ($column.Style) {
                    $text = $column.Style.Apply($text)
                } elseif ($this.RowStyle) {
                    $text = $this.RowStyle.Apply($text)
                }

                [void]$output.Append(" $text ")
                [void]$output.Append($box.vertical)
            }
            [void]$output.AppendLine()

            # Row separator (if ShowLines is true)
            if ($this.ShowLines -and $rowIdx -lt $this.Rows.Count - 1) {
                [void]$output.Append($box.left_join)
                for ($i = 0; $i -lt $widths.Count; $i++) {
                    [void]$output.Append($box.horizontal * ($widths[$i] + 2))
                    if ($i -lt $widths.Count - 1) {
                        [void]$output.Append($box.cross)
                    }
                }
                [void]$output.AppendLine($box.right_join)
            }
        }

        # Bottom border
        [void]$output.Append($box.bottom_left)
        for ($i = 0; $i -lt $widths.Count; $i++) {
            [void]$output.Append($box.horizontal * ($widths[$i] + 2))
            if ($i -lt $widths.Count - 1) {
                [void]$output.Append($box.bottom_join)
            }
        }
        [void]$output.Append($box.bottom_right)

        return $output.ToString()
    }
}

# Helper function to create and render a table
function New-RichTable {
    param(
        [string]$Title,
        [string]$BoxStyle = "rounded",
        [switch]$ShowLines,
        [switch]$HideHeader
    )

    $table = [RichTable]::new()
    if ($Title) { $table.Title = $Title }
    $table.BoxStyle = $BoxStyle
    $table.ShowLines = $ShowLines.IsPresent
    $table.ShowHeader = -not $HideHeader.IsPresent

    return $table
}
