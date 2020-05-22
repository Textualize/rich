# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.1] - 2020-05-22

### Fixed

- Issue with sum and Style

## [1.2.0] - 2020-05-22

### Added

- Support for double underline, framed, encircled, and overlined attributes

### Changed

- Optimized Style
- Changed methods `__console__` to `__rich_console__`, and `__measure__` to `__rich_measure__`

## [1.1.9] - 2020-05-20

### Fixed

- Exception when BarColumn.bar_width == None

## [1.1.8] - 2020-05-20

### Changed

- Optimizations for Segment, Console and Table

### Added

- Added Console.clear method
- Added exporting of links to HTML

## [1.1.7] - 2020-05-19

### Added

- Added collapse_padding option to Table.

### Changed

- Some style attributes may be abbreviated (b for bold, i for italic etc). Previously abbreviations worked in console markup but only one at a time, i.e. "[b]Hello[/]" but not "[b i]Hello[/]" -- now they work everywhere.
- Renamed 'text' property on Text to 'plain'. i.e. text.plain returns a string version of the Text instance.

### Fixed

- Fixed zero division if total is 0 in progress bar

## [1.1.6] - 2020-05-17

### Added

- Added rich.align.Align class
- Added justify argument to Console.print and console.log

## [1.1.5] - 2020-05-15

### Changed

- Changed progress bars to write to stdout on terminal and hide on non-terminal

## [1.1.4] - 2020-05-15

### Fixed

- Fixed incorrect file and link in progress.log
- Fixes for legacy windows: Bar, Panel, and Rule now use ASCII characters
- show_cursor is now a no-op on legacy windows

### Added

- Added Console.input

### Changed

- Disable progress bars when not writing to a terminal

## [1.1.3] - 2020-05-14

### Fixed

- Issue with progress of one line`

## [1.1.2] - 2020-05-14

### Added

- Added -p switch to python -m rich.markdown to page output
- Added Console.control to output control codes

### Changed

- Changed Console log_time_format to no longer require a space at the end
- Added print and log to Progress to render terminal output when progress is active

## [1.1.1] - 2020-05-12

### Changed

- Stripped cursor moving control codes from text

## [1.1.0] - 2020-05-10

### Added

- Added hyperlinks to Style and markup
- Added justify and code theme switches to markdown command

## [1.0.3] - 2020-05-08

### Added

- Added `python -m rich.syntax` command

## [1.0.2] - 2020-05-08

### Fixed

- Issue with Windows legacy support https://github.com/willmcgugan/rich/issues/59

## [1.0.1] - 2020-05-08

### Changed

- Applied console markup after highlighting
- Documented highlighting
- Changed Markup parser to handle overlapping styles
- Relaxed dependency on colorama
- Allowed Theme to accept values as style definitions (str) as well as Style instances
- Added a panel to emphasize code in Markdown

### Added

- Added markup.escape
- Added `python -m rich.theme` command
- Added `python -m rich.markdown` command
- Added rendering of images in Readme (links only)

### Fixed

- Fixed Text.assemble not working with strings https://github.com/willmcgugan/rich/issues/57
- Fixed table when column widths must be compressed to fit

## [1.0.0] - 2020-05-03

### Changed

- Improvements to repr highlighter to highlight URLs

## [0.8.13] - 2020-04-28

### Fixed

- Fixed incorrect markdown rendering for quotes and changed style

## [0.8.12] - 2020-04-21

### Fixed

- Removed debug print from rich.progress

## [0.8.11] - 2020-04-14

### Added

- Added Table.show_lines to render lines between rows

### Changed

- Added markup escape with double square brackets

## [0.8.10] - 2020-04-12

### Fixed

- Fix row_styles applying to header

## [0.8.9] - 2020-04-12

### Changed

- Added force_terminal option to `Console.__init__`

### Added

- Added Table.row_styles to enable zebra striping.

## [0.8.8] - 2020-03-31

### Fixed

- Fixed background in Syntax

## [0.8.7] - 2020-03-31

### Fixed

- Broken wrapping of long lines
- Fixed wrapping in Syntax

### Changed

- Added word_wrap option to Syntax, which defaults to False.
- Added word_wrap option to Traceback.

## [0.8.6] - 2020-03-29

### Added

- Experimental Jupyter notebook support: from rich.jupyter import print

## [0.8.5] - 2020-03-29

### Changed

- Smarter number parsing regex for repr highlighter

### Added

- uuid highlighter for repr

## [0.8.4] - 2020-03-28

### Added

- Added 'test card', run python -m rich

### Changed

- Detected windows terminal, defaulting to colorama support

### Fixed

- Fixed table scaling issue

## [0.8.3] - 2020-03-27

### Fixed

- CJK right align

## [0.8.2] - 2020-03-27

### Changed

- Fixed issue with 0 speed resulting in zero division error
- Changed signature of Progress.update
- Made calling start() a second time a no-op

## [0.8.1] - 2020-03-22

### Added

- Added progress.DownloadColumn

## [0.8.0] - 2020-03-17

### Added

- CJK support
- Console level highlight flag
- Added encoding argument to Syntax.from_path

### Changed

- Dropped support for Windows command prompt (try https://www.microsoft.com/en-gb/p/windows-terminal-preview/)
- Added task_id to Progress.track

## [0.7.2] - 2020-03-15

### Fixed

- KeyError for missing pygments style

## [0.7.1] - 2020-03-13

### Fixed

- Issue with control codes being used in length calculation

### Changed

- Remove current_style concept, which wasn't really used and was problematic for concurrency

## [0.7.0] - 2020-03-12

### Changed

- Added width option to Panel
- Change special method `__render_width__` to `__measure__`
- Dropped the "markdown style" syntax in console markup
- Optimized style rendering

### Added

- Added Console.show_cursor method
- Added Progress bars

### Fixed

- Fixed wrapping when a single word was too large to fit in a line

## [0.6.0] - 2020-03-03

### Added

- Added tab_size to Console and Text
- Added protocol.is_renderable for runtime check
- Added emoji switch to Console
- Added inherit boolean to Theme
- Made Console thread safe, with a thread local buffer

### Changed

- Console.markup attribute now effects Table
- SeparatedConsoleRenderable and RichCast types

### Fixed

- Fixed tabs breaking rendering by converting to spaces

## [0.5.0] - 2020-02-23

### Changed

- Replaced `__console_str__` with `__rich__`

## [0.4.1] - 2020-02-22

### Fixed

- Readme links in Pypi

## [0.4.0] - 2020-02-22

### Added

- Added Traceback rendering and handler
- Added rich.constrain
- Added rich.rule

### Fixed

- Fixed unnecessary padding

## [0.3.3] - 2020-02-04

### Fixed

- Fixed Windows color support
- Fixed line width on windows issue (https://github.com/willmcgugan/rich/issues/7)
- Fixed Pretty print on Windows

## [0.3.2] - 2020-01-26

### Added

- Added rich.logging

## [0.3.1] - 2020-01-22

### Added

- Added colorama for Windows support

## [0.3.0] - 2020-01-19

### Added

- First official release, API still bto be stabilized
