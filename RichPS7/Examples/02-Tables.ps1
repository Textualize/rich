#!/usr/bin/env pwsh
#Requires -Version 7.0

# Example 2: Using Tables with RichPS7

# Import the module
Import-Module "$PSScriptRoot/../RichPS7.psd1" -Force

Write-Host "`n=== RichPS7 Table Examples ===`n" -ForegroundColor Cyan

# Example 1: Simple table
Write-Host "--- Simple Table ---`n"

$table1 = New-RichTable -Title "System Information"
$table1.AddColumn("Property")
$table1.AddColumn("Value")

$table1.AddRow(@("OS", $PSVersionTable.OS))
$table1.AddRow(@("PowerShell Version", $PSVersionTable.PSVersion))
$table1.AddRow(@("Edition", $PSVersionTable.PSEdition))
$table1.AddRow(@("Platform", $PSVersionTable.Platform))

Write-Host $table1.Render()

# Example 2: Table with different box styles
Write-Host "`n--- Different Box Styles ---`n"

foreach ($style in @('rounded', 'square', 'double', 'simple')) {
    $table = New-RichTable -BoxStyle $style
    $table.AddColumn("Style")
    $table.AddColumn("Description")
    $table.AddRow(@($style, "This table uses the '$style' box style"))
    Write-Host $table.Render()
    Write-Host ""
}

# Example 3: Table with alignment
Write-Host "`n--- Table with Alignment ---`n"

$table2 = New-RichTable -Title "Product Pricing"
$table2.AddColumn("Product", @{ Align = 'left' })
$table2.AddColumn("Price", @{ Align = 'right' })
$table2.AddColumn("Quantity", @{ Align = 'center' })

$table2.AddRow(@("Widget", "$19.99", "42"))
$table2.AddRow(@("Gadget", "$29.99", "17"))
$table2.AddRow(@("Doohickey", "$9.99", "103"))
$table2.AddRow(@("Thingamajig", "$49.99", "8"))

Write-Host $table2.Render()

# Example 4: Table with row lines
Write-Host "`n--- Table with Row Lines ---`n"

$table3 = New-RichTable -Title "Server Status" -ShowLines
$table3.AddColumn("Server")
$table3.AddColumn("Status")
$table3.AddColumn("Uptime")

$table3.AddRow(@("web-01", "Running", "45d 12h"))
$table3.AddRow(@("web-02", "Running", "32d 8h"))
$table3.AddRow(@("db-01", "Running", "127d 4h"))
$table3.AddRow(@("cache-01", "Stopped", "0d 0h"))

Write-Host $table3.Render()

# Example 5: Process information table
Write-Host "`n--- Process Information ---`n"

$table4 = New-RichTable -Title "Top Processes by Memory" -BoxStyle "double"
$table4.AddColumn("Process", @{ Align = 'left' })
$table4.AddColumn("PID", @{ Align = 'right' })
$table4.AddColumn("Memory (MB)", @{ Align = 'right' })

$processes = Get-Process | Sort-Object -Property WS -Descending | Select-Object -First 5
foreach ($proc in $processes) {
    $memMB = [math]::Round($proc.WS / 1MB, 2)
    $table4.AddRow(@($proc.ProcessName, $proc.Id, $memMB))
}

Write-Host $table4.Render()

Write-Host ""
