"""Contains sample classes.

This was generated from the ChatGPT prompt:

> Generate a list of ideas for sample classes within python.

...

Book: A class to represent a book with attributes like title, author,
publication year, and methods to display book information, and update book
details.

...

> Generate a book class using the above example. Ensure that the book class is
  documented using numpydoc, but include several issues within the class that a
  novice programmer would make.

Here's a sample Book class with a few issues that a novice programmer might
make, documented using the numpydoc style:


"""


class Book:
    """
    A class to represent a book.

    Attributes
    ----------
    title : str
        The title of the book.
    author : str
        The author of the book.
    publication_year : int
        The year the book was published.

    Methods
    -------
    display_info():
        Prints the book's information.
    update_book_details(new_title, new_author, new_publication_year):
        Updates the book's details.
    """

    def __init__(self, title, author, publication_year):
        self.title = title
        self.author = author
        self.publication_year = publication_year

    def display_info(self):
        """
        Prints the book's information.
        """
        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        print(f"Publication Year: {self.publication_year}")

    def update_book_details(
        self, new_title=None, new_author=None, new_publication_year=None
    ):
        """
        Updates the book's details.

        Parameters
        ----------
        new_title : str, optional
            The new title of the book.
        new_author : str, optional
            The new author of the book.
        new_publication_year : int, optional
            The new year the book was published.
        """
        self.title = new_title if new_title is not None else self.title
        self.author = new_author if new_author is not None else self.author
        self.publication_year = (
            new_publication_year
            if new_publication_year is not None
            else self.publication_year
        )
