from typing import Any, Generic, List, Optional, TextIO, TypeVar, Union, overload

from . import get_console
from .console import Console
from .text import Text, TextType

PromptType = TypeVar("PromptType")
DefaultType = TypeVar("DefaultType")

class PromptError(Exception):
    pass

class InvalidResponse(PromptError):
    def __init__(self, message: TextType) -> None:
        self.message = message

    def __rich__(self) -> TextType:
        return self.message

class PromptBase(Generic[PromptType]):
    response_type: type = str
    validate_error_message = "[prompt.invalid]Please enter a valid value"
    illegal_choice_message = "[prompt.invalid.choice]Please select one of the available options"
    prompt_suffix = ": "

    def __init__(
        self,
        prompt: TextType = "",
        *,
        console: Optional[Console] = None,
        password: bool = False,
        choices: Optional[List[str]] = None,
        case_sensitive: bool = True,
        show_default: bool = True,
        show_choices: bool = True,
    ) -> None:
        self.console = console or get_console()
        self.prompt = Text.from_markup(prompt, style="prompt") if isinstance(prompt, str) else prompt
        self.password = password
        self.choices = choices
        self.case_sensitive = case_sensitive
        self.show_default = show_default
        self.show_choices = show_choices

    @classmethod
    def ask(
        cls,
        prompt: TextType = "",
        *,
        console: Optional[Console] = None,
        password: bool = False,
        choices: Optional[List[str]] = None,
        case_sensitive: bool = True,
        show_default: bool = True,
        show_choices: bool = True,
        default: Any = ...,
        stream: Optional[TextIO] = None,
    ) -> Any:
        return cls(prompt, console=console, password=password, choices=choices, case_sensitive=case_sensitive,
                   show_default=show_default, show_choices=show_choices)(default=default, stream=stream)

    def make_prompt(self, default: DefaultType) -> Text:
        prompt = self.prompt.copy()
        prompt.end = ""
        if self.show_choices and self.choices:
            prompt.append(f" [{'/'.join(self.choices)}]", "prompt.choices")
        if default != ... and self.show_default and isinstance(default, (str, self.response_type)):
            prompt.append(f" ({default})", "prompt.default")
        prompt.append(self.prompt_suffix)
        return prompt

    @classmethod
    def get_input(cls, console: Console, prompt: TextType, password: bool, stream: Optional[TextIO] = None) -> str:
        return console.input(prompt, password=password, stream=stream)

    def check_choice(self, value: str) -> bool:
        assert self.choices is not None
        return value.strip() in self.choices if self.case_sensitive else value.strip().lower() in map(str.lower, self.choices)

    def process_response(self, value: str) -> PromptType:
        value = value.strip()
        try:
            return_value: PromptType = self.response_type(value)
        except ValueError:
            raise InvalidResponse(self.validate_error_message)

        if self.choices and not self.check_choice(value):
            raise InvalidResponse(self.illegal_choice_message)
        return return_value

    def on_validate_error(self, value: str, error: InvalidResponse) -> None:
        self.console.print(error)

    def pre_prompt(self) -> None:
        pass

    def __call__(self, *, default: Any = ..., stream: Optional[TextIO] = None) -> Any:
        while True:
            self.pre_prompt()
            value = self.get_input(self.console, self.make_prompt(default), self.password, stream=stream)
            if value == "" and default != ...:
                return default
            try:
                return self.process_response(value)
            except InvalidResponse as error:
                self.on_validate_error(value, error)

class Prompt(PromptBase[str]):
    response_type = str

class IntPrompt(PromptBase[int]):
    response_type = int
