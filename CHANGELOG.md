# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.1] - 2020-05-10

### Added

- `build` target to Makefile
- `codecov` step in github workflow

### Fixed

- fixed code coverage
- fixed generating docs in Makefile
- cleaned the github workflow

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
