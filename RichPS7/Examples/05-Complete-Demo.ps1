#!/usr/bin/env pwsh
#Requires -Version 7.0

# Example 5: Complete RichPS7 Demo - All Features

# Import the module
Import-Module "$PSScriptRoot/../RichPS7.psd1" -Force

$console = Get-RichConsole

# Clear screen
$console.Clear()

# Title
$console.NewLine()
$titleStyle = New-RichStyle -ForegroundColor (New-RichColor 'cyan') -Bold
Write-Rich "╔══════════════════════════════════════════════════════════╗" -Style $titleStyle
Write-Rich "║           RichPS7 - Complete Feature Demo               ║" -Style $titleStyle
Write-Rich "║     Beautiful Terminal Formatting for PowerShell 7      ║" -Style $titleStyle
Write-Rich "╚══════════════════════════════════════════════════════════╝" -Style $titleStyle
$console.NewLine()

# Introduction panel
$intro = @"
Welcome to RichPS7!

This demo showcases all the core features:
• Colors and text styling
• Tables with various formats
• Panels with borders
• Progress bars with ETA
"@

$panel = New-RichPanel -Content $intro -Title "Introduction" -BoxStyle "rounded"
Write-Host $panel.Render()

Start-Sleep -Seconds 2

# Rule separator
$console.NewLine()
$console.Rule("FEATURE 1: Colors & Styles", (New-RichColor 'yellow'))
$console.NewLine()

# Color demonstration
Write-Rich "Bold text example" -Bold
Write-Rich "Italic text example" -Italic
Write-Rich "Underlined text example" -Underline

$console.NewLine()
Write-Rich "Rainbow colors:" -Bold

$colors = @('red', 'yellow', 'green', 'cyan', 'blue', 'magenta')
foreach ($color in $colors) {
    Write-Rich "● " -Color (New-RichColor $color) -NoNewline
}
$console.NewLine(2)

Start-Sleep -Seconds 2

# Table demonstration
$console.Rule("FEATURE 2: Tables", (New-RichColor 'green'))
$console.NewLine()

$table = New-RichTable -Title "System Resources" -BoxStyle "double"
$table.AddColumn("Resource", @{ Align = 'left' })
$table.AddColumn("Usage", @{ Align = 'right' })
$table.AddColumn("Status", @{ Align = 'center' })

# Get actual system info
$cpu = Get-Counter '\Processor(_Total)\% Processor Time' -ErrorAction SilentlyContinue
$cpuUsage = if ($cpu) { [math]::Round($cpu.CounterSamples.CookedValue, 1) } else { "N/A" }

$memory = Get-CimInstance -ClassName Win32_OperatingSystem -ErrorAction SilentlyContinue
if (-not $memory) {
    # Try Linux approach
    $memInfo = Get-Content /proc/meminfo -ErrorAction SilentlyContinue
    if ($memInfo) {
        $total = ($memInfo | Select-String "MemTotal" | ForEach-Object { ($_ -split '\s+')[1] }) / 1024
        $available = ($memInfo | Select-String "MemAvailable" | ForEach-Object { ($_ -split '\s+')[1] }) / 1024
        $memUsage = [math]::Round((($total - $available) / $total) * 100, 1)
    } else {
        $memUsage = "N/A"
    }
} else {
    $memUsage = [math]::Round((($memory.TotalVisibleMemorySize - $memory.FreePhysicalMemory) / $memory.TotalVisibleMemorySize) * 100, 1)
}

$diskUsage = "N/A"
try {
    $disk = Get-PSDrive -Name C -ErrorAction SilentlyContinue
    if ($disk) {
        $diskUsage = [math]::Round(($disk.Used / ($disk.Used + $disk.Free)) * 100, 1)
    } else {
        # Try Linux root
        $disk = Get-PSDrive -Name / -ErrorAction SilentlyContinue
        if ($disk) {
            $diskUsage = [math]::Round(($disk.Used / ($disk.Used + $disk.Free)) * 100, 1)
        }
    }
} catch {
    $diskUsage = "N/A"
}

$table.AddRow(@("CPU", "$cpuUsage%", "OK"))
$table.AddRow(@("Memory", "$memUsage%", "OK"))
$table.AddRow(@("Disk", "$diskUsage%", "OK"))
$table.AddRow(@("Network", "12.5 Mbps", "OK"))

Write-Host $table.Render()

$console.NewLine()
Start-Sleep -Seconds 2

# Panel demonstration
$console.Rule("FEATURE 3: Panels", (New-RichColor 'magenta'))
$console.NewLine()

$infoContent = @"
Current Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
User: $env:USER
PowerShell: $($PSVersionTable.PSVersion)
"@

$infoPanel = New-RichPanel -Content $infoContent -Title "Session Info" -BoxStyle "heavy" -TitleAlign "center"
Write-Host $infoPanel.Render()

$console.NewLine()
Start-Sleep -Seconds 2

# Progress demonstration
$console.Rule("FEATURE 4: Progress Bars", (New-RichColor 'cyan'))
$console.NewLine()

Write-Host "Simulating a download process...`n"

$progress = New-RichProgress

$download = $progress.AddTask("Downloading package", 100)
$extract = $progress.AddTask("Extracting files", 50)
$install = $progress.AddTask("Installing", 25)

$download.CompleteColor = New-RichColor 'green'
$extract.CompleteColor = New-RichColor 'cyan'
$install.CompleteColor = New-RichColor 'yellow'

$progress.Start()

try {
    # Simulate download
    while ($download.Current -lt $download.Total) {
        $download.Advance([Random]::new().Next(2, 8))
        $progress.Refresh()
        Start-Sleep -Milliseconds 30
    }

    # Simulate extract
    while ($extract.Current -lt $extract.Total) {
        $extract.Advance([Random]::new().Next(1, 5))
        $progress.Refresh()
        Start-Sleep -Milliseconds 50
    }

    # Simulate install
    while ($install.Current -lt $install.Total) {
        $install.Advance([Random]::new().Next(1, 3))
        $progress.Refresh()
        Start-Sleep -Milliseconds 80
    }

    $progress.Refresh()
    Start-Sleep -Milliseconds 500

} finally {
    $progress.Stop()
}

# Completion message
$console.NewLine()
$console.Rule("Demo Complete!", (New-RichColor 'green'))
$console.NewLine()

$outro = @"
Thank you for trying RichPS7!

To get started:
  Import-Module RichPS7
  Get-Command -Module RichPS7

Check out the Examples directory for more demos.
"@

$outroPanel = New-RichPanel -Content $outro -Title "Next Steps" -Subtitle "Happy Scripting!" -BoxStyle "rounded"
Write-Host $outroPanel.Render()

$console.NewLine()
$console.Success("Demo completed successfully!")
$console.NewLine()
