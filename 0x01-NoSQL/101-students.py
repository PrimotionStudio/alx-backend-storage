#!/usr/bin/env python3
"""
returns all students sorted by average score
"""

def top_students(mongo_collection):
    """
    returns all students sorted by average score
    """
    return mongo_collection.aggregate([
        {
            "$project": {
                "name": 1,
                "topics": 1,
                "averageScore": {
                    "$avg": "$topics.score"
                }
            }
        },
        {
            "$sort": {
                "averageScore": -1
            }
        }
    ])
