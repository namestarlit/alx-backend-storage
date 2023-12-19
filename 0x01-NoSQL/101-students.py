#!/usr/bin/env python3
"""A module that returns all students sorted by average score"""


def top_students(mongo_collection):
    """retrives top students"""
    return mongo_collection.aggregate([
        {
            "$project": {
                "name": "$name",
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {"$sort": {"averageScore": -1}}
    ])
