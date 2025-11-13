@{
    # Script module or binary module file associated with this manifest.
    RootModule = 'RichPS7.psm1'

    # Version number of this module.
    ModuleVersion = '0.1.0'

    # ID used to uniquely identify this module
    GUID = 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'

    # Author of this module
    Author = 'RichPS7 Contributors'

    # Company or vendor of this module
    CompanyName = 'Community'

    # Copyright statement for this module
    Copyright = '(c) 2025 RichPS7 Contributors. MIT License.'

    # Description of the functionality provided by this module
    Description = 'A PowerShell 7 port of Pythons Rich library - Beautiful terminal formatting with colors, tables, panels, and progress bars. Provides ANSI styling, advanced text formatting, and rich UI components for the terminal.'

    # Minimum version of the PowerShell engine required by this module
    PowerShellVersion = '7.0'

    # Functions to export from this module
    FunctionsToExport = @(
        'New-RichColor'
        'New-RichStyle'
        'Get-RichConsole'
        'Write-Rich'
        'New-RichTable'
        'New-RichPanel'
        'New-RichProgress'
        'Invoke-RichProgress'
    )

    # Cmdlets to export from this module
    CmdletsToExport = @()

    # Variables to export from this module
    VariablesToExport = @('RichConsole')

    # Aliases to export from this module
    AliasesToExport = @()

    # Private data to pass to the module specified in RootModule/ModuleToProcess
    PrivateData = @{
        PSData = @{
            # Tags applied to this module
            Tags = @('Terminal', 'Console', 'Formatting', 'ANSI', 'Colors', 'Rich', 'UI', 'Table', 'Progress', 'Panel')

            # A URL to the license for this module.
            LicenseUri = 'https://opensource.org/licenses/MIT'

            # A URL to the main website for this project.
            ProjectUri = 'https://github.com/Textualize/rich'

            # ReleaseNotes of this module
            ReleaseNotes = @'
## Version 0.1.0 - Initial Release

Core Features:
- ANSI color support with RGB, named colors, and hex codes
- Text styling (bold, italic, underline, strike, dim)
- Console output with styled text
- Table rendering with multiple box styles and alignment
- Panel components with titles and borders
- Progress bars with ETA estimation
- Cross-platform support (PowerShell 7+)

Components:
- RichColor: Color handling and ANSI code generation
- RichStyle: Text styling and formatting
- RichConsole: Main console output interface
- RichTable: Table rendering with borders
- RichPanel: Panel components with decorative borders
- RichProgress: Progress tracking and display

This is a port of the Python Rich library's core functionality to PowerShell 7.
'@
        }
    }
}
