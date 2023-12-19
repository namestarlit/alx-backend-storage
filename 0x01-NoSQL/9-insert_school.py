#!/usr/bin/env python3
"""A module that inserts a new document in a collection based on kwargs"""


def insert_school(mongo_collection, **kwargs):
    """inserts a new document into a collection

    Args:
        **kwargs (dict): a key-value document fields data

    """
    # Insert the document into the collection and get the new _id
    result = mongo_collection.insert_one(kwargs)

    # Return the new _id
    return result.inserted_id


if __name__ == "__main__":
    pass
