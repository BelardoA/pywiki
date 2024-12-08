from textual.app import App
from textual.widgets import Header, Footer, Input, Button, Static, Select
from textual.containers import Vertical
from articles import Article


class WikipediaTUI(App):
    """Main application for fetching and displaying Wikipedia articles with search suggestions."""

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

    Select {
        margin: 1 0;
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
                Button("Search Suggestions", id="search_suggestions"),
                Select(options=[], id="search_results"),
                Button("Fetch Article", id="fetch_article"),
                id="input_container"
            ),
            Static("", id="article_display", expand=True)
        )
        yield Footer()

    async def on_input_changed(self, event: Input.Changed):
        """Fetch suggestions dynamically as the user types."""
        if event.input.id == "title_input" and len(event.value) > 2:
            query = event.value.strip()
            article = Article(query, auto_fetch=False)  # No need to fetch content
            suggestions = article.search_articles(query)
            self.query_one("#search_results").options = [(s, s) for s in suggestions]

    async def on_button_pressed(self, event: Button.Pressed):
        """Handle button press events."""
        if event.button.id == "search_suggestions":
            # Populate suggestions
            query = self.query_one("#title_input").value.strip()
            if query:
                article = Article(query, auto_fetch=False)
                suggestions = article.search_articles(query)
                self.query_one("#search_results").options = [(s, s) for s in suggestions]

        elif event.button.id == "fetch_article":
            # Fetch the selected article
            selected_title = self.query_one("#search_results").value
            if not selected_title:
                self.query_one("#article_display").update("Please select an article from suggestions.")
                return

            # Fetch the article
            try:
                article = Article(selected_title)
                self.query_one("#article_display").update(article.content)
            except Exception as e:
                self.query_one("#article_display").update(f"Error: {str(e)}")


def main():
    wiki_tui = WikipediaTUI()
    wiki_tui.run()


if __name__ == "__main__":
    main()
