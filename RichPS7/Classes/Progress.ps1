class RichProgressBar {
    [string]$Description
    [int]$Total
    [int]$Current
    [bool]$IsComplete
    [datetime]$StartTime
    [RichColor]$CompleteColor
    [RichColor]$RemainingColor
    [int]$Width

    RichProgressBar([string]$description, [int]$total) {
        $this.Description = $description
        $this.Total = $total
        $this.Current = 0
        $this.IsComplete = $false
        $this.StartTime = Get-Date
        $this.Width = 40
        $this.CompleteColor = New-RichColor 'green'
        $this.RemainingColor = New-RichColor 'bright_black'
    }

    # Update progress
    [void] Update([int]$value) {
        $this.Current = [Math]::Min($value, $this.Total)
        $this.IsComplete = ($this.Current -ge $this.Total)
    }

    [void] Advance([int]$delta) {
        $this.Update($this.Current + $delta)
    }

    # Get percentage complete
    [double] GetPercentage() {
        if ($this.Total -eq 0) { return 100.0 }
        return ($this.Current / $this.Total) * 100.0
    }

    # Get elapsed time
    [timespan] GetElapsed() {
        return (Get-Date) - $this.StartTime
    }

    # Estimate remaining time
    [timespan] GetEstimatedRemaining() {
        if ($this.Current -eq 0) {
            return [timespan]::Zero
        }

        $elapsed = $this.GetElapsed()
        $rate = $this.Current / $elapsed.TotalSeconds

        if ($rate -eq 0) {
            return [timespan]::Zero
        }

        $remaining = $this.Total - $this.Current
        $seconds = $remaining / $rate

        return [timespan]::FromSeconds($seconds)
    }

    # Format time span
    hidden [string] FormatTimeSpan([timespan]$ts) {
        if ($ts.TotalHours -ge 1) {
            return "{0:D2}:{1:D2}:{2:D2}" -f [Math]::Floor($ts.TotalHours), $ts.Minutes, $ts.Seconds
        } elseif ($ts.TotalMinutes -ge 1) {
            return "{0:D2}:{1:D2}" -f $ts.Minutes, $ts.Seconds
        } else {
            return "{0:D2}s" -f $ts.Seconds
        }
    }

    # Render the progress bar
    [string] Render() {
        $percentage = $this.GetPercentage()
        $filled = [Math]::Floor($this.Width * ($percentage / 100.0))
        $remaining = $this.Width - $filled

        # Build the bar
        $completeStyle = [RichStyle]::new()
        $completeStyle.ForegroundColor = $this.CompleteColor

        $remainingStyle = [RichStyle]::new()
        $remainingStyle.ForegroundColor = $this.RemainingColor

        $bar = $completeStyle.Apply('█' * $filled) + $remainingStyle.Apply('░' * $remaining)

        # Build the info text
        $elapsed = $this.FormatTimeSpan($this.GetElapsed())
        $eta = if ($this.IsComplete) {
            "Done"
        } else {
            $this.FormatTimeSpan($this.GetEstimatedRemaining())
        }

        $percentText = "{0,5:F1}%" -f $percentage
        $countText = "$($this.Current)/$($this.Total)"

        # Combine everything
        return "$($this.Description.PadRight(30)) [$bar] $percentText $countText ETA: $eta"
    }
}

class RichProgress {
    [System.Collections.ArrayList]$Tasks
    [bool]$IsLive
    [int]$LastLineCount

    RichProgress() {
        $this.Tasks = [System.Collections.ArrayList]::new()
        $this.IsLive = $false
        $this.LastLineCount = 0
    }

    # Add a task
    [RichProgressBar] AddTask([string]$description, [int]$total) {
        $task = [RichProgressBar]::new($description, $total)
        [void]$this.Tasks.Add($task)
        return $task
    }

    # Start live display
    [void] Start() {
        $this.IsLive = $true
        [Console]::CursorVisible = $false
    }

    # Stop live display
    [void] Stop() {
        $this.IsLive = $false
        [Console]::CursorVisible = $true
    }

    # Render all tasks
    [string] Render() {
        $output = [System.Text.StringBuilder]::new()

        foreach ($task in $this.Tasks) {
            [void]$output.AppendLine($task.Render())
        }

        return $output.ToString().TrimEnd()
    }

    # Update the display
    [void] Refresh() {
        if (-not $this.IsLive) { return }

        # Move cursor up to overwrite previous output
        if ($this.LastLineCount -gt 0) {
            for ($i = 0; $i -lt $this.LastLineCount; $i++) {
                Write-Host "`e[1A`e[2K" -NoNewline
            }
        }

        # Render and display
        $output = $this.Render()
        Write-Host $output

        # Track how many lines we wrote
        $this.LastLineCount = ($output -split "`n").Count
    }

    # Check if all tasks are complete
    [bool] IsComplete() {
        foreach ($task in $this.Tasks) {
            if (-not $task.IsComplete) {
                return $false
            }
        }
        return $true
    }
}

# Helper function to create a progress display
function New-RichProgress {
    return [RichProgress]::new()
}

# Helper function for simple progress tracking
function Invoke-RichProgress {
    param(
        [Parameter(Mandatory)]
        [string]$Description,

        [Parameter(Mandatory)]
        [array]$Collection,

        [Parameter(Mandatory)]
        [scriptblock]$ScriptBlock
    )

    $progress = [RichProgress]::new()
    $task = $progress.AddTask($Description, $Collection.Count)

    $progress.Start()

    try {
        foreach ($item in $Collection) {
            $progress.Refresh()

            # Execute the script block
            & $ScriptBlock $item

            $task.Advance(1)
        }

        $progress.Refresh()
        Start-Sleep -Milliseconds 500  # Show final state
    } finally {
        $progress.Stop()
    }
}
