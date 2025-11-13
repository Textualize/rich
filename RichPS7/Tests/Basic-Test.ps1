#!/usr/bin/env pwsh
#Requires -Version 7.0

# Basic functionality test for RichPS7

Write-Host "=== RichPS7 Basic Functionality Test ===`n" -ForegroundColor Cyan

$testsPassed = 0
$testsFailed = 0

function Test-Feature {
    param(
        [string]$Name,
        [scriptblock]$Test
    )

    Write-Host "Testing: $Name ... " -NoNewline

    try {
        & $Test
        Write-Host "PASS" -ForegroundColor Green
        $script:testsPassed++
        return $true
    } catch {
        Write-Host "FAIL" -ForegroundColor Red
        Write-Host "  Error: $_" -ForegroundColor Red
        $script:testsFailed++
        return $false
    }
}

# Import module
Write-Host "Importing RichPS7 module...`n"
try {
    Import-Module "$PSScriptRoot/../RichPS7.psd1" -Force
    Write-Host "Module imported successfully!`n" -ForegroundColor Green
} catch {
    Write-Host "Failed to import module: $_" -ForegroundColor Red
    exit 1
}

# Test 1: Color creation
Test-Feature "Color creation (named)" {
    $color = New-RichColor 'red'
    if (-not $color) { throw "Color creation failed" }
    if ($color.Red -ne 255) { throw "Red value incorrect" }
}

Test-Feature "Color creation (hex)" {
    $color = New-RichColor '#FF5733'
    if (-not $color) { throw "Hex color creation failed" }
}

Test-Feature "Color creation (RGB)" {
    $color = [RichColor]::new(100, 150, 200)
    if ($color.Red -ne 100) { throw "RGB color creation failed" }
}

# Test 2: Style creation
Test-Feature "Style creation" {
    $style = New-RichStyle -Bold -Italic
    if (-not $style.Bold) { throw "Bold not set" }
    if (-not $style.Italic) { throw "Italic not set" }
}

Test-Feature "Style with colors" {
    $style = New-RichStyle -ForegroundColor (New-RichColor 'cyan')
    if (-not $style.ForegroundColor) { throw "Foreground color not set" }
}

# Test 3: Console
Test-Feature "Console instance" {
    $console = Get-RichConsole
    if (-not $console) { throw "Console not created" }
}

# Test 4: Table creation
Test-Feature "Table creation" {
    $table = New-RichTable
    if (-not $table) { throw "Table creation failed" }
}

Test-Feature "Table with columns and rows" {
    $table = New-RichTable
    $table.AddColumn("Col1")
    $table.AddColumn("Col2")
    $table.AddRow(@("A", "B"))

    if ($table.Columns.Count -ne 2) { throw "Column count incorrect" }
    if ($table.Rows.Count -ne 1) { throw "Row count incorrect" }
}

Test-Feature "Table rendering" {
    $table = New-RichTable
    $table.AddColumn("Test")
    $table.AddRow(@("Value"))
    $output = $table.Render()

    if (-not $output) { throw "Table rendering failed" }
    if ($output.Length -lt 10) { throw "Table output too short" }
}

# Test 5: Panel creation
Test-Feature "Panel creation" {
    $panel = New-RichPanel -Content "Test"
    if (-not $panel) { throw "Panel creation failed" }
}

Test-Feature "Panel rendering" {
    $panel = New-RichPanel -Content "Test content"
    $output = $panel.Render()

    if (-not $output) { throw "Panel rendering failed" }
    if ($output.Length -lt 10) { throw "Panel output too short" }
}

Test-Feature "Panel with title" {
    $panel = New-RichPanel -Content "Test" -Title "Title"
    if ($panel.Title -ne "Title") { throw "Panel title not set" }
}

# Test 6: Progress
Test-Feature "Progress creation" {
    $progress = New-RichProgress
    if (-not $progress) { throw "Progress creation failed" }
}

Test-Feature "Progress task creation" {
    $progress = New-RichProgress
    $task = $progress.AddTask("Test", 100)

    if (-not $task) { throw "Task creation failed" }
    if ($task.Total -ne 100) { throw "Task total incorrect" }
}

Test-Feature "Progress advancement" {
    $progress = New-RichProgress
    $task = $progress.AddTask("Test", 100)
    $task.Advance(50)

    if ($task.Current -ne 50) { throw "Task advancement failed" }
}

# Test 7: Write-Rich function
Test-Feature "Write-Rich function exists" {
    $command = Get-Command Write-Rich -ErrorAction SilentlyContinue
    if (-not $command) { throw "Write-Rich function not found" }
}

# Summary
Write-Host "`n=== Test Summary ===" -ForegroundColor Cyan
Write-Host "Tests Passed: $testsPassed" -ForegroundColor Green
Write-Host "Tests Failed: $testsFailed" -ForegroundColor $(if ($testsFailed -gt 0) { 'Red' } else { 'Green' })

if ($testsFailed -eq 0) {
    Write-Host "`nAll tests passed! ✓" -ForegroundColor Green
    exit 0
} else {
    Write-Host "`nSome tests failed! ✗" -ForegroundColor Red
    exit 1
}
