from textual.app import App
from textual.widgets import Header, Footer, Input, Button, Static
from textual.containers import Vertical

from pywiki.models.article import Article


class WikipediaTUI(App):
    """Main application for fetching and displaying Wikipedia articles."""

    CSS = """
    Screen {
        layout: vertical;
    }

    Header, Footer {
        dock: top;
        height: 3;
    }

    #input_container {
        height: auto;
        padding: 1;
    }

    #article_display {
        border: round yellow;
        padding: 1;
        height: 1fr;
    }

    Button {
        margin: 1 0;
        align: center middle;
    }
    """

    def compose(self):
        """Compose the UI layout."""
        yield Header()
        yield Vertical(
            Static("Wikipedia Article Viewer", id="title", expand=False),
            Vertical(
                Input(placeholder="Enter article title...", id="title_input"),
                Button("Fetch Article", id="fetch_article"),
                id="input_container"
            ),
            Static("", id="article_display", expand=True)
        )
        yield Footer()

    async def on_button_pressed(self, event):
        """Handle button press events."""
        if event.button.id == "fetch_article":
            # Get the article title from the input
            title = self.query_one("#title_input").value.strip()
            if not title:
                self.query_one("#article_display").update("Please enter a valid article title.")
                return

            # Fetch the article
            try:
                article = Article(title)
                self.query_one("#article_display").update(article.content)
            except Exception as e:
                self.query_one("#article_display").update(f"Error: {str(e)}")


def main():
    wiki_tui = WikipediaTUI()
    wiki_tui.run()


if __name__ == "__main__":
    main()
