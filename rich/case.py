from .console import Console, ConsoleOptions, RenderableType, RenderResult
from .segment import Segment
from .style   import Style

# Experimenting with getting to know the __rich_console__ protocol. Tidying
# up and documentation and stuff to follow. Also need to remind myself how
# to type hint a method; as in, what the type hint for "pointer". I type
# hint "normal" Callables all the time but now I think about it I can't
# remember the last time I type-hinted an instance method.

class StrCaseBase:

    def __init__( self, renderable: RenderableType, case_filter ):
        self.renderable  = renderable
        self.case_filter = case_filter

    def __rich_console__( self, console: Console, options: ConsoleOptions ) -> RenderResult:
        for segment in console.render( self.renderable ):
            yield Segment( self.case_filter( segment.text ), segment.style )

class Upper( StrCaseBase ):

    def __init__( self, renderable: RenderableType ) -> None:
        super().__init__( renderable, str.upper )

class Lower( StrCaseBase ):

    def __init__( self, renderable: RenderableType ) -> None:
        super().__init__( renderable, str.lower )

class Capitalize( StrCaseBase ):

    def __init__( self, renderable: RenderableType ) -> None:
        super().__init__( renderable, str.capitalize )

class SwapCase( StrCaseBase ):

    def __init__( self, renderable: RenderableType ) -> None:
        super().__init__( renderable, str.swapcase )

### case.py ends here
