from typing import (
    Any,
    Callable,
    ClassVar,
    Generic,
    List,
    overload,
    Optional,
    Type,
    TypeVar,
    Union,
)

from .__init__ import get_console
from .console import Console, RenderableType
from .text import Text, TextType


PromptType = TypeVar("PromptType")
DefaultType = TypeVar("DefaultType")


PromptValidater = Callable[[str], PromptType]


class PromptError(Exception):
    pass


class InvalidResponse(PromptError):
    def __init__(self, error_message: str):
        self.error_message = error_message

    def __rich__(self) -> RenderableType:
        print(repr(self.error_message))
        return Text.from_markup(self.error_message)


class PromptBase(Generic[PromptType]):
    response_type: Type[PromptType] = str

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
        self.prompt = Text.from_markup(prompt) if isinstance(prompt, str) else prompt
        self.password = password
        if choices is not None:
            self.choices = choices

        self.show_default = show_default
        self.show_choices = show_choices

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
    ):
        _prompt = cls(
            prompt,
            console=console,
            password=password,
            choices=choices,
            show_default=show_default,
            show_choices=show_choices,
        )
        return _prompt

    def make_prompt(self, default: DefaultType) -> Text:
        prompt = self.prompt.copy()
        prompt.end = ""
        if self.show_choices and self.choices:
            _choices = ",".join(self.choices)
            choices = f"[{_choices}]"
            prompt.append(" ")
            prompt.append(choices, "prompt.choices")

        if default != ... and self.show_default:
            prompt.append(" ")
            prompt.append(f"({default})", "prompt.default")
        prompt.append(self.prompt_suffix)
        return prompt

    @classmethod
    def get_input(cls, console: Console, prompt: TextType, password: bool) -> str:
        return console.input(prompt, password=password)

    def check_choice(self, value: str) -> bool:
        assert self.choices is not None
        return value.strip() in self.choices

    def process_response(self, value: str) -> PromptType:
        value = value.strip()

        if self.choices is not None and not self.check_choice(value):
            raise InvalidResponse(self.illegal_choice_message)

        try:
            return self.response_type(value)
        except ValueError:
            raise InvalidResponse(self.validate_error_message)

    def on_validate_error(self, value: str, error: InvalidResponse):
        self.console.print(error)

    @overload
    def __call__(self) -> PromptType:
        ...

    @overload
    def __call__(self, *, default: DefaultType) -> Union[PromptType, DefaultType]:
        ...

    def __call__(self, *, default: Any = ...,) -> Any:
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
    response_type = str


class IntPrompt(PromptBase[int]):
    response_type = int
    validate_error_message = "[prompt.invalid]Please enter a valid integer number"


class FloatPrompt(PromptBase[int]):
    response_type = float
    validate_error_message = "[prompt.invalid]Please enter a number"


if __name__ == "__main__":  # pragma: no cover

    def list_validate(value: str) -> List[str]:
        return list(value)

    class MyPrompt(Prompt):
        choices = ["foo", "bar"]

    MyPrompt.ask("Type something")

    prompt = Prompt("Enter a [i]number[/i]",)
    result = prompt(default="hello")
    # reveal_type(result)
    print(repr(result))
