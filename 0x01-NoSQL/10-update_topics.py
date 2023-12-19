#!/usr/bin/env python3
"""A module that changes all topics of a school document based on the name"""


def update_topics(mongo_collection, name, topics):
    """updates all school topics matching a name field"""
    query = {"name": name}
    update = {"$set": {"topics": topics}}
    mongo_collection.update_many(query, update)


if __name__ == "__main__":
    pass
