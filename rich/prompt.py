from typing import (
    Any,
    Generic,
    List,
    overload,
    Optional,
    TypeVar,
    Union,
)

from .__init__ import get_console
from .console import Console, RenderableType
from .text import Text, TextType


PromptType = TypeVar("PromptType")
DefaultType = TypeVar("DefaultType")


class PromptError(Exception):
    """Exception base class for prompt related errors."""


class InvalidResponse(PromptError):
    """Exception to indicate a response was invalid.

        Args:
        message (str): Error message.
    """

    def __init__(self, message: str) -> None:
        self.message = message

    def __rich__(self) -> RenderableType:
        return Text.from_markup(self.message)


class PromptBase(Generic[PromptType]):
    """Ask the user for input until a valid response is received.

    Args:
        prompt (TextType, optional): Prompt text. Defaults to "".
        console (Console, optional): A Console instance or None to use global console. Defaults to None.
        password (bool, optional): Enable password input. Defaults to False.
        choices (List[str], optional): A list of valid choices. Defaults to None.
        show_default (bool, optional): Show default in prompt. Defaults to True.
        show_choices (bool, optional): Show choices in prompt. Defaults to True.
    """

    response_type: type = str

    validate_error_message = "[prompt.invalid]Please enter a valid value"
    illegal_choice_message = (
        "[prompt.invalid.choice]Please select one of the available options"
    )
    prompt_suffix = ": "

    choices: Optional[List[str]] = None

    def __init__(
        self,
        prompt: TextType = "",
        *,
        console: Console = None,
        password: bool = False,
        choices: List[str] = None,
        show_default: bool = True,
        show_choices: bool = True,
    ) -> None:
        self.console = console or get_console()
        self.prompt = (
            Text.from_markup(prompt, style="prompt")
            if isinstance(prompt, str)
            else prompt
        )
        self.password = password
        if choices is not None:
            self.choices = choices
        self.show_default = show_default
        self.show_choices = show_choices

    @classmethod
    @overload
    def ask(
        cls,
        prompt: TextType = "",
        *,
        console: Console = None,
        password: bool = False,
        choices: List[str] = None,
        show_default: bool = True,
        show_choices: bool = True,
        default: DefaultType,
    ) -> Union[DefaultType, PromptType]:
        ...

    @classmethod
    @overload
    def ask(
        cls,
        prompt: TextType = "",
        *,
        console: Console = None,
        password: bool = False,
        choices: List[str] = None,
        show_default: bool = True,
        show_choices: bool = True,
    ) -> PromptType:
        ...

    @classmethod
    def ask(
        cls,
        prompt: TextType = "",
        *,
        console: Console = None,
        password: bool = False,
        choices: List[str] = None,
        show_default: bool = True,
        show_choices: bool = True,
        default: DefaultType = ...,
    ) -> PromptType:
        _prompt = cls(
            prompt,
            console=console,
            password=password,
            choices=choices,
            show_default=show_default,
            show_choices=show_choices,
        )
        return _prompt(default=default)

    def make_prompt(self, default: DefaultType) -> Text:
        """Make prompt text.

        Args:
            default (DefaultType): Default value.

        Returns:
            Text: Text to display in prompt.
        """
        prompt = self.prompt.copy()
        prompt.end = ""
        prompt.append(self.prompt_suffix)

        if self.show_choices and self.choices:
            _choices = "/".join(self.choices)
            choices = f"[{_choices}]"
            prompt.append(choices, "prompt.choices")
            prompt.append(" ")

        if (
            default != ...
            and self.show_default
            and isinstance(default, (str, self.response_type))
        ):
            prompt.append(f"({default})", "prompt.default")
            prompt.append(" ")

        return prompt

    @classmethod
    def get_input(cls, console: Console, prompt: TextType, password: bool) -> str:
        """Get input from user.

        Args:
            console (Console): Console instance.
            prompt (TextType): Prompt text.
            password (bool): Enable password entry.

        Returns:
            str: String from user.
        """
        return console.input(prompt, password=password)

    def check_choice(self, value: str) -> bool:
        """Check value is in the list of valid choices.

        Args:
            value (str): Value entered by user.

        Returns:
            bool: True if choice was valid, otherwise False.
        """
        assert self.choices is not None
        return value.strip() in self.choices

    def process_response(self, value: str) -> PromptType:
        """Process response from user, convert to prompt type.

        Args:
            value (str): String typed by user.

        Raises:
            InvalidResponse: If ``value`` is invalid.

        Returns:
            PromptType: The value to be returned from ask method.
        """
        value = value.strip()
        try:
            return_value = self.response_type(value)
        except ValueError:
            raise InvalidResponse(self.validate_error_message)

        if self.choices is not None and not self.check_choice(value):
            raise InvalidResponse(self.illegal_choice_message)

        return return_value

    def on_validate_error(self, value: str, error: InvalidResponse):
        """Called to handle validation error.

        Args:
            value (str): String entered by user.
            error (InvalidResponse): Exception instance the initiated the error.
        """
        self.console.print(error)

    @overload
    def __call__(self) -> PromptType:
        ...

    @overload
    def __call__(self, *, default: DefaultType) -> Union[PromptType, DefaultType]:
        ...

    def __call__(self, *, default: Any = ...) -> Any:
        """Run the prompt loop.

        Args:
            default (Any, optional): Optional default value.

        Returns:
            PromptType: Processed value.
        """
        while True:
            prompt = self.make_prompt(default)
            value = self.get_input(self.console, prompt, self.password)
            if value == "" and default != ...:
                return default
            try:
                return_value = self.process_response(value)
            except InvalidResponse as error:
                self.on_validate_error(value, error)
                continue
            else:
                return return_value


class Prompt(PromptBase[str]):
    """A prompt that returns a str."""

    response_type = str


class IntPrompt(PromptBase[int]):
    """A prompt that returns an integer."""

    response_type = int
    validate_error_message = "[prompt.invalid]Please enter a valid integer number"


class FloatPrompt(PromptBase[int]):
    """A prompt that returns a float."""

    response_type = float
    validate_error_message = "[prompt.invalid]Please enter a number"


class Confirm(PromptBase[bool]):
    """A yes / no confirmation prompt."""

    response_type = bool
    prompt_suffix = "? "
    validate_error_message = "[prompt.invalid]Please enter Y or N"
    choices = ["y", "N"]

    def process_response(self, value: str) -> PromptType:
        value = value.strip().lower()
        if value not in ["y", "n"]:
            raise InvalidResponse(self.validate_error_message)
        return value == "y"


if __name__ == "__main__":  # pragma: no cover

    from rich import print

    if Confirm.ask("Run prompt tests"):
        while True:
            result = IntPrompt.ask("Enter a number betwen 1 and 10", default=5)
            if result >= 1 and result <= 10:
                break
            print("[prompt.invalid]Number must be between 1 and 10")
        print(result)

        while True:
            password = Prompt.ask(
                "Please enter a password (must be at least 5 characters)", password=True
            )
            if len(password) >= 5:
                break
            print("[prompt.invalid]password too short")
        print(f"password={password!r}")

        fruit = Prompt.ask("Enter a fruit", choices=["apple", "orange", "pear"])
        print(f"fruit={fruit!r}")

    else:
        print("[b]OK")

