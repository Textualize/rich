from typing import Any, Generic, List, Optional, TextIO, TypeVar, overload
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
    choices: Optional[List[str]] = None

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
        _prompt = cls(
            prompt,
            console=console,
            password=password,
            choices=choices,
            case_sensitive=case_sensitive,
            show_default=show_default,
            show_choices=show_choices,
        )
        return _prompt(default=default, stream=stream)

    def render_default(self, default: DefaultType) -> Text:
        return Text(f"({default})", "prompt.default")

    def make_prompt(self, default: DefaultType) -> Text:
        prompt = self.prompt.copy()
        prompt.end = ""

        if self.show_choices and self.choices:
            prompt.append(f" [{'/'.join(self.choices)}]", "prompt.choices")

        if default != ... and self.show_default and isinstance(default, (str, self.response_type)):
            prompt.append(" ")
            prompt.append(self.render_default(default))

        prompt.append(self.prompt_suffix)
        return prompt

    @classmethod
    def get_input(
        cls,
        console: Console,
        prompt: TextType,
        password: bool,
        stream: Optional[TextIO] = None,
    ) -> str:
        return console.input(prompt, password=password, stream=stream)

    def check_choice(self, value: str) -> bool:
        if self.choices is None:
            return False
        return value.strip() in self.choices if self.case_sensitive else value.strip().lower() in [choice.lower() for choice in self.choices]

    def process_response(self, value: str) -> PromptType:
        value = value.strip()
        try:
            return_value: PromptType = self.response_type(value)
        except ValueError:
            raise InvalidResponse(self.validate_error_message)

        if self.choices is not None and not self.check_choice(value):
            raise InvalidResponse(self.illegal_choice_message)

        if not self.case_sensitive and self.choices:
            return_value = self.response_type(self.choices[[choice.lower() for choice in self.choices].index(value.lower())])

        return return_value

    def on_validate_error(self, value: str, error: InvalidResponse) -> None:
        self.console.print(error)

    def pre_prompt(self) -> None:
        pass

    def __call__(self, *, default: Any = ..., stream: Optional[TextIO] = None) -> Any:
        while True:
            self.pre_prompt()
            prompt = self.make_prompt(default)
            value = self.get_input(self.console, prompt, self.password, stream=stream)
            if value == "" and default != ...:
                return default
            try:
                return self.process_response(value)
            except InvalidResponse as error:
                self.on_validate_error(value, error)


class Prompt(PromptBase[str]):
    pass


class IntPrompt(PromptBase[int]):
    validate_error_message = "[prompt.invalid]Please enter a valid integer number"


class FloatPrompt(PromptBase[float]):
    validate_error_message = "[prompt.invalid]Please enter a number"


class Confirm(PromptBase[bool]):
    validate_error_message = "[prompt.invalid]Please enter Y or N"
    choices = ["y", "n"]

    def render_default(self, default: DefaultType) -> Text:
        return Text(f"({self.choices[0]})" if default else f"({self.choices[1]})", style="prompt.default")

    def process_response(self, value: str) -> bool:
        value = value.strip().lower()
        if value not in self.choices:
            raise InvalidResponse(self.validate_error_message)
        return value == self.choices[0]


if __name__ == "__main__":
    from rich import print

    if Confirm.ask("Run [i]prompt[/i] tests?", default=True):
        while True:
            result = IntPrompt.ask(":rocket: Enter a number between [b]1[/b] and [b]10[/b]", default=5)
            if 1 <= result <= 10:
                break
            print(":pile_of_poo: [prompt.invalid]Number must be between 1 and 10")
        print(f"number={result}")

        while True:
            password = Prompt.ask("Please enter a password [cyan](must be at least 5 characters)", password=True)
            if len(password) >= 5:
                break
            print("[prompt.invalid]password too short")
        print(f"password={password!r}")

        fruit = Prompt.ask("Enter a fruit", choices=["apple", "orange", "pear"])
        print(f"fruit={fruit!r}")

        doggie = Prompt.ask(
            "What's the best Dog? (Case INSENSITIVE)",
            choices=["Border Terrier", "Collie", "Labradoodle"],
            case_sensitive=False,
        )
        print(f"doggie={doggie!r}")

    else:
        print("[b]OK :loudly_crying_face:")