#!/usr/bin/env python3
"""A Python function that lists all documents in a collection"""


def list_all(mongo_collection):
    """list all documents in a collection"""
    # use find() to retrive all documents in the collection
    result = mongo_collection.find()

    # convert the result to a list of documents
    documents = list(result)

    # check if documents is empty
    if not documents:
        return []

    # return documents list
    return documents


if __name__ == "__main__":
    pass
