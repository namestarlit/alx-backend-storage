#!/usr/bin/env python3
"""A module that provides some stats about Nginx logs stored in MongoDB"""


def log_stats(mongo_collection):
    """retrives stats from nginx collection"""
    # Get the total number of logs
    total_logs = mongo_collection.count_documents({})
    print(f"{total_logs} logs")

    # Use aggregation to get the count of logs for each method
    pipeline = [
            {"$group": {"_id": "$method", "count": {"$sum": 1}}}
            ]
    methods_counts = list(mongo_collection.aggregate(pipeline))

    # Define the methods in the desired order
    ordered_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    for method in ordered_methods:
        count = (next((item["count"] for item in methods_counts
                       if item["_id"] == method), 0))
        print(f"\tmethod {method}: {count}")

    # Get the count of logs with method=GET and path=/status
    status_check_count = mongo_collection.count_documents(
            {"method": "GET", "path": "/status"})
    print(f"{status_check_count} status check")


if __name__ == "__main__":
    # Connect to MongoDB and specify the database and collection
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    nginx_collection = db.nginx

    # Call the log_stats function with the Nginx collection
    log_stats(nginx_collection)
