# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [9.2.0] - Unreleased

### Added

- Added tracebacks_show_locals parameter to RichHandler
- Applied dim=True to indent guide styles
- Added max_string to Pretty

## [9.1.0] - 2020-10-23

### Added

- Added Text.with_indentation_guide
- Added Text.detect_indentation
- Added Pretty.indent_guides
- Added Syntax.indent_guides
- Added indent_guides parameter on pretty.install
- Added rich.pretty.pprint
- Added max_length to Pretty

### Changed

- Enabled indent guides on Tracebacks

### Fixed

- Fixed negative time remaining in Progress bars https://github.com/willmcgugan/rich/issues/378

## [9.0.1] - 2020-10-19

### Fixed

- Fixed broken ANSI codes in input on windows legacy https://github.com/willmcgugan/rich/issues/393

## [9.0.0] - 2020-10-18

### Fixed

- Progress download column now displays decimal units

### Added

- Support for Python 3.9
- Added legacy_windows to ConsoleOptions
- Added ascii_only to ConsoleOptions
- Added box.SQUARE_DOUBLE_HEAD
- Added highlighting of EUI-48 and EUI-64 (MAC addresses)
- Added Console.pager
- Added Console.out
- Added binary_units in progress download column
- Added Progress.reset
- Added Style.background_style property
- Added Bar renderable https://github.com/willmcgugan/rich/pull/361
- Added Table.min_width
- Added table.Column.min_width and table.Column.max_width, and same to Table.add_column

### Changed

- Dropped box.get_safe_box function in favor of Box.substitute
- Changed default padding in Panel from 0 to (0, 1) https://github.com/willmcgugan/rich/issues/385
- Table with row_styles will extend background color between cells if the box has no vertical dividerhttps://github.com/willmcgugan/rich/issues/383
- Changed default of fit kwarg in render_group() from False to True
- Renamed rich.bar to rich.progress_bar, and Bar class to ProgressBar, rich.bar is now the new solid bar class

### Fixed

- Fixed typo in `Style.transparent_background` method name.

## [8.0.0] - 2020-10-03

### Added

- Added Console.bell method
- Added Set to types that Console.print will automatically pretty print
- Added show_locals to Traceback
- Added theme stack mechanism, see Console.push_theme and Console.pop_theme

### Changed

- Changed Style.empty to Style.null to better reflect what it does
- Optimized combining styles involving a null style
- Change error messages in Style.parse to read better

### Fixed

- Fixed Table.\_\_rich_measure\_\_
- Fixed incorrect calculation of fixed width columns

## [7.1.0] - 2020-09-26

### Added

- Added Console.begin_capture, Console.end_capture and Console.capture
- Added Table.title_justify and Table.caption_justify https://github.com/willmcgugan/rich/issues/301

### Changed

- Improved formatting of exceptions
- Enabled Rich exceptions in logging https://github.com/taliraj
- UTF-8 encoding is now mentioned in HTML head section

### Removed

- Removed line_numbers argument from traceback.install, which was undocumented and did nothing

## [7.0.0] - 2020-09-18

### Added

- New ansi_dark and ansi_light themes
- Added Text.append_tokens for fast appending of string + Style pairs
- Added Text.remove_suffix
- Added Text.append_tokens

### Changed

- Text.tabs_to_spaces was renamed to Text.expand_tabs, which works in place rather than returning a new instance
- Renamed Column.index to Column.\_index
- Optimized Style.combine and Style.chain
- Optimized text rendering by fixing internal cache mechanism
- Optimized hash generation for Styles

## [6.2.0] - 2020-09-13

### Added

- Added inline code highlighting to Markdown

## [6.1.2] - 2020-09-11

### Added

- Added ipv4 and ipv6 to ReprHighlighter

### Changed

- The `#` sign is included in url highlighting

### Fixed

- Fixed force-color switch in rich.syntax and rich.markdown commands

## [6.1.1] - 2020-09-07

### Changed

- Restored "def" in inspect signature

## [6.1.0] - 2020-09-07

### Added

- New inspect module
- Added os.\_Environ to pretty print

### Fixed

- Prevented recursive renderables from getting stuck

## Changed

- force_terminal and force_jupyter can now be used to force the disabled state, or left as None to auto-detect.
- Panel now expands to fit title if supplied

## [6.0.0] - 2020-08-25

### Fixed

- Fixed use of `__rich__` cast

### Changed

- New algorithm to pretty print which fits more on a line if possible
- Deprecated `character` parameter in Rule and Console.rule, in favor of `characters`
- Optimized Syntax.from_path to avoid searching all lexers, which also speeds up tracebacks

### Added

- Added soft_wrap flag to Console.print

## [5.2.1] - 2020-08-19

### Fixed

- Fixed underscore with display hook https://github.com/willmcgugan/rich/issues/235

## [5.2.0] - 2020-08-14

### Changed

- Added crop argument to Console.print
- Added "ignore" overflow method
- Added multiple characters per rule @hedythedev https://github.com/willmcgugan/rich/pull/207

## [5.1.2] - 2020-08-10

### Fixed

- Further optimized pretty printing ~5X.

## [5.1.1] - 2020-08-09

### Fixed

- Optimized pretty printing ~3X faster

## [5.1.0] - 2020-08-08

### Added

- Added Text.cell_len
- Added helpful message regarding unicode decoding errors https://github.com/willmcgugan/rich/issues/212
- Added display hook with pretty.install()

### Fixed

- Fixed deprecation warnings re backslash https://github.com/willmcgugan/rich/issues/210
- Fixed repr highlighting of scientific notation, e.g. 1e100

### Changed

- Implemented pretty printing, and removed pprintpp from dependencies
- Optimized Text.join

## [5.0.0] - 2020-08-02

### Changed

- Change to console markup syntax to not parse Python structures as markup, i.e. `[1,2,3]` is treated as a literal, not a tag.
- Standard color numbers syntax has changed to `"color(<number>)"` so that `[5]` (for example) is considered a literal.
- Markup escape method has changed from double brackets to preceding with a backslash, so `foo[[]]` would be `foo\[bar]`

## [4.2.2] - 2020-07-30

### Changed

- Added thread to automatically call update() in progress.track(). Replacing previous adaptive algorithm.
- Second attempt at working around https://bugs.python.org/issue37871

## [4.2.1] - 2020-07-29

### Added

- Added show_time and show_level parameters to RichHandler https://github.com/willmcgugan/rich/pull/182

### Fixed

- Fixed progress.track iterator exiting early https://github.com/willmcgugan/rich/issues/189
- Added workaround for Python bug https://bugs.python.org/issue37871, fixing https://github.com/willmcgugan/rich/issues/186

### Changed

- Set overflow=fold for log messages https://github.com/willmcgugan/rich/issues/190

## [4.2.0] - 2020-07-27

### Fixed

- Fixed missing new lines https://github.com/willmcgugan/rich/issues/178
- Fixed Progress.track https://github.com/willmcgugan/rich/issues/184
- Remove control codes from exported text https://github.com/willmcgugan/rich/issues/181
- Implemented auto-detection and color rendition of 16-color mode

## [4.1.0] - 2020-07-26

### Changed

- Optimized progress.track for very quick iterations
- Force default size of 80x25 if get_terminal_size reports size of 0,0

## [4.0.0] - 2020-07-23

Major version bump for a breaking change to `Text.stylize signature`, which corrects a minor but irritating API wart. The style now comes first and the `start` and `end` offsets default to the entire text. This allows for `text.stylize_all(style)` to be replaced with `text.stylize(style)`. The `start` and `end` offsets now support negative indexing, so `text.stylize("bold", -1)` makes the last character bold.

### Added

- Added markup switch to RichHandler https://github.com/willmcgugan/rich/issues/171

### Changed

- Change signature of Text.stylize to accept style first
- Remove Text.stylize_all which is no longer necessary

### Fixed

- Fixed rendering of Confirm prompt https://github.com/willmcgugan/rich/issues/170

## [3.4.1] - 2020-07-22

### Fixed

- Fixed incorrect default of expand in Table.grid

## [3.4.0] - 2020-07-22

### Added

- Added stream parameter to Console.input
- Added password parameter to Console.input
- Added description parameter to Progress.update
- Added rich.prompt
- Added detecting 'dumb' terminals
- Added Text.styled alternative constructor

### Fixes

- Fixed progress bars so that they are readable when color is disabled

## [3.3.2] - 2020-07-14

### Changed

- Optimized Text.pad

### Added

- Added rich.scope
- Change log_locals to use scope.render_scope
- Added title parameter to Columns

## [3.3.1] - 2020-07-13

### Added

- box.ASCII_DOUBLE_HEAD

### Changed

- Removed replace of -- --- ... from Markdown, as it made it impossible to include CLI info

## [3.3.0] - 2020-07-12

### Added

- Added title and title_align options to Panel
- Added pad and width parameters to Align
- Added end parameter to Rule
- Added Text.pad and Text.align methods
- Added leading parameter to Table

## [3.2.0] - 2020-07-10

### Added

- Added Align.left Align.center Align.right shortcuts
- Added Panel.fit shortcut
- Added align parameter to Columns

### Fixed

- Align class now pads to the right, like Text
- ipywidgets added as an optional dependency
- Issue with Panel and background color
- Fixed missing `__bool__` on Segment

### Changed

- Added `border_style` argument to Panel (note, `style` now applies to interior of the panel)

## [3.1.0] - 2020-07-09

### Changed

- Progress bars now work in Jupyter

## Added

- Added refresh_per_second to progress.track
- Added styles to BarColumn and progress.track

## [3.0.5] - 2020-07-07

### Fixed

- Fixed Windows version number require for truecolor

## [3.0.4] - 2020-07-07

### Changed

- More precise detection of Windows console https://github.com/willmcgugan/rich/issues/140

## [3.0.3] - 2020-07-03

### Fixed

- Fixed edge case with wrapped and overflowed text

### Changed

- New algorithm for compressing table that priorities smaller columns

### Added

- Added safe_box parameter to Console constructor

## [3.0.2] - 2020-07-02

### Added

- Added rich.styled.Styled class to apply styles to renderable
- Table.add_row now has an optional style parameter
- Added table_movie.py to examples

### Changed

- Modified box options to use half line characters at edges
- Non no_wrap columns will now shrink below minimum width if table is compressed

## [3.0.1] - 2020-06-30

### Added

- Added box.ASCII2
- Added markup argument to logging extra

### Changed

- Setting a non-None width now implies expand=True

## [3.0.0] - 2020-06-28

### Changed

- Enabled supported box chars for legacy Windows, and introduce `safe_box` flag
- Disable hyperlinks on legacy Windows
- Constructors for Rule and Panel now have keyword only arguments (reason for major version bump)
- Table.add_colum added keyword only arguments

### Fixed

- Fixed Table measure

## [2.3.1] - 2020-06-26

### Fixed

- Disabled legacy_windows if jupyter is detected https://github.com/willmcgugan/rich/issues/125

## [2.3.0] - 2020-06-26

### Fixed

- Fixed highlighting of paths / filenames
- Corrected docs for RichHandler which erroneously said default console writes to stderr

### Changed

- Allowed `style` parameter for `highlight_regex` to be a callable that returns a style

### Added

- Added optional highlighter parameter to RichHandler

## [2.2.6] - 2020-06-24

### Changed

- Store a "link id" on Style instance, so links containing different styles are highlighted together. (https://github.com/willmcgugan/rich/pull/123)

## [2.2.5] - 2020-06-23

### Fixed

- Fixed justify of tables (https://github.com/willmcgugan/rich/issues/117)

## [2.2.4] - 2020-06-21

### Added

- Added enable_link_path to RichHandler
- Added legacy_windows switch to Console constructor

## [2.2.3] - 2020-06-15

### Fixed

- Fixed console.log hyperlink not containing full path

### Changed

- Used random number for hyperlink id

## [2.2.2] - 2020-06-14

### Changed

- Exposed RichHandler highlighter as a class var

## [2.2.1] - 2020-06-14

### Changed

- Linked path in log render to file

## [2.2.0] - 2020-06-14

### Added

- Added redirect_stdout and redirect_stderr to Progress

### Changed

- printing to console with an active Progress doesn't break visuals

## [2.1.0] - 2020-06-11

### Added

- Added 'transient' option to Progress

### Changed

- Truncated overly long text in Rule with ellipsis overflow

## [2.0.1] - 2020-06-10

### Added

- Added expand option to Padding

### Changed

- Some minor optimizations in Text

### Fixed

- Fixed broken rule with CJK text

## [2.0.0] - 2020-06-06

### Added

- Added overflow methods
- Added no_wrap option to print()
- Added width option to print
- Improved handling of compressed tables

### Fixed

- Fixed erroneous space at end of log
- Fixed erroneous space at end of progress bar

### Changed

- Renamed \_ratio.ratio_divide to \_ratio.ratio_distribute
- Renamed JustifyValues to JustifyMethod (backwards incompatible)
- Optimized \_trim_spans
- Enforced keyword args in Console / Text interfaces (backwards incompatible)
- Return self from text.append

## [1.3.1] - 2020-06-01

### Changed

- Changed defaults of Table.grid
- Polished listdir.py example

### Added

- Added width argument to Columns

### Fixed

- Fixed for `columns_first` argument in Columns
- Fixed incorrect padding in columns with fixed width

## [1.3.0] - 2020-05-31

### Added

- Added rich.get_console() function to get global console instance.
- Added Columns class

### Changed

- Updated `markdown.Heading.create()` to work with subclassing.
- Console now transparently works with Jupyter

### Fixed

- Fixed issue with broken table with show_edge=False and a non-None box arg

## [1.2.3] - 2020-05-24

### Added

- Added `padding` parameter to Panel
- Added 'indeterminate' state when progress bars aren't started

### Fixed

- Fixed Progress deadlock https://github.com/willmcgugan/rich/issues/90

### Changed

- Auto-detect "truecolor" color system when in Windows Terminal

## [1.2.2] - 2020-05-22

### Fixed

- Issue with right aligned wrapped text adding extra spaces

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

- First official release, API still to be stabilized
