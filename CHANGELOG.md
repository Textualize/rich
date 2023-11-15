# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [13.7.0] - 2023-11-15

### Added

- Adds missing parameters to Panel.fit https://github.com/Textualize/rich/issues/3142

### Fixed

- Some text goes missing during wrapping when it contains double width characters https://github.com/Textualize/rich/issues/3176
- Ensure font is correctly inherited in exported HTML https://github.com/Textualize/rich/issues/3104
- Fixed typing for `FloatPrompt`.

## [13.6.0] - 2023-09-30

### Added

- Added Python 3.12 to classifiers.

## [13.5.3] - 2023-09-17

### Fixed

- Markdown table rendering issue with inline styles and links https://github.com/Textualize/rich/issues/3115
- Fix Markdown code blocks on a light background https://github.com/Textualize/rich/issues/3123

## [13.5.2] - 2023-08-01

### Fixed

- Fixed Text.expand_tabs assertion error

## [13.5.1] - 2023-07-31

### Fixed

- Fix tilde character (`~`) not included in link regex when printing to console https://github.com/Textualize/rich/issues/3057

## [13.5.0] - 2023-07-29

### Fixed

- Fixed Text.expand_tabs not expanding spans.
- Fixed TimeElapsedColumn from showing negative.
- Fix for escaping strings with a trailing backslash https://github.com/Textualize/rich/issues/2987
- Fixed exception in Markdown with partial table https://github.com/Textualize/rich/issues/3053
- Fixed the HTML export template so that the `<html>` tag comes before the `<head>` tag https://github.com/Textualize/rich/issues/3021
- Fixed issue with custom classes overwriting `__eq__` https://github.com/Textualize/rich/issues/2875
- Fix rich.pretty.install breakage in iPython https://github.com/Textualize/rich/issues/3013

### Added

- Added Text.extend_style method.
- Added Span.extend method.

### Changed

- Text.tab_size now defaults to `None` to indicate that Console.tab_size should be used.


## [13.4.2] - 2023-06-12

### Changed

- Relaxed markdown-it-py dependency

## [13.4.1] - 2023-05-31

### Fixed

- Fixed typing extensions import in markdown https://github.com/Textualize/rich/issues/2979

## [13.4.0] - 2023-05-31

### Added

- Added support for tables in `Markdown` https://github.com/Textualize/rich/pull/2977

## [13.3.5] - 2023-04-27

### Fixed

- Fixed italic indent guides in SVG output

## [13.3.4] - 2023-04-12

### Fixed

- Fixed for `is_terminal` ignoring FORCE_COLOR https://github.com/Textualize/rich/pull/2923

## [13.3.3] - 2023-02-27

### Added

- Added Style.clear_meta_and_links

## [13.3.2] - 2023-02-04

### Fixed

- Reversed `pre` and `code` tags in base HTML format https://github.com/Textualize/rich/pull/2642
- Fix syntax error when building with nuitka https://github.com/Textualize/rich/pull/2635
- Fixed pretty printing of empty dataclass https://github.com/Textualize/rich/issues/2819
- Use `Console(stderr=True)` in `rich.traceback.install` to support io redirection.
- Fixes superfluous spaces in html output https://github.com/Textualize/rich/issues/2832
- Fixed duplicate output in Jupyter https://github.com/Textualize/rich/pulls/2804
- Filter ANSI character-encoding-change codes in `Text.from_ansi` parser
- Fixes traceback failing when a frame filename is unreadable https://github.com/Textualize/rich/issues/2821
- Fix for live update rendering console markup https://github.com/Textualize/rich/issues/2726

### Added

- Added Polish README

### Changed

- `rich.progress.track()` will now show the elapsed time after finishing the task https://github.com/Textualize/rich/pull/2659

## [13.3.1] - 2023-01-28

### Fixed

- Fixed truecolor to eight bit color conversion https://github.com/Textualize/rich/pull/2785

## [13.3.0] - 2023-01-27

### Fixed

- Fixed failing tests due to Pygments dependency https://github.com/Textualize/rich/issues/2757
- Relaxed ipywidgets https://github.com/Textualize/rich/issues/2767

### Added

- Added `encoding` parameter in `Theme.read`


## [13.2.0] - 2023-01-19

### Changed

- Switch Markdown parsing from commonmark to markdown-it-py https://github.com/Textualize/rich/pull/2439

## [13.1.0] - 2023-01-14

### Fixed

- Fixed wrong filenames in Jupyter tracebacks https://github.com/Textualize/rich/issues/2271

### Added

- Added locals_hide_dunder and locals_hide_sunder to Tracebacks, to hide double underscore and single underscore locals. https://github.com/Textualize/rich/pull/2754

### Changed

- Tracebacks will now hide double underscore names from locals by default. Set `locals_hide_dunder=False` to restore previous behaviour.

## [13.0.1] - 2023-01-06

### Fixed

- Fixed issue with Segment.split_cells for mixed single and double cell widths

## [13.0.0] - 2022-12-30

### Fixed

- Reversed `pre` and `code` tags in base HTML format https://github.com/Textualize/rich/pull/2642
- Improved detection of `attrs` library, that isn't confused by the presence of the `attr` library.
- Fixed issue with `locals_max_length` parameter not being respected in Traceback https://github.com/Textualize/rich/issues/2649
- Handling of broken `fileno` made more robust. Fixes https://github.com/Textualize/rich/issues/2645
- Fixed missing `fileno` on FileProxy

### Fixed

- Fix type of `spinner_style` argument in `Console.status` https://github.com/Textualize/rich/pull/2613.

### Changed

- Bumped minimum Python version to 3.7 https://github.com/Textualize/rich/pull/2567
- Pretty-printing of "tagged" `__repr__` results is now greedy when matching tags https://github.com/Textualize/rich/pull/2565
- `progress.track` now supports deriving total from `__length_hint__`

### Added

- Add type annotation for key_separator of pretty.Node https://github.com/Textualize/rich/issues/2625


## [12.6.0] - 2022-10-02

### Added

- Parse ANSI escape sequences in pretty repr https://github.com/Textualize/rich/pull/2470
- Add support for `FORCE_COLOR` env var https://github.com/Textualize/rich/pull/2449
- Allow a `max_depth` argument to be passed to the `install()` hook https://github.com/Textualize/rich/issues/2486
- Document using `None` as name in `__rich_repr__` for tuple positional args https://github.com/Textualize/rich/pull/2379
- Add `font_aspect_ratio` parameter in SVG export https://github.com/Textualize/rich/pull/2539/files
- Added `Table.add_section` method. https://github.com/Textualize/rich/pull/2544

### Fixed

- Handle stdout/stderr being null https://github.com/Textualize/rich/pull/2513
- Fix NO_COLOR support on legacy Windows https://github.com/Textualize/rich/pull/2458
- Fix pretty printer handling of cyclic references https://github.com/Textualize/rich/pull/2524
- Fix missing `mode` property on file wrapper breaking uploads via `requests` https://github.com/Textualize/rich/pull/2495
- Fix mismatching default value of parameter `ensure_ascii` https://github.com/Textualize/rich/pull/2538
- Remove unused height parameter in `Layout` class https://github.com/Textualize/rich/pull/2540
- Fixed exception in Syntax.__rich_measure__ for empty files

### Changed

- Removed border from code blocks in Markdown

## [12.5.2] - 2022-07-18

### Added

- Add Turkish Readme.

## [12.5.1] - 2022-07-11

### Fixed

- Fixed missing typing extensions dependency on 3.9 https://github.com/Textualize/rich/issues/2386
- Fixed Databricks Notebook is not detected as Jupyter environment. https://github.com/Textualize/rich/issues/2422

## [12.5.0] - 2022-07-11

### Added

- Environment variables `JUPYTER_COLUMNS` and `JUPYTER_LINES` to control width and height of console in Jupyter
- Markdown friendly `Box` style, `MARKDOWN`, for rendering tables ready to copy into markdown files
- `inspect` will prefix coroutine functions with `async def`
- `Style.__add__` will no longer return `NotImplemented`
- Remove rich.\_lru_cache

### Changed

- Default width of Jupyter console size is increased to 115
- Optimized Segment.divide

### Fixed

- Fix Rich clobbering cursor style on Windows https://github.com/Textualize/rich/pull/2339
- Fix text wrapping edge case https://github.com/Textualize/rich/pull/2296
- Allow exceptions that are raised while a Live is rendered to be displayed and/or processed https://github.com/Textualize/rich/pull/2305
- Fix crashes that can happen with `inspect` when docstrings contain some special control codes https://github.com/Textualize/rich/pull/2294
- Fix edges used in first row of tables when `show_header=False` https://github.com/Textualize/rich/pull/2330
- Fix interaction between `Capture` contexts and `Console(record=True)` https://github.com/Textualize/rich/pull/2343
- Fixed hash issue in Styles class https://github.com/Textualize/rich/pull/2346
- Fixed bug in `Segment.split_and_crop_lines`

## [12.4.4] - 2022-05-24

### Changed

- Added clipping per line to SVG output to avoid box characters overlapping
- Optimized SVG output

## [12.4.3] - 2022-05-23

### Changed

- Further tweaks to SVG character matrix
- Added clip rect to SVG to prevent box characters overlapping bottom of terminal

## [12.4.2] - 2022-05-23

### Fixed

- Fix for SVG on Firefox

### Changed

- Removed excess margin from SVG, tweaked cell sizes to better render block characters

## [12.4.1] - 2022-05-08

### Fixed

- Fix for default background color in SVG export https://github.com/Textualize/rich/issues/2260

### Changed

- Added a keyline around SVG terminals which is visible on dark backgrounds

### Changed

- Added a keyline around SVG terminals which is visible on dark backgrounds

## [12.4.0] - 2022-05-07

### Changed

- Rebuilt SVG export to create a simpler SVG that is more portable
- Fix render_lines crash when render height was negative https://github.com/Textualize/rich/pull/2246
- Make objects from `rich.progress.open` forward the name of the internal handle https://github.com/Textualize/rich/pull/2254

### Added

- Add `padding` to Syntax constructor https://github.com/Textualize/rich/pull/2247

## [12.3.0] - 2022-04-26

### Added

- Ability to change terminal window title https://github.com/Textualize/rich/pull/2200
- Added show_speed parameter to progress.track which will show the speed when the total is not known
- Python blocks can now opt out from being rendered in tracebacks's frames, by setting a `_rich_traceback_omit = True` in their local scope https://github.com/Textualize/rich/issues/2207

### Fixed

- Fall back to `sys.__stderr__` on POSIX systems when trying to get the terminal size (fix issues when Rich is piped to another process)
- Fixed markup escaping issue https://github.com/Textualize/rich/issues/2187
- Safari - Box appearing around SVG export https://github.com/Textualize/rich/pull/2201
- Fixed recursion error in Jupyter progress bars https://github.com/Textualize/rich/issues/2047
- Complex numbers are now identified by the highlighter https://github.com/Textualize/rich/issues/2214
- Fix crash on IDLE and forced is_terminal detection to False because IDLE can't do escape codes https://github.com/Textualize/rich/issues/2222
- Fixed missing blank line in traceback rendering https://github.com/Textualize/rich/issues/2206
- Fixed running Rich with the current working dir was deleted https://github.com/Textualize/rich/issues/2197

### Changed

- Setting `total=None` on progress is now possible, and will display pulsing animation
- Micro-optimization for Segment.divide

## [12.2.0] - 2022-04-05

### Changed

- Bumped typing-extensions minimum to 4.0.0
- Bumped minimum Python version to 3.6.3

## [12.1.0] - 2022-04-03

### Added

- Progress.open and Progress.wrap_file method to track the progress while reading from a file or file-like object https://github.com/textualize/rich/pull/1759
- SVG export functionality https://github.com/Textualize/rich/pull/2101
- Adding Indonesian translation

### Fixed

- Add missing `end` keyword argument to `Text.from_markup` https://github.com/Textualize/rich/pull/2095
- Fallback to text lexer when no lexer guessed https://github.com/Textualize/rich/pull/2133
- Fixed issue with decoding ANSI reset https://github.com/Textualize/rich/issues/2112

## [12.0.1] - 2022-03-22

### Changed

- Improve performance of cell_length https://github.com/Textualize/rich/pull/2061
- Improve performance of chop_cells https://github.com/Textualize/rich/pull/2077

### Fixed

- Fix capturing stdout on legacy Windows https://github.com/Textualize/rich/pull/2066

## [12.0.0] - 2022-03-10

### Added

- Added options to TimeRemainingColumn to render a compact time format and render elapsed time when a task is
  finished. https://github.com/Textualize/rich/pull/1992
- Added ProgressColumn `MofNCompleteColumn` to display raw `completed/total` column (similar to DownloadColumn,
  but displays values as ints, does not convert to floats or add bit/bytes units).
  https://github.com/Textualize/rich/pull/1941
- Replace Colorama with win32 renderer https://github.com/Textualize/rich/pull/1993
- Add support for namedtuples to `Pretty` https://github.com/Textualize/rich/pull/2031

### Fixed

- In Jupyter mode make the link target be set to "\_blank"
- Fix some issues with markup handling around "[" characters https://github.com/Textualize/rich/pull/1950
- Fix syntax lexer guessing.
- Fixed Pretty measure not respecting expand_all https://github.com/Textualize/rich/issues/1998
- Collapsed definitions for single-character spinners, to save memory and reduce import time.
- Fix print_json indent type in `__init__.py`
- Fix error when inspecting object defined in REPL https://github.com/Textualize/rich/pull/2037
- Fix incorrect highlighting of non-indented JSON https://github.com/Textualize/rich/pull/2038
- Fixed height reset in complex renderables https://github.com/Textualize/rich/issues/2042

### Changed

- Improved support for enum.Flag in ReprHighlighter https://github.com/Textualize/rich/pull/1920
- Tree now respects justify=None, i.e. won't pad to right https://github.com/Textualize/rich/issues/1690
- Removed rich.tabulate which was marked for deprecation
- Deprecated rich.align.AlignValues in favor of AlignMethod

## [11.2.0] - 2022-02-08

### Added

- Add support for US spelling of "gray" in ANSI color names https://github.com/Textualize/rich/issues/1890
- Added `rich.diagnose.report` to expose environment debugging logic as function https://github.com/Textualize/rich/pull/1917
- Added classmethod `Progress.get_default_columns()` to get the default list of progress bar columns https://github.com/Textualize/rich/pull/1894

### Fixed

- Fixed performance issue in measuring text

### Fixed

- Fixed test failures on PyPy3 https://github.com/Textualize/rich/pull/1904

## [11.1.0] - 2022-01-28

### Added

- Workaround for edge case of object from Faiss with no `__class__` https://github.com/Textualize/rich/issues/1838
- Add Traditional Chinese readme
- Add `Syntax.guess_lexer`, add support for more lexers (e.g. Django templates etc.) https://github.com/Textualize/rich/pull/1869
- Add `lexer` parameter to `Syntax.from_path` to allow for overrides https://github.com/Textualize/rich/pull/1873

### Fixed

- Workaround for edge case of object from Faiss with no `__class__` https://github.com/Textualize/rich/issues/1838
- Ensure `Syntax` always justifies left https://github.com/Textualize/rich/pull/1872
- Handle classes in inspect when methods=True https://github.com/Textualize/rich/pull/1874

## [11.0.0] - 2022-01-09

### Added

- Added max_depth arg to pretty printing https://github.com/Textualize/rich/issues/1585
- Added `vertical_align` to Table.add_row https://github.com/Textualize/rich/issues/1590

### Fixed

- Fixed issue with pretty repr in jupyter notebook https://github.com/Textualize/rich/issues/1717
- Fix Traceback theme defaults override user supplied styles https://github.com/Textualize/rich/issues/1786

### Changed

- **breaking** Deprecated rich.console.RenderGroup, now named rich.console.Group
- **breaking** `Syntax.__init__` parameter `lexer_name` renamed to `lexer`
- Syntax constructor accepts both str and now a pygments lexer https://github.com/Textualize/rich/pull/1748

## [10.16.2] - 2021-01-02

### Fixed

- Fixed @ not being escaped in markup

## [10.16.1] - 2021-12-15

### Fixed

- Fixed issues with overlapping tags https://github.com/textualize/rich/issues/1755

## [10.16.0] - 2021-12-12

### Fixed

- Double print of progress bar in Jupyter https://github.com/textualize/rich/issues/1737

### Added

- Added Text.markup property https://github.com/textualize/rich/issues/1751

## [10.15.2] - 2021-12-02

### Fixed

- Deadlock issue https://github.com/textualize/rich/issues/1734

## [10.15.1] - 2021-11-29

### Fixed

- Reverted thread-safety fix for Live that introduced deadlock potential

## [10.15.0] - 2021-11-28

### Added

- Added dynamic_progress.py to examples
- Added ConsoleOptions.update_height
- Fixed Padding not respecting height

### Changed

- Some optimizations for simple strings (with only single cell widths)

### Fixed

- Fixed issue with progress bar not rendering markup https://github.com/textualize/rich/issues/1721
- Fixed race condition when exiting Live https://github.com/textualize/rich/issues/1530

## [10.14.0] - 2021-11-16

### Fixed

- Fixed progress speed not updating when total doesn't change
- Fixed superfluous new line in Status https://github.com/textualize/rich/issues/1662
- Fixed Windows legacy width again
- Fixed infinite loop in set_cell_size https://github.com/textualize/rich/issues/1682

### Added

- Added file protocol to URL highlighter https://github.com/textualize/rich/issues/1681
- Added rich.protocol.rich_cast

### Changed

- Allowed `__rich__` to work recursively
- Allowed Text classes to work with sep in print https://github.com/textualize/rich/issues/1689

### Added

- Added a `rich.text.Text.from_ansi` helper method for handling pre-formatted input strings https://github.com/textualize/rich/issues/1670

## [10.13.0] - 2021-11-07

### Added

- Added json.dumps parameters to print_json https://github.com/textualize/rich/issues/1638

### Fixed

- Fixed an edge case bug when console module try to detect if they are in a tty at the end of a pytest run
- Fixed a bug where logging handler raises an exception when running with pythonw (related to https://bugs.python.org/issue13807)
- Fixed issue with TERM env vars that have more than one hyphen https://github.com/textualize/rich/issues/1640
- Fixed missing new line after progress bar when terminal is not interactive https://github.com/textualize/rich/issues/1606
- Fixed exception in IPython when disabling pprint with %pprint https://github.com/textualize/rich/issues/1646
- Fixed issue where values longer than the console width produced invalid JSON https://github.com/textualize/rich/issues/1653
- Fixes trailing comma when pretty printing dataclass with last field repr=False https://github.com/textualize/rich/issues/1599

## Changed

- Markdown codeblocks now word-wrap https://github.com/textualize/rich/issues/1515

## [10.12.0] - 2021-10-06

### Updated

- Official Py3.10 release

### Fixed

- Fixed detection of custom repr when pretty printing dataclasses

## [10.11.0] - 2021-09-24

### Added

- Added `suppress` parameter to tracebacks
- Added `max_frames` parameter to tracebacks

## [10.10.0] - 2021-09-18

### Added

- Added stdin support to `rich.json`

### Fixed

- Fixed pretty printing of objects with fo magic with **getattr** https://github.com/textualize/rich/issues/1492

## [10.9.0] - 2021-08-29

### Added

- Added data parameter to print_json method / function
- Added an --indent parameter to python -m rich.json

### Changed

- Changed default indent of JSON to 2 (down from 4)
- Changed highlighting of JSON keys to new style (bold blue)

## [10.8.0] - 2021-08-28

### Added

- Added Panel.subtitle
- Added Panel.subtitle_align
- Added rich.json.JSON
- Added rich.print_json and Console.print_json

### Fixed

- Fixed a bug where calling `rich.reconfigure` within a `pytest_configure` hook would lead to a crash
- Fixed highlight not being passed through options https://github.com/textualize/rich/issues/1404

## [10.7.0] - 2021-08-05

### Added

- Added Text.apply_meta
- Added meta argument to Text.assemble
- Added Style.from_meta
- Added Style.on
- Added Text.on

### Changed

- Changed `RenderGroup` to `Group` and `render_group` to `group` (old names remain for compatibility but will be deprecated in the future)
- Changed `rich.repr.RichReprResult` to `rich.repr.Result` (old names remain for compatibility but will be deprecated in the future)
- Changed meta serialization to use pickle rather than marshal to permit callables

## [10.6.0] - 2021-07-12

### Deprecated

- Added deprecation warning for tabulate_mapping which will be removed in v11.0.0

### Added

- Added precision argument to filesize.decimal
- Added separator argument to filesize.decimal
- Added \_rich_traceback_guard to Traceback
- Added emoji_variant to Console
- Added -emoji and -text variant selectors to emoji code

### Fixed

- Fixed issue with adjoining color tags https://github.com/textualize/rich/issues/1334

### Changed

- Changed Console.size to use unproxied stdin and stdout

## [10.5.0] - 2021-07-05

### Fixed

- Fixed Pandas objects not pretty printing https://github.com/textualize/rich/issues/1305
- Fixed https://github.com/textualize/rich/issues/1256
- Fixed typing with rich.repr.auto decorator
- Fixed repr error formatting https://github.com/textualize/rich/issues/1326

### Added

- Added new_line_start argument to Console.print
- Added Segment.divide method
- Added Segment.split_cells method
- Added segment.SegmentLines class

## [10.4.0] - 2021-06-18

### Added

- Added Style.meta
- Added rich.repr.auto decorator

### Fixed

- Fixed error pretty printing classes with special **rich_repr** method

## [10.3.0] - 2021-06-09

### Added

- Added Console.size setter
- Added Console.width setter
- Added Console.height setter
- Added angular style Rich reprs
- Added an IPython extension. Load via `%load_ext rich`

### Changed

- Changed the logic for retrieving the calling frame in console logs to a faster one for the Python implementations that support it.

## [10.2.2] - 2021-05-19

### Fixed

- Fixed status not rendering console markup https://github.com/textualize/rich/issues/1244

## [10.2.1] - 2021-05-17

### Fixed

- Fixed panel in Markdown exploding https://github.com/textualize/rich/issues/1234

## [10.2.0] - 2021-05-12

### Added

- Added syntax for call, i.e. "Foo(bar)"
- Added Console.measure as a convenient alias for Measurement.get
- Added support for pretty printing attrs objects
- Added mappingproxy to pretty print
- Added UserDict and UserList support to pretty printer

### Changed

- Changed colorama init to set strip=False
- Changed highlighter for False, True, None to not match in the middle of a word. i.e. NoneType is no longer highlighted as None

### Fixed

- Fixed initial blank lines removed from Syntax https://github.com/textualize/rich/issues/1214

## [10.1.0] - 2021-04-03

### Fixed

- Fixed support for jupyter qtconsole and similar Jupyter environments

## [10.0.1] - 2021-03-30

### Fixed

- Fixed race condition that duplicated lines in progress https://github.com/textualize/rich/issues/1144

## [10.0.0] - 2021-03-27

### Changed

- Made pydoc import lazy as at least one use found it slow to import https://github.com/textualize/rich/issues/1104
- Modified string highlighting to not match in the middle of a word, so that apostrophes are not considered strings
- New way of encoding control codes in Segment
- New signature for Control class
- Changed Layout.split to use new Splitter class
- Improved layout.tree
- Changed default theme color for repr.number to cyan
- `__rich_measure__` signature changed to accept ConsoleOptions rather than max_width
- `text` parameter to rich.spinner.Spinner changed to RenderableType

### Added

- Added `__rich_repr__` protocol method to Pretty
- Added rich.region.Region
- Added ConsoleOptions.update_dimensions
- Added rich.console.ScreenUpdate
- Added Console.is_alt_screen
- Added Control.segment, Control.bell, Control.home, Control.move_to, Control.clear, Control.show_cursor, Control.alt_screen
- Added Console.update_screen and Console.update_screen_lines
- Added Layout.add_split, Layout.split_column, Layout.split_row, layout.refresh
- Added new Rich repr protocol `__rich_repr__`

### Fixed

- Fixed table style taking precedence over row style https://github.com/textualize/rich/issues/1129
- Fixed incorrect measurement of Text with new lines and whitespace https://github.com/textualize/rich/issues/1133
- Made type annotations consistent for various `total` keyword arguments in `rich.progress` and rich.`progress_bar`
- Disabled Progress no longer displays itself when starting https://github.com/textualize/rich/pull/1125
- Animations no longer reset when updating rich.status.Status

## [9.13.0] - 2021-03-06

### Added

- Pretty printer now supports dataclasses

### Fixed

- Fixed Syntax background https://github.com/textualize/rich/issues/1088
- Fix for double tracebacks when no formatter https://github.com/textualize/rich/issues/1079

### Changed

- Added ws and wss to url highlighter

## [9.12.4] - 2021-03-01

### Fixed

- Fixed custom formatters with rich tracebacks in RichHandler https://github.com/textualize/rich/issues/1079

### Changed

- Allow highly compressed table cells to go to 0 width
- Optimization to remove empty styles in various places

## [9.12.3] - 2021-02-28

### Changed

- Optimized Padding

## [9.12.2] - 2021-02-27

### Added

- Added ConsoleOptions.copy

### Changed

- Optimized ConsoleOptions.update

## [9.12.1] - 2021-02-27

### Fixed

- Fixed deadlock in Progress https://github.com/textualize/rich/issues/1061

### Added

- Added Task.finished_speed

### Changed

- Froze TransferSpeedColumn speed when task is finished
- Added SIGINT handler to downloader.py example
- Optimization for large tables

## [9.12.0] - 2021-02-24

### Fixed

- Fixed issue with Syntax and missing lines in Layout https://github.com/textualize/rich/issues/1050
- Fixed issue with nested markdown elements https://github.com/textualize/rich/issues/1036
- Fixed new lines not invoking render hooks https://github.com/textualize/rich/issues/1052
- Fixed Align setting height to child https://github.com/textualize/rich/issues/1057

### Changed

- Printing a table with no columns now result in a blank line https://github.com/textualize/rich/issues/1044

### Added

- Added height to Panel

## [9.11.1] - 2021-02-20

### Fixed

- Fixed table with expand=False not expanding when justify="center"
- Fixed single renderable in Layout not respecting height
- Fixed COLUMNS and LINES env var https://github.com/textualize/rich/issues/1019
- Layout now respects minimum_size when fixes sizes are greater than available space
- HTML export now changes link underline score to match terminal https://github.com/textualize/rich/issues/1009

### Changed

- python -m rich.markdown and rich.syntax show usage with no file

### Added

- Added height parameter to Layout
- Added python -m rich.segment

## [9.11.0] - 2021-02-15

### Fixed

- Fixed error message for tracebacks with broken `__str__` https://github.com/textualize/rich/issues/980
- Fixed markup edge case https://github.com/textualize/rich/issues/987

### Added

- Added cheeky sponsorship request to test card
- Added `quiet` argument to Console constructor
- Added support for a callback function to format timestamps (allows presentation of milliseconds)
- Added Console.set_alt_screen and Console.screen
- Added height to ConsoleOptions
- Added `vertical` parameter to Align
- Added Layout class

### Changed

- Pretty.overflow now defaults to None
- Panel now respects options.height
- Traceback lexer defaults to Python if no extension on source
- Added ConsoleDimensions size attribute to ConsoleOptions so that size can't change mid-render

## [9.10.0] - 2021-01-27

### Changed

- Some optimizations for Text
- Further optimized Tracebacks by not tokenizing code more that necessary
- Table Column.header_style and Column.footer_style are now added to Table header/footer style

## [9.9.0] - 2021-01-23

### Changed

- Extended Windows palette to 16 colors
- Modified windows palette to Windows 10 colors
- Change regex for attrib_name to be more performant
- Optimized traceback generation

### Fixed

- Fix double line tree guides on Windows
- Fixed Tracebacks ignoring initial blank lines
- Partial fix for tracebacks not finding source after chdir
- Fixed error message when code in tracebacks doesn't have an extension https://github.com/textualize/rich/issues/996

### Added

- Added post_style argument to Segment.apply_style

## [9.8.2] - 2021-01-15

### Fixed

- Fixed deadlock in live https://github.com/textualize/rich/issues/927

## [9.8.1] - 2021-01-13

### Fixed

- Fixed rich.inspect failing with attributes that claim to be callable but aren't https://github.com/textualize/rich/issues/916

## [9.8.0] - 2021-01-11

### Added

- Added **rich_measure** for tree
- Added rich.align.VerticalCenter

### Changed

- The `style` argument on Align now applies to background only
- Changed display of progress bars in no_color mode for clarity
- Console property `size` will fall back to getting the terminal size of stdout it stdin fails, this allows size to be correctly determined when piping

### Fixed

- Fixed panel cropping when shrunk too bar
- Allow passing markdown over STDIN when using `python -m rich.markdown`
- Fix printing MagicMock.mock_calls https://github.com/textualize/rich/issues/903

## [9.7.0] - 2021-01-09

### Added

- Added rich.tree
- Added no_color argument to Console

## [9.6.2] - 2021-01-07

### Fixed

- Fixed markup escaping edge case https://github.com/textualize/rich/issues/878
- Double tag escape, i.e. `"\\[foo]"` results in a backslash plus `[foo]` tag
- Fixed header_style not applying to headers in positional args https://github.com/textualize/rich/issues/953

## [9.6.1] - 2020-12-31

### Fixed

- Fixed encoding error on Windows when loading code for Tracebacks

## [9.6.0] - 2020-12-30

### Changed

- MarkupError exception raise from None to omit internal exception
- Factored out RichHandler.render and RichHandler.render_message for easier extending
- Display pretty printed value in rich.inspect

### Added

- Added Progress.TimeElapsedColumn
- Added IPython support to pretty.install

### Fixed

- Fixed display of locals in Traceback for stdin

## [9.5.1] - 2020-12-19

### Fixed

- Fixed terminal size detection on Windows https://github.com/textualize/rich/issues/836
- Fixed hex number highlighting

## [9.5.0] - 2020-12-18

### Changed

- If file is not specified on Console then the Console.file will return the current sys.stdout. Prior to 9.5.0 sys.stdout was cached on the Console, which could break code that wrapped sys.stdout after the Console was constructed.
- Changed `Color.__str__` to not include ansi codes
- Changed Console.size to get the terminal dimensions via sys.stdin. This means that if you set file to be an io.StringIO file then the width will be set to the current terminal dimensions and not a default of 80.

### Added

- Added stderr parameter to Console
- Added rich.reconfigure
- Added `Color.__rich__`
- Added Console.soft_wrap
- Added Console.style parameter
- Added Table.highlight parameter to enable highlighting of cells
- Added Panel.highlight parameter to enable highlighting of panel title
- Added highlight to ConsoleOptions

### Fixed

- Fixed double output in rich.live https://github.com/textualize/rich/issues/485
- Fixed Console.out highlighting not reflecting defaults https://github.com/textualize/rich/issues/827
- FileProxy now raises TypeError for empty non-str arguments https://github.com/textualize/rich/issues/828

## [9.4.0] - 2020-12-12

### Added

- Added rich.live https://github.com/textualize/rich/pull/382
- Added align parameter to Rule and Console.rule
- Added rich.Status class and Console.status
- Added getitem to Text
- Added style parameter to Console.log
- Added rich.diagnose command

### Changed

- Table.add_row style argument now applies to entire line and not just cells
- Added end_section parameter to Table.add_row to force a line underneath row

## Fixed

- Fixed suppressed traceback context https://github.com/textualize/rich/issues/468

## [9.3.0] - 2020-12-1

### Added

- Added get_datetime parameter to Console, to allow for repeatable tests
- Added get_time parameter to Console
- Added rich.abc.RichRenderable
- Added expand_all to rich.pretty.install()
- Added locals_max_length, and locals_max_string to Traceback and logging.RichHandler
- Set defaults of max_length and max_string for Traceback to 10 and 80
- Added disable argument to Progress

### Changed

- Reformatted test card (python -m rich)

### Fixed

- Fixed redirecting of stderr in Progress
- Fixed broken expanded tuple of one https://github.com/textualize/rich/issues/445
- Fixed traceback message with `from` exceptions
- Fixed justify argument not working in console.log https://github.com/textualize/rich/issues/460

## [9.2.0] - 2020-11-08

### Added

- Added tracebacks_show_locals parameter to RichHandler
- Added max_string to Pretty
- Added rich.ansi.AnsiDecoder
- Added decoding of ansi codes to captured stdout in Progress
- Added expand_all to rich.pretty.pprint

### Changed

- Applied dim=True to indent guide styles
- Factored out RichHandler.get_style_and_level to allow for overriding in subclasses
- Hid progress bars from html export
- rich.pretty.pprint now soft wraps

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

- Fixed negative time remaining in Progress bars https://github.com/textualize/rich/issues/378

## [9.0.1] - 2020-10-19

### Fixed

- Fixed broken ANSI codes in input on windows legacy https://github.com/textualize/rich/issues/393

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
- Added Bar renderable https://github.com/textualize/rich/pull/361
- Added Table.min_width
- Added table.Column.min_width and table.Column.max_width, and same to Table.add_column

### Changed

- Dropped box.get_safe_box function in favor of Box.substitute
- Changed default padding in Panel from 0 to (0, 1) https://github.com/textualize/rich/issues/385
- Table with row_styles will extend background color between cells if the box has no vertical dividerhttps://github.com/textualize/rich/issues/383
- Changed default of fit kwarg in render_group() from False to True
- Renamed rich.bar to rich.progress_bar, and Bar class to ProgressBar, rich.bar is now the new solid bar class

### Fixed

- Fixed typo in `Style.transparent_background` method name.

## [8.0.0] - 2020-10-03

### Added

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
- Added Table.title_justify and Table.caption_justify https://github.com/textualize/rich/issues/301

### Changed

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

### Changed

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

- Fixed underscore with display hook https://github.com/textualize/rich/issues/235

## [5.2.0] - 2020-08-14

### Changed

- Added crop argument to Console.print
- Added "ignore" overflow method
- Added multiple characters per rule @hedythedev https://github.com/textualize/rich/pull/207

## [5.1.2] - 2020-08-10

### Fixed

- Further optimized pretty printing ~5X.

## [5.1.1] - 2020-08-09

### Fixed

- Optimized pretty printing ~3X faster

## [5.1.0] - 2020-08-08

### Added

- Added Text.cell_len
- Added helpful message regarding unicode decoding errors https://github.com/textualize/rich/issues/212
- Added display hook with pretty.install()

### Fixed

- Fixed deprecation warnings re backslash https://github.com/textualize/rich/issues/210
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

- Added show_time and show_level parameters to RichHandler https://github.com/textualize/rich/pull/182

### Fixed

- Fixed progress.track iterator exiting early https://github.com/textualize/rich/issues/189
- Added workaround for Python bug https://bugs.python.org/issue37871, fixing https://github.com/textualize/rich/issues/186

### Changed

- Set overflow=fold for log messages https://github.com/textualize/rich/issues/190

## [4.2.0] - 2020-07-27

### Fixed

- Fixed missing new lines https://github.com/textualize/rich/issues/178
- Fixed Progress.track https://github.com/textualize/rich/issues/184
- Remove control codes from exported text https://github.com/textualize/rich/issues/181
- Implemented auto-detection and color rendition of 16-color mode

## [4.1.0] - 2020-07-26

### Changed

- Optimized progress.track for very quick iterations
- Force default size of 80x25 if get_terminal_size reports size of 0,0

## [4.0.0] - 2020-07-23

Major version bump for a breaking change to `Text.stylize signature`, which corrects a minor but irritating API wart. The style now comes first and the `start` and `end` offsets default to the entire text. This allows for `text.stylize_all(style)` to be replaced with `text.stylize(style)`. The `start` and `end` offsets now support negative indexing, so `text.stylize("bold", -1)` makes the last character bold.

### Added

- Added markup switch to RichHandler https://github.com/textualize/rich/issues/171

### Changed

- Change signature of Text.stylize to accept style first
- Remove Text.stylize_all which is no longer necessary

### Fixed

- Fixed rendering of Confirm prompt https://github.com/textualize/rich/issues/170

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

- More precise detection of Windows console https://github.com/textualize/rich/issues/140

## [3.0.3] - 2020-07-03

### Fixed

- Fixed edge case with wrapped and overflowed text

### Changed

- New algorithm for compressing table that priorities smaller columns

### Added

- Added safe_box parameter to Console constructor

## [3.0.2] - 2020-07-02

### Added

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

- Disabled legacy_windows if jupyter is detected https://github.com/textualize/rich/issues/125

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

- Store a "link id" on Style instance, so links containing different styles are highlighted together. (https://github.com/textualize/rich/pull/123)

## [2.2.5] - 2020-06-23

### Fixed

- Fixed justify of tables (https://github.com/textualize/rich/issues/117)

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

### Changed

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

- Fixed Progress deadlock https://github.com/textualize/rich/issues/90

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

### Added

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

### Added

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

### Added

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

- Issue with Windows legacy support https://github.com/textualize/rich/issues/59

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

- Fixed Text.assemble not working with strings https://github.com/textualize/rich/issues/57
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

- Readme links in PyPI

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
- Fixed line width on windows issue (https://github.com/textualize/rich/issues/7)
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

[13.7.0]: https://github.com/textualize/rich/compare/v13.6.0...v13.7.0
[13.6.0]: https://github.com/textualize/rich/compare/v13.5.3...v13.6.0
[13.5.3]: https://github.com/textualize/rich/compare/v13.5.2...v13.5.3
[13.5.2]: https://github.com/textualize/rich/compare/v13.5.1...v13.5.2
[13.5.1]: https://github.com/textualize/rich/compare/v13.5.0...v13.5.1
[13.5.0]: https://github.com/textualize/rich/compare/v13.4.2...v13.5.0
[13.4.2]: https://github.com/textualize/rich/compare/v13.4.1...v13.4.2
[13.4.1]: https://github.com/textualize/rich/compare/v13.4.0...v13.4.1
[13.4.0]: https://github.com/textualize/rich/compare/v13.3.5...v13.4.0
[13.3.5]: https://github.com/textualize/rich/compare/v13.3.4...v13.3.5
[13.3.4]: https://github.com/textualize/rich/compare/v13.3.3...v13.3.4
[13.3.3]: https://github.com/textualize/rich/compare/v13.3.2...v13.3.3
[13.3.2]: https://github.com/textualize/rich/compare/v13.3.1...v13.3.2
[13.3.1]: https://github.com/textualize/rich/compare/v13.3.0...v13.3.1
[13.3.0]: https://github.com/textualize/rich/compare/v13.2.0...v13.3.0
[13.2.0]: https://github.com/textualize/rich/compare/v13.1.0...v13.2.0
[13.1.0]: https://github.com/textualize/rich/compare/v13.0.1...v13.1.0
[13.0.1]: https://github.com/textualize/rich/compare/v13.0.0...v13.0.1
[13.0.0]: https://github.com/textualize/rich/compare/v12.6.0...v13.0.0
[12.6.0]: https://github.com/textualize/rich/compare/v12.5.2...v12.6.0
[12.5.2]: https://github.com/textualize/rich/compare/v12.5.1...v12.5.2
[12.5.1]: https://github.com/textualize/rich/compare/v12.5.0...v12.5.1
[12.5.0]: https://github.com/textualize/rich/compare/v12.4.4...v12.5.0
[12.4.4]: https://github.com/textualize/rich/compare/v12.4.3...v12.4.4
[12.4.3]: https://github.com/textualize/rich/compare/v12.4.2...v12.4.3
[12.4.2]: https://github.com/textualize/rich/compare/v12.4.1...v12.4.2
[12.4.1]: https://github.com/textualize/rich/compare/v12.4.0...v12.4.1
[12.4.0]: https://github.com/textualize/rich/compare/v12.3.0...v12.4.0
[12.3.0]: https://github.com/textualize/rich/compare/v12.2.0...v12.3.0
[12.2.0]: https://github.com/textualize/rich/compare/v12.1.0...v12.2.0
[12.1.0]: https://github.com/textualize/rich/compare/v12.0.1...v12.1.0
[12.0.1]: https://github.com/textualize/rich/compare/v12.0.0...v12.0.1
[12.0.0]: https://github.com/textualize/rich/compare/v11.2.0...v12.0.0
[11.2.0]: https://github.com/textualize/rich/compare/v11.1.0...v11.2.0
[11.1.0]: https://github.com/textualize/rich/compare/v11.0.0...v11.1.0
[11.0.0]: https://github.com/textualize/rich/compare/v10.16.1...v11.0.0
[10.16.2]: https://github.com/textualize/rich/compare/v10.16.1...v10.16.2
[10.16.1]: https://github.com/textualize/rich/compare/v10.16.0...v10.16.1
[10.16.0]: https://github.com/textualize/rich/compare/v10.15.2...v10.16.0
[10.15.2]: https://github.com/textualize/rich/compare/v10.15.1...v10.15.2
[10.15.1]: https://github.com/textualize/rich/compare/v10.15.0...v10.15.1
[10.15.0]: https://github.com/textualize/rich/compare/v10.14.0...v10.15.0
[10.14.0]: https://github.com/textualize/rich/compare/v10.13.0...v10.14.0
[10.13.0]: https://github.com/textualize/rich/compare/v10.12.0...v10.13.0
[10.12.0]: https://github.com/textualize/rich/compare/v10.11.0...v10.12.0
[10.11.0]: https://github.com/textualize/rich/compare/v10.10.0...v10.11.0
[10.10.0]: https://github.com/textualize/rich/compare/v10.9.0...v10.10.0
[10.9.0]: https://github.com/textualize/rich/compare/v10.8.0...v10.9.0
[10.8.0]: https://github.com/textualize/rich/compare/v10.7.0...v10.8.0
[10.7.0]: https://github.com/textualize/rich/compare/v10.6.0...v10.7.0
[10.6.0]: https://github.com/textualize/rich/compare/v10.5.0...v10.6.0
[10.5.0]: https://github.com/textualize/rich/compare/v10.4.0...v10.5.0
[10.4.0]: https://github.com/textualize/rich/compare/v10.3.0...v10.4.0
[10.3.0]: https://github.com/textualize/rich/compare/v10.2.2...v10.3.0
[10.2.2]: https://github.com/textualize/rich/compare/v10.2.1...v10.2.2
[10.2.1]: https://github.com/textualize/rich/compare/v10.2.0...v10.2.1
[10.2.0]: https://github.com/textualize/rich/compare/v10.1.0...v10.2.0
[10.1.0]: https://github.com/textualize/rich/compare/v10.0.1...v10.1.0
[10.0.1]: https://github.com/textualize/rich/compare/v10.0.0...v10.0.1
[10.0.0]: https://github.com/textualize/rich/compare/v9.13.0...v10.0.0
[9.13.0]: https://github.com/textualize/rich/compare/v9.12.4...v9.13.0
[9.12.4]: https://github.com/textualize/rich/compare/v9.12.3...v9.12.4
[9.12.3]: https://github.com/textualize/rich/compare/v9.12.2...v9.12.3
[9.12.2]: https://github.com/textualize/rich/compare/v9.12.1...v9.12.2
[9.12.1]: https://github.com/textualize/rich/compare/v9.12.0...v9.12.1
[9.12.0]: https://github.com/textualize/rich/compare/v9.11.1...v9.12.0
[9.11.1]: https://github.com/textualize/rich/compare/v9.11.0...v9.11.1
[9.11.0]: https://github.com/textualize/rich/compare/v9.10.0...v9.11.0
[9.10.0]: https://github.com/textualize/rich/compare/v9.9.0...v9.10.0
[9.9.0]: https://github.com/textualize/rich/compare/v9.8.2...v9.9.0
[9.8.2]: https://github.com/textualize/rich/compare/v9.8.1...v9.8.2
[9.8.1]: https://github.com/textualize/rich/compare/v9.8.0...v9.8.1
[9.8.0]: https://github.com/textualize/rich/compare/v9.7.0...v9.8.0
[9.7.0]: https://github.com/textualize/rich/compare/v9.6.2...v9.7.0
[9.6.2]: https://github.com/textualize/rich/compare/v9.6.1...v9.6.2
[9.6.1]: https://github.com/textualize/rich/compare/v9.6.0...v9.6.1
[9.6.0]: https://github.com/textualize/rich/compare/v9.5.1...v9.6.0
[9.5.1]: https://github.com/textualize/rich/compare/v9.5.0...v9.5.1
[9.5.0]: https://github.com/textualize/rich/compare/v9.4.0...v9.5.0
[9.4.0]: https://github.com/textualize/rich/compare/v9.3.0...v9.4.0
[9.3.0]: https://github.com/textualize/rich/compare/v9.2.0...v9.3.0
[9.2.0]: https://github.com/textualize/rich/compare/v9.1.0...v9.2.0
[9.1.0]: https://github.com/textualize/rich/compare/v9.0.1...v9.1.0
[9.0.1]: https://github.com/textualize/rich/compare/v9.0.0...v9.0.1
[9.0.0]: https://github.com/textualize/rich/compare/v8.0.0...v9.0.0
[8.0.0]: https://github.com/textualize/rich/compare/v7.1.0...v8.0.0
[7.1.0]: https://github.com/textualize/rich/compare/v7.0.0...v7.1.0
[7.0.0]: https://github.com/textualize/rich/compare/v6.2.0...v7.0.0
[6.2.0]: https://github.com/textualize/rich/compare/v6.1.2...v6.2.0
[6.1.2]: https://github.com/textualize/rich/compare/v6.1.1...v6.1.2
[6.1.1]: https://github.com/textualize/rich/compare/v6.1.0...v6.1.1
[6.1.0]: https://github.com/textualize/rich/compare/v6.0.0...v6.1.0
[6.0.0]: https://github.com/textualize/rich/compare/v5.2.1...v6.0.0
[5.2.1]: https://github.com/textualize/rich/compare/v5.2.0...v5.2.1
[5.2.0]: https://github.com/textualize/rich/compare/v5.1.2...v5.2.0
[5.1.2]: https://github.com/textualize/rich/compare/v5.1.1...v5.1.2
[5.1.1]: https://github.com/textualize/rich/compare/v5.1.0...v5.1.1
[5.1.0]: https://github.com/textualize/rich/compare/v5.0.0...v5.1.0
[5.0.0]: https://github.com/textualize/rich/compare/v4.2.2...v5.0.0
[4.2.2]: https://github.com/textualize/rich/compare/v4.2.1...v4.2.2
[4.2.1]: https://github.com/textualize/rich/compare/v4.2.0...v4.2.1
[4.2.0]: https://github.com/textualize/rich/compare/v4.1.0...v4.2.0
[4.1.0]: https://github.com/textualize/rich/compare/v4.0.0...v4.1.0
[4.0.0]: https://github.com/textualize/rich/compare/v3.4.1...v4.0.0
[3.4.1]: https://github.com/textualize/rich/compare/v3.4.0...v3.4.1
[3.4.0]: https://github.com/textualize/rich/compare/v3.3.2...v3.4.0
[3.3.2]: https://github.com/textualize/rich/compare/v3.3.1...v3.3.2
[3.3.1]: https://github.com/textualize/rich/compare/v3.3.0...v3.3.1
[3.3.0]: https://github.com/textualize/rich/compare/v3.2.0...v3.3.0
[3.2.0]: https://github.com/textualize/rich/compare/v3.1.0...v3.2.0
[3.1.0]: https://github.com/textualize/rich/compare/v3.0.5...v3.1.0
[3.0.5]: https://github.com/textualize/rich/compare/v3.0.4...v3.0.5
[3.0.4]: https://github.com/textualize/rich/compare/v3.0.3...v3.0.4
[3.0.3]: https://github.com/textualize/rich/compare/v3.0.2...v3.0.3
[3.0.2]: https://github.com/textualize/rich/compare/v3.0.1...v3.0.2
[3.0.1]: https://github.com/textualize/rich/compare/v3.0.0...v3.0.1
[3.0.0]: https://github.com/textualize/rich/compare/v2.3.1...v3.0.0
[2.3.1]: https://github.com/textualize/rich/compare/v2.3.0...v2.3.1
[2.3.0]: https://github.com/textualize/rich/compare/v2.2.6...v2.3.0
[2.2.6]: https://github.com/textualize/rich/compare/v2.2.5...v2.2.6
[2.2.5]: https://github.com/textualize/rich/compare/v2.2.4...v2.2.5
[2.2.4]: https://github.com/textualize/rich/compare/v2.2.3...v2.2.4
[2.2.3]: https://github.com/textualize/rich/compare/v2.2.2...v2.2.3
[2.2.2]: https://github.com/textualize/rich/compare/v2.2.1...v2.2.2
[2.2.1]: https://github.com/textualize/rich/compare/v2.2.0...v2.2.1
[2.2.0]: https://github.com/textualize/rich/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/textualize/rich/compare/v2.0.1...v2.1.0
[2.0.1]: https://github.com/textualize/rich/compare/v2.0.0...v2.0.1
[2.0.0]: https://github.com/textualize/rich/compare/v1.3.1...v2.0.0
[1.3.1]: https://github.com/textualize/rich/compare/v1.3.0...v1.3.1
[1.3.0]: https://github.com/textualize/rich/compare/v1.2.3...v1.3.0
[1.2.3]: https://github.com/textualize/rich/compare/v1.2.2...v1.2.3
[1.2.2]: https://github.com/textualize/rich/compare/v1.2.1...v1.2.2
[1.2.1]: https://github.com/textualize/rich/compare/v1.2.0...v1.2.1
[1.2.0]: https://github.com/textualize/rich/compare/v1.1.9...v1.2.0
[1.1.9]: https://github.com/textualize/rich/compare/v1.1.8...v1.1.9
[1.1.8]: https://github.com/textualize/rich/compare/v1.1.7...v1.1.8
[1.1.7]: https://github.com/textualize/rich/compare/v1.1.6...v1.1.7
[1.1.6]: https://github.com/textualize/rich/compare/v1.1.5...v1.1.6
[1.1.5]: https://github.com/textualize/rich/compare/v1.1.4...v1.1.5
[1.1.4]: https://github.com/textualize/rich/compare/v1.1.3...v1.1.4
[1.1.3]: https://github.com/textualize/rich/compare/v1.1.2...v1.1.3
[1.1.2]: https://github.com/textualize/rich/compare/v1.1.1...v1.1.2
[1.1.1]: https://github.com/textualize/rich/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/textualize/rich/compare/v1.0.3...v1.1.0
[1.0.3]: https://github.com/textualize/rich/compare/v1.0.2...v1.0.3
[1.0.2]: https://github.com/textualize/rich/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/textualize/rich/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/textualize/rich/compare/v0.8.13...v1.0.0
[0.8.13]: https://github.com/textualize/rich/compare/v0.8.12...v0.8.13
[0.8.12]: https://github.com/textualize/rich/compare/v0.8.11...v0.8.12
[0.8.11]: https://github.com/textualize/rich/compare/v0.8.10...v0.8.11
[0.8.10]: https://github.com/textualize/rich/compare/v0.8.9...v0.8.10
[0.8.9]: https://github.com/textualize/rich/compare/v0.8.8...v0.8.9
[0.8.8]: https://github.com/textualize/rich/compare/v0.8.7...v0.8.8
[0.8.7]: https://github.com/textualize/rich/compare/v0.8.6...v0.8.7
[0.8.6]: https://github.com/textualize/rich/compare/v0.8.5...v0.8.6
[0.8.5]: https://github.com/textualize/rich/compare/v0.8.4...v0.8.5
[0.8.4]: https://github.com/textualize/rich/compare/v0.8.3...v0.8.4
[0.8.3]: https://github.com/textualize/rich/compare/v0.8.2...v0.8.3
[0.8.2]: https://github.com/textualize/rich/compare/v0.8.1...v0.8.2
[0.8.1]: https://github.com/textualize/rich/compare/v0.8.0...v0.8.1
[0.8.0]: https://github.com/textualize/rich/compare/v0.7.2...v0.8.0
[0.7.2]: https://github.com/textualize/rich/compare/v0.7.1...v0.7.2
[0.7.1]: https://github.com/textualize/rich/compare/v0.7.0...v0.7.1
[0.7.0]: https://github.com/textualize/rich/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/textualize/rich/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/textualize/rich/compare/v0.4.1...v0.5.0
[0.4.1]: https://github.com/textualize/rich/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/textualize/rich/compare/v0.3.3...v0.4.0
[0.3.3]: https://github.com/textualize/rich/compare/v0.3.2...v0.3.3
[0.3.2]: https://github.com/textualize/rich/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/textualize/rich/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/textualize/rich/compare/v0.2.0...v0.3.0
