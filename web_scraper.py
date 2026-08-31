import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin


BASE_URL = "https://books.toscrape.com/"
OUTPUT_FILE = "books_dataset.csv"


def scrape_books():

    books = []
    page_url = BASE_URL

    while page_url:

        print("Scraping:", page_url)

        response = requests.get(
            page_url,
            timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Find all books on the page
        book_list = soup.select(
            "article.product_pod"
        )

        for book in book_list:

            # Book title
            title_tag = book.select_one(
                "h3 a"
            )

            # Price
            price_tag = book.select_one(
                ".price_color"
            )

            # Availability
            availability_tag = book.select_one(
                ".availability"
            )

            # Rating
            rating_tag = book.select_one(
                "p.star-rating"
            )

            # Extract rating
            rating = "Unknown"

            if rating_tag:

                rating_classes = rating_tag.get(
                    "class", []
                )

                for value in [
                    "One",
                    "Two",
                    "Three",
                    "Four",
                    "Five"
                ]:

                    if value in rating_classes:
                        rating = value
                        break

            # Store data
            if title_tag:

                title = title_tag.get(
                    "title",
                    title_tag.get_text(strip=True)
                )

                price = (
                    price_tag.get_text(strip=True)
                    if price_tag
                    else ""
                )

                availability = (
                    availability_tag.get_text(
                        " ",
                        strip=True
                    )
                    if availability_tag
                    else ""
                )

                book_url = urljoin(
                    page_url,
                    title_tag.get("href", "")
                )

                books.append({
                    "Title": title,
                    "Price": price,
                    "Availability": availability,
                    "Rating": rating,
                    "Book URL": book_url
                })

        # Find next page
        next_button = soup.select_one(
            "li.next a"
        )

        if next_button:

            page_url = urljoin(
                page_url,
                next_button["href"]
            )

        else:

            page_url = None

    return pd.DataFrame(books)


# Main program
if __name__ == "__main__":

    print("=" * 50)
    print("CODEALPHA WEB SCRAPING PROJECT")
    print("=" * 50)

    df = scrape_books()

    # Save dataset
    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    print("\nScraping completed!")
    print("Total books:", len(df))
    print("Dataset saved as:", OUTPUT_FILE)

    print("\nFirst 5 records:")
    print(df.head())