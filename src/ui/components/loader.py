from pyfiglet import figlet_format
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from textual.widgets import LoadingIndicator, Static


class LoaderScreen(ModalScreen):
    AUTO_FOCUS = None

    def __init__(self, user_query: str | None = None) -> None:
        super().__init__()
        self.user_query = user_query or ""

    def compose(self) -> ComposeResult:
        big = figlet_format("Searching", font="small")

        with Container(id="loader_root"):
            with Vertical(id="loader_overlay"):
                yield Static(
                    f"[cyan]{big}[/]\n[bold white]{self.user_query}[/]\n[dim]Please wait...[/]",
                    id="title",
                )
                yield LoadingIndicator(id="spinner")
