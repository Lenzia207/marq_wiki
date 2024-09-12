import argparse
from src.documents.handle_documents import split_documents, load_documents
from src.db.handle_db import add_to_chroma, clear_database


CHROMA_PATH = "chroma"

def main():
    """ Main """
    # Check if the database should be cleared (using the --clear flag).
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    if args.reset:
        print("✨ Clearing Database")
        clear_database()

    # Create (or update) the data store.
    documents = load_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)


if __name__ == "__main__":
    main()