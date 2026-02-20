from textual import on
from textual.app import ComposeResult
from textual.events import Key
from textual.widgets import Input, Static

from loader import LoaderScreen


class UserInput(Static):
    def compose(self) -> ComposeResult:
        yield Input(placeholder="Enter a movie name...", id="search_input")

    def on_mount(self) -> None:
        self.query_one("#search_input", Input).focus()

    @on(Key)
    def handle_keys(self, event: Key):
        if event.key == "escape":
            self.query_one("#search_input", Input).toggle_class("hidden")
            event.stop()
            return

    @on(Input.Submitted)
    def show_invalid_reasons(self):
        user_input: str = self.query_one(Input).value
        if user_input == "":
            self.notify("please enter a movie/series name")
            return

        self.query_one("#search_input", Input).value = ""
        self.query_one("#search_input", Input).add_class("hidden")

        # showing the loader
        self.app.push_screen(LoaderScreen(user_input))
