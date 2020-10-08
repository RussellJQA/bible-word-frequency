import os

import markdown2  # pip install markdown2

from get_bible_data import get_bible_books, get_book_nums
from utils import get_base_template_args, write_html


def get_bible_book_index_hrefs():

    bible_book_index_hrefs = {}

    bible_books = get_bible_books()
    for bible_book in bible_books:
        book_abbrev = bible_books[bible_book][0]
        book_num = str(get_book_nums()[book_abbrev]).zfill(2)
        bible_book_index_hrefs[bible_book] = (
            f"{book_num}-"
            f"{book_abbrev.lower()}/{book_abbrev.lower()}-index.html")

    return bible_book_index_hrefs


def write_site_index():

    description = "KJV Bible Chapter Word Frequencies"
    base_template_args = get_base_template_args(
        description,
        ",".join(["KJV", "Bible", "chapter", "word frequency"]),
        "Home: " + description,
    )

    with open("readme.md", "r") as read_file:
        readme_source = read_file.read()
    readme_html = markdown2.markdown(readme_source)
    readme_html = readme_html.replace("examples.md", "examples.html")
    #   GitHub repos's README.md file points to GitHub repos's examples.md file
    #   Update to point to corresponding examples.html file
    bible_book_index_hrefs = get_bible_book_index_hrefs()
    new_template_args = {
        "images_path": "./images",
        "styles_path": "./styles",
        "readme_html": readme_html,
        "bible_book_index_hrefs": bible_book_index_hrefs,
    }

    html_folder = os.path.join(os.getcwd(), "public_html")
    write_html(
        base_template_args,
        new_template_args,
        "templates/site_index.mako",
        html_folder,
        "index.html",
    )


def main():

    write_site_index()


if __name__ == "__main__":
    main()
