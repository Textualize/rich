#Requires -Version 7.0

# RichPS7 - A PowerShell 7 port of Python's Rich library
# Beautiful terminal formatting for PowerShell

# Import classes in order (dependencies first)
. $PSScriptRoot\Classes\Color.ps1
. $PSScriptRoot\Classes\Style.ps1
. $PSScriptRoot\Classes\Console.ps1
. $PSScriptRoot\Classes\Table.ps1
. $PSScriptRoot\Classes\Panel.ps1
. $PSScriptRoot\Classes\Progress.ps1

# Export functions
Export-ModuleMember -Function @(
    'New-RichColor'
    'New-RichStyle'
    'Get-RichConsole'
    'Write-Rich'
    'New-RichTable'
    'New-RichPanel'
    'New-RichProgress'
    'Invoke-RichProgress'
)

# Export the global console variable
Export-ModuleMember -Variable 'RichConsole'

# Module initialization message
Write-Host "RichPS7 module loaded. " -NoNewline
Write-Host "Beautiful terminal formatting for PowerShell 7!" -ForegroundColor Cyan
Write-Host "Get started with: " -NoNewline
Write-Host "Get-Command -Module RichPS7" -ForegroundColor Yellow
