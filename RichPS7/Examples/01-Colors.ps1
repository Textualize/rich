#!/usr/bin/env pwsh
#Requires -Version 7.0

# Example 1: Using Colors with RichPS7

# Import the module
Import-Module "$PSScriptRoot/../RichPS7.psd1" -Force

Write-Host "`n=== RichPS7 Color Examples ===`n" -ForegroundColor Cyan

# Example 1: Named colors
Write-Rich "This is red text" -Color (New-RichColor 'red')
Write-Rich "This is green text" -Color (New-RichColor 'green')
Write-Rich "This is blue text" -Color (New-RichColor 'blue')
Write-Rich "This is yellow text" -Color (New-RichColor 'yellow')
Write-Rich "This is magenta text" -Color (New-RichColor 'magenta')
Write-Rich "This is cyan text" -Color (New-RichColor 'cyan')

Write-Host "`n--- Bright Colors ---`n"

Write-Rich "This is bright red" -Color (New-RichColor 'bright_red')
Write-Rich "This is bright green" -Color (New-RichColor 'bright_green')
Write-Rich "This is bright blue" -Color (New-RichColor 'bright_blue')

Write-Host "`n--- Hex Colors ---`n"

Write-Rich "This is orange (#FFA500)" -Color (New-RichColor '#FFA500')
Write-Rich "This is purple (#9B59B6)" -Color (New-RichColor '#9B59B6')
Write-Rich "This is pink (#FF69B4)" -Color (New-RichColor '#FF69B4')

Write-Host "`n--- RGB Colors ---`n"

$color1 = [RichColor]::new(255, 100, 50)  # Orange-red
Write-Rich "Custom RGB: (255, 100, 50)" -Color $color1

$color2 = [RichColor]::new(50, 200, 150)  # Teal
Write-Rich "Custom RGB: (50, 200, 150)" -Color $color2

Write-Host "`n--- Text Styles ---`n"

Write-Rich "Bold text" -Bold
Write-Rich "Italic text" -Italic
Write-Rich "Underlined text" -Underline
Write-Rich "Bold + Italic + Underline" -Bold -Italic -Underline

Write-Host "`n--- Combined Styles ---`n"

$style1 = New-RichStyle -ForegroundColor (New-RichColor 'cyan') -Bold
Write-Rich "Bold Cyan Text" -Style $style1

$style2 = New-RichStyle -ForegroundColor (New-RichColor 'yellow') -BackgroundColor (New-RichColor 'blue') -Bold
Write-Rich "Yellow on Blue Background" -Style $style2

$style3 = New-RichStyle -ForegroundColor (New-RichColor '#FF1493') -Italic -Underline
Write-Rich "Hot Pink with Italic and Underline" -Style $style3

Write-Host "`n--- Using the Console Object ---`n"

$console = Get-RichConsole
$console.Info("This is an info message")
$console.Warning("This is a warning message")
$console.Error("This is an error message")
$console.Success("This is a success message")

Write-Host ""
