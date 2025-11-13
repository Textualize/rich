# RichPS7 Quick Start Guide

Get up and running with RichPS7 in 5 minutes!

## Installation

```powershell
# Clone or download, then import
Import-Module ./RichPS7/RichPS7.psd1
```

## 5-Minute Tutorial

### 1. Print Colored Text (30 seconds)

```powershell
# Simple colored text
Write-Rich "Success!" -Color (New-RichColor 'green') -Bold

# Use the console for themed messages
$console = Get-RichConsole
$console.Info("Information message")
$console.Warning("Warning message")
$console.Error("Error message")
$console.Success("Success message")
```

### 2. Create a Table (1 minute)

```powershell
# Create a table
$table = New-RichTable -Title "My First Table"

# Add columns
$table.AddColumn("Name")
$table.AddColumn("Status")
$table.AddColumn("Count")

# Add rows
$table.AddRow(@("Item 1", "Active", "42"))
$table.AddRow(@("Item 2", "Inactive", "17"))
$table.AddRow(@("Item 3", "Active", "99"))

# Render it
Write-Host $table.Render()
```

### 3. Create a Panel (1 minute)

```powershell
# Simple panel
$panel = New-RichPanel -Content "Hello from RichPS7!" -Title "Welcome"
Write-Host $panel.Render()

# Multi-line panel
$content = @"
This is a panel with multiple lines.
You can include any text you want.
Perfect for highlighting important information!
"@

$panel = New-RichPanel -Content $content -Title "Info" -BoxStyle "double"
Write-Host $panel.Render()
```

### 4. Show Progress (1 minute)

```powershell
# Simple progress bar
$items = 1..50
Invoke-RichProgress -Description "Processing" -Collection $items -ScriptBlock {
    param($item)
    Start-Sleep -Milliseconds 50  # Your work here
}
```

### 5. Combine Everything (1.5 minutes)

```powershell
# Clear screen and show a complete example
$console = Get-RichConsole
$console.Clear()

# Title
$console.Rule("System Report", (New-RichColor 'cyan'))
$console.NewLine()

# Info panel
$info = @"
Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
PowerShell: $($PSVersionTable.PSVersion)
"@
$panel = New-RichPanel -Content $info -Title "Report Info"
Write-Host $panel.Render()
$console.NewLine()

# Data table
$table = New-RichTable -Title "System Processes" -BoxStyle "rounded"
$table.AddColumn("Process")
$table.AddColumn("PID", @{ Align = 'right' })
$table.AddColumn("Memory (MB)", @{ Align = 'right' })

Get-Process | Select-Object -First 5 | ForEach-Object {
    $memMB = [math]::Round($_.WS / 1MB, 1)
    $table.AddRow(@($_.ProcessName, $_.Id, $memMB))
}

Write-Host $table.Render()
$console.NewLine()

# Success message
$console.Success("Report generated successfully!")
```

## Next Steps

### Explore Examples

Run the complete demo:

```powershell
./RichPS7/Examples/05-Complete-Demo.ps1
```

Or explore individual examples:
- `01-Colors.ps1` - Colors and text styling
- `02-Tables.ps1` - Table formatting
- `03-Panels.ps1` - Panel styles
- `04-Progress.ps1` - Progress bars

### Customize Your Output

#### Box Styles

Tables and panels support multiple box styles:

```powershell
# Try different styles
foreach ($style in @('rounded', 'square', 'double', 'heavy', 'simple')) {
    $panel = New-RichPanel -Content "Using $style style" -Title $style -BoxStyle $style
    Write-Host $panel.Render()
}
```

#### Color Schemes

Create custom color schemes:

```powershell
# Define your colors
$primary = New-RichColor '#3498db'    # Blue
$success = New-RichColor '#2ecc71'    # Green
$warning = New-RichColor '#f39c12'    # Orange
$danger = New-RichColor '#e74c3c'     # Red

# Use them
Write-Rich "Primary action" -Color $primary -Bold
Write-Rich "Success!" -Color $success
Write-Rich "Warning!" -Color $warning
Write-Rich "Error!" -Color $danger
```

#### Style Presets

Create reusable styles:

```powershell
# Define styles
$headerStyle = New-RichStyle -ForegroundColor (New-RichColor 'cyan') -Bold
$errorStyle = New-RichStyle -ForegroundColor (New-RichColor 'red') -Bold -Underline
$codeStyle = New-RichStyle -ForegroundColor (New-RichColor 'green') -BackgroundColor (New-RichColor 'black')

# Use them
Write-Rich "=== Header ===" -Style $headerStyle
Write-Rich "Error occurred!" -Style $errorStyle
Write-Rich "code snippet" -Style $codeStyle
```

### Real-World Use Cases

#### Script Progress Tracking

```powershell
function Process-Files {
    param([string[]]$Files)

    Invoke-RichProgress -Description "Processing files" -Collection $Files -ScriptBlock {
        param($file)
        # Process each file
        # ...
    }
}
```

#### Status Reports

```powershell
function Show-SystemStatus {
    $console = Get-RichConsole

    $console.Rule("System Status Report", (New-RichColor 'cyan'))
    $console.NewLine()

    # CPU Check
    if ($cpuUsage -lt 80) {
        $console.Success("CPU: OK ($cpuUsage%)")
    } else {
        $console.Warning("CPU: High ($cpuUsage%)")
    }

    # Memory Check
    if ($memUsage -lt 90) {
        $console.Success("Memory: OK ($memUsage%)")
    } else {
        $console.Error("Memory: Critical ($memUsage%)")
    }
}
```

#### Configuration Display

```powershell
function Show-Config {
    param($Config)

    $table = New-RichTable -Title "Configuration" -BoxStyle "double"
    $table.AddColumn("Setting")
    $table.AddColumn("Value")

    foreach ($key in $Config.Keys) {
        $table.AddRow(@($key, $Config[$key]))
    }

    Write-Host $table.Render()
}
```

## Tips & Tricks

1. **Auto-width tables**: Don't specify column widths - they'll auto-size to content
2. **Multi-line panels**: Use here-strings (`@"..."@`) for multi-line panel content
3. **Console theme**: Customize the global console's theme colors
4. **Progress ETA**: Progress bars automatically calculate and display ETA
5. **Style combinations**: You can combine multiple style attributes (bold + italic + color)

## Getting Help

```powershell
# List all available functions
Get-Command -Module RichPS7

# Get help for a specific function
Get-Help New-RichTable -Full
Get-Help Write-Rich -Examples
```

## Troubleshooting

### Colors not showing?

Make sure you're using PowerShell 7+ and a modern terminal:

```powershell
# Check PowerShell version
$PSVersionTable.PSVersion

# Should be 7.0 or higher
```

### Module not loading?

```powershell
# Try explicit import
Import-Module ./RichPS7/RichPS7.psd1 -Force -Verbose

# Check for errors
$Error[0] | Format-List -Force
```

## Ready to Learn More?

Check out the full [README.md](README.md) for complete API documentation and advanced features!

---

Happy scripting with RichPS7! 🎨✨
