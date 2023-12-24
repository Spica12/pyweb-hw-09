import json
import pathlib

from mongoengine import NotUniqueError

from models import Author, Quote

BASE_DIR = pathlib.Path(__file__).parent.parent.joinpath("data")


def delete_collections(model):
    collection = model.objects()

    for el in collection:
        object = model.objects(id=el.id).delete()


def seed_authors_from_json():
    file_name = "authors.json"
    file_path = BASE_DIR / file_name

    with open(file_path) as file:
        data = json.load(file)
        for el in data:
            try:
                author = Author(
                    fullname=el.get("fullname"),
                    born_date=el.get("born_date"),
                    born_location=el.get("born_location"),
                    description=el.get("description"),
                )
                
                if author.fullname == "Alexandre Dumas-fils":
                    author.fullname = "Alexandre Dumas fils"

                author.save()
            except NotUniqueError:
                print(f"Author {el.get('fullname')} exists.")


def seed_qoutes_from_json():
    file_name = "quotes.json"
    file_path = BASE_DIR / file_name

    with open(file_path) as file:
        data = json.load(file)
        for i, el in enumerate(data):
            author, *_ = Author.objects(fullname=el.get("author"))
            quote = Quote(
                quote=el.get("quote"),
                tags=el.get("tags"),
                author=author,
            )
            print(f"{i}. {quote.author.fullname}: {quote.quote}")

            quote.save()


if __name__ == "__main__":
    # Видалити усіх авторів, а з ними і цитати з БД
    delete_collections(Author)

    # Добавити авторів з json файлу
    seed_authors_from_json()

    # Добавити цитати з json файлу
    seed_qoutes_from_json()
