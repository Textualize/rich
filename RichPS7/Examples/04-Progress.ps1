#!/usr/bin/env pwsh
#Requires -Version 7.0

# Example 4: Using Progress Bars with RichPS7

# Import the module
Import-Module "$PSScriptRoot/../RichPS7.psd1" -Force

Write-Host "`n=== RichPS7 Progress Examples ===`n" -ForegroundColor Cyan

# Example 1: Simple progress with Invoke-RichProgress
Write-Host "--- Simple Progress Example ---`n"

$items = 1..20
Invoke-RichProgress -Description "Processing items" -Collection $items -ScriptBlock {
    param($item)
    # Simulate some work
    Start-Sleep -Milliseconds 100
}

Write-Host "`n--- Multiple Tasks ---`n"

# Example 2: Multiple progress bars
$progress = New-RichProgress

# Add multiple tasks
$task1 = $progress.AddTask("Downloading files", 50)
$task2 = $progress.AddTask("Processing data", 100)
$task3 = $progress.AddTask("Uploading results", 30)

$progress.Start()

try {
    # Simulate progress on multiple tasks
    $random = [Random]::new()

    while (-not $progress.IsComplete()) {
        # Randomly advance tasks
        if (-not $task1.IsComplete) {
            $task1.Advance($random.Next(1, 5))
        }

        if (-not $task2.IsComplete) {
            $task2.Advance($random.Next(1, 3))
        }

        if (-not $task3.IsComplete) {
            $task3.Advance($random.Next(1, 4))
        }

        # Refresh display
        $progress.Refresh()

        # Small delay
        Start-Sleep -Milliseconds 50
    }

    # Show final state
    $progress.Refresh()
    Start-Sleep -Milliseconds 500

} finally {
    $progress.Stop()
}

Write-Host "`n--- File Processing Simulation ---`n"

# Example 3: Simulating file processing
$files = @(
    "document1.pdf"
    "document2.pdf"
    "document3.pdf"
    "spreadsheet1.xlsx"
    "spreadsheet2.xlsx"
    "presentation1.pptx"
    "presentation2.pptx"
    "image1.jpg"
    "image2.jpg"
    "image3.jpg"
)

Invoke-RichProgress -Description "Converting files" -Collection $files -ScriptBlock {
    param($file)
    # Simulate file processing time based on extension
    $delay = switch -Regex ($file) {
        '\.pdf$' { 200 }
        '\.xlsx$' { 150 }
        '\.pptx$' { 180 }
        '\.jpg$' { 50 }
        default { 100 }
    }
    Start-Sleep -Milliseconds $delay
}

Write-Host "`n--- Custom Progress Bar ---`n"

# Example 4: Single task with manual updates
$progress2 = New-RichProgress
$task = $progress2.AddTask("Installing packages", 10)

# Customize colors
$task.CompleteColor = New-RichColor 'cyan'
$task.RemainingColor = New-RichColor 'bright_black'

$progress2.Start()

try {
    $packages = @(
        "core-utils"
        "network-tools"
        "security-suite"
        "dev-dependencies"
        "runtime-libraries"
        "documentation"
        "examples"
        "tests"
        "benchmarks"
        "tools"
    )

    foreach ($pkg in $packages) {
        $task.Description = "Installing $pkg".PadRight(30)
        $progress2.Refresh()
        Start-Sleep -Milliseconds ([Random]::new().Next(100, 300))
        $task.Advance(1)
    }

    $task.Description = "Installation complete!".PadRight(30)
    $progress2.Refresh()
    Start-Sleep -Milliseconds 500

} finally {
    $progress2.Stop()
}

Write-Host ""
