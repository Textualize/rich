#!/usr/bin/env pwsh
#Requires -Version 7.0

# Example 3: Using Panels with RichPS7

# Import the module
Import-Module "$PSScriptRoot/../RichPS7.psd1" -Force

Write-Host "`n=== RichPS7 Panel Examples ===`n" -ForegroundColor Cyan

# Example 1: Simple panel
Write-Host "--- Simple Panel ---`n"

$panel1 = New-RichPanel -Content "This is a simple panel with default styling."
Write-Host $panel1.Render()

# Example 2: Panel with title
Write-Host "`n--- Panel with Title ---`n"

$panel2 = New-RichPanel -Content "This panel has a title!" -Title "Welcome"
Write-Host $panel2.Render()

# Example 3: Different box styles
Write-Host "`n--- Different Box Styles ---`n"

foreach ($style in @('rounded', 'square', 'double', 'heavy')) {
    $content = "This panel uses the '$style' box style."
    $panel = New-RichPanel -Content $content -Title $style.ToUpper() -BoxStyle $style
    Write-Host $panel.Render()
    Write-Host ""
}

# Example 4: Panel with title alignment
Write-Host "`n--- Title Alignment ---`n"

$panel3 = New-RichPanel -Content "Left-aligned title" -Title "LEFT" -TitleAlign "left"
Write-Host $panel3.Render()
Write-Host ""

$panel4 = New-RichPanel -Content "Center-aligned title" -Title "CENTER" -TitleAlign "center"
Write-Host $panel4.Render()
Write-Host ""

$panel5 = New-RichPanel -Content "Right-aligned title" -Title "RIGHT" -TitleAlign "right"
Write-Host $panel5.Render()

# Example 5: Panel with subtitle
Write-Host "`n--- Panel with Subtitle ---`n"

$panel6 = New-RichPanel -Content "This panel has both a title and a subtitle." -Title "Main Title" -Subtitle "Subtitle here"
Write-Host $panel6.Render()

# Example 6: Multi-line content
Write-Host "`n--- Multi-line Content ---`n"

$content = @"
This panel contains multiple lines of text.
Each line is displayed within the panel.
You can include as many lines as you want!

This is useful for displaying:
- Instructions
- Status messages
- Help text
- And much more!
"@

$panel7 = New-RichPanel -Content $content -Title "Multi-line Panel" -BoxStyle "double"
Write-Host $panel7.Render()

# Example 7: Styled panels
Write-Host "`n--- Styled Panels ---`n"

$titleStyle = New-RichStyle -ForegroundColor (New-RichColor 'yellow') -Bold
$borderStyle = New-RichStyle -ForegroundColor (New-RichColor 'cyan')
$contentStyle = New-RichStyle -ForegroundColor (New-RichColor 'green')

$panel8 = New-RichPanel -Content "This panel has custom styles!" -Title "Styled Panel" -TitleStyle $titleStyle -BorderStyle $borderStyle -ContentStyle $contentStyle
Write-Host $panel8.Render()

# Example 8: Information panel
Write-Host "`n--- Information Panel ---`n"

$info = @"
PowerShell Version: $($PSVersionTable.PSVersion)
OS: $($PSVersionTable.OS)
Edition: $($PSVersionTable.PSEdition)
"@

$panel9 = New-RichPanel -Content $info -Title "System Information" -BoxStyle "rounded" -Padding 2
Write-Host $panel9.Render()

Write-Host ""
