from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Footer, Header

from components.input import UserInput


class NetCliTui(App):
    AUTO_FOCUS = None

    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
        ("ctrl+h", "show_history", "show history"),
        ("ctrl+s", "save_to_watch_later", "watch later"),
        ("ctrl+f", "show_search", "search"),
        ("alt+d", "download_selected", "download"),
    ]

    CSS_PATH = "./styles/style.css"

    def compose(self) -> ComposeResult:
        yield Header(icon="📽", show_clock=True, id="header")
        with Horizontal(id="input_container"):
            yield UserInput()
        yield Footer()

    def on_mount(self) -> None:
        self.title = "Net-cli"
        self.sub_title = "A simple TUI for watching movies & series"

    def action_show_search(self) -> None:
        self.query_one("#search_input").remove_class("hidden")
        self.query_one("#search_input").focus()


app = NetCliTui()

if __name__ == "__main__":
    app.run()
