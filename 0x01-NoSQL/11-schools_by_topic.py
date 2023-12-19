#!/usr/bin/env python3
"""A module that returns the list of school having a specific topic"""


def schools_by_topic(mongo_collection, topic):
    """retrives a list of schools having certain topics"""
    # query the list of schools
    query = {"topics": {"$in": [topic]}}
    schools = mongo_collection.find(query)

    # Format and return the results
    schools = list(schools)

    # check if schools is empty
    if not schools:
        return []

    return schools


if __name__ == "__main__":
    pass
