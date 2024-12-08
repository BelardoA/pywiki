import requests


class Article:
    """A class to represent a Wikipedia article.

    This class allows for the retrieval of a specific article's content from Wikipedia and provides functionality to search for articles based on a query. It initializes with a title and fetches the article content upon creation.

    Attributes:
        title (str): The title of the Wikipedia article.
        content (str): The content of the Wikipedia article.

    Args:
        title (str): The title of the article to be fetched from Wikipedia.

    Methods:
        fetch_article: Fetches the content of the article from Wikipedia.
        search_articles: Searches for articles on Wikipedia based on a query.
    """

    WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"

    def __init__(self, title, auto_fetch=True):
        self.title = title
        self.content = ''
        if auto_fetch:
            self.fetch_article()

    def fetch_article(self):
        """Fetch the content of the Wikipedia article.

        This function retrieves the content of the article specified by the title attribute. It updates the content
        attribute with the article's extract or sets it to a default message if the article is not found.

        Args:
            None

        Returns:
            None
        """
        params = {
            "action": "query",
            "format": "json",
            "titles": self.title,
            "prop": "extracts",
            "explaintext": False,
            "exintro": False,
        }
        response = requests.get(self.WIKIPEDIA_API_URL, params=params)
        data = response.json()
        print(data)
        page = next(iter(data['query']['pages'].values()))
        self.content = page['extract'] if 'extract' in page else 'Article not found'

    def search_articles(self, query, limit=5):
        """Search for articles on Wikipedia based on a query.

        This function queries the Wikipedia API to find articles that match the specified search term. It returns a list of article titles, limited to the specified number of results.

        Args:
            query (str): The search term to look for in Wikipedia articles.
            limit (int, optional): The maximum number of article titles to return. Defaults to 5.

        Returns:
            list: A list of article titles that match the search query.
        """
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": query,
            "srlimit": limit,
        }
        response = requests.get(self.WIKIPEDIA_API_URL, params=params)
        data = response.json()
        return [result['title'] for result in data['query']['search']]

    def set_wiki_url(self, wiki_url: str):
        """Set the Wikipedia URL for the article and searching."""
        self.WIKIPEDIA_API_URL = wiki_url


if __name__ == "__main__":
    article = Article("Python (programming language)")
    print(article.content)
    print(article.search_articles("Python"))