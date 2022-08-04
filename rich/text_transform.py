"""Console renderables for transforming text within other console renderables."""

# Python imports.
from typing import Callable

# Local Rich imports.
from .console import Console, ConsoleOptions, RenderableType, RenderResult
from .segment import Segment

# Experimenting with getting to know the __rich_console__ protocol. Tidying
# up and documentation and stuff to follow. Also need to remind myself how
# to type hint a method; as in, what the type hint for "pointer". I type
# hint "normal" Callables all the time but now I think about it I can't
# remember the last time I type-hinted an instance method.

class TextTransform:
    """A console renderable that transform text found in its contents.

    Example:
        >>> console.print( TextTransform( Panel( "Hello, World!" ), str.upper ) )

    Note:
        This class only really works well if the given transformation
        function works at the individual character level. While
        `transformer` can be called with strings that are multiple
        characters in length, there is no guarantee that logical groupings
        will be passed during calls to it. As an example of where this would
        be a problem, attempting to do anything at a word boundary would
        fail.

        Consider the difference of how `str.upper` works vs
        `str.capitalize`.

    Args:
        renderable (RenderableType): A console renderable object.
        transformer (Callable[[str],str]) A string transformation function to apply to all found text.
    """

    def __init__( self, renderable: RenderableType, transformer: Callable[ [ str ], str ] ) -> None:
        self.renderable  = renderable
        self.transformer = transformer

    def __rich_console__( self, console: Console, options: ConsoleOptions ) -> RenderResult:
        del options             # options is unused in here.
        for segment in console.render( self.renderable ):
            yield Segment( self.transformer( segment.text ), segment.style, segment.control )

class Upper( TextTransform ):
    """A console renderable that upper-cases all text found in its contents.

    Example:
        >>> console.print( Upper( Panel( "Hello, World!" ) ) )

    Args:
        renderable (RenderableType): A console renderable object.
    """

    def __init__( self, renderable: RenderableType ) -> None:
        super().__init__( renderable, str.upper )

class Lower( TextTransform ):
    """A console renderable that lower-cases all text found in its contents.

    Example:
        >>> console.print( Lower( Panel( "Hello, World!" ) ) )

    Args:
        renderable (RenderableType): A console renderable object.
    """

    def __init__( self, renderable: RenderableType ) -> None:
        super().__init__( renderable, str.lower )

class SwapCase( TextTransform ):
    """A console renderable that swaps the case of all text found in its contents.

    Example:
        >>> console.print( SwapCase( Panel( "Hello, World!" ) ) )

    Args:
        renderable (RenderableType): A console renderable object.
    """

    def __init__( self, renderable: RenderableType ) -> None:
        super().__init__( renderable, str.swapcase )

### text_transform.py ends here
