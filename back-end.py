import csv
import requests

API_URL = "https://openlibrary.org/search.json"

PARAMS = {
    "q": "python programming",
    "limit": 50,
    "fields": "title,author_name,first_publish_year,key"
}

MIN_YEAR = 2000


def fetch_books_from_api():
    try:
        response = requests.get(API_URL, params=PARAMS, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("docs", [])
    except requests.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return []


def filter_books_by_year(books, min_year):
    filtered_books = []
    for book in books:
        publish_year = book.get("first_publish_year")
        if publish_year and publish_year >= min_year:
            authors = book.get("author_name", ["Unknown Author"])
            author_name = authors[0] if authors else "Unknown Author"

            filtered_books.append({
                "title": book.get("title", "Untitled"),
                "author": author_name,
                "first_publish_year": publish_year,
                "key": book.get("key", "")
            })
    return filtered_books


def save_books_to_csv(books, filename="filtered_books.csv"):
    fieldnames = ["title", "author", "first_publish_year", "key"]
    try:
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for book in books:
                writer.writerow(book)
        print(f"Saved {len(books)} books to '{filename}'.")
    except IOError as e:
        print(f"Error writing CSV file: {e}")


def main():
    print("Fetching data from Open Library API...")
    all_books = fetch_books_from_api()

    if not all_books:
        print("No books were fetched or an error occurred.")
        return

    print(f"Fetched {len(all_books)} books. Filtering...")
    recent_books = filter_books_by_year(all_books, MIN_YEAR)

    if not recent_books:
        print(f"No books found with publish year >= {MIN_YEAR}.")
        return

    save_books_to_csv(recent_books)


if name == "__main__":
    main()