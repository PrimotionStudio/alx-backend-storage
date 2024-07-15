#!/usr/bin/env python3
"""
provides some stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    col_nginx = client.logs.nginx
    total = col_nginx.count_documents({})
    print(f'{total} logs')
    print("Methods:")
    method = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for met in method:
        print(f'\tmethod {met}: {col_nginx.count_documents({"method": met})}')
    status_total = col_nginx.count_documents({"path": "/status"})
    print(f'{status_total} status check')    
