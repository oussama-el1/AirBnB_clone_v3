#!/usr/bin/python3
"""Testing file
"""
import requests

if __name__ == "__main__":
    """ POST /api/v1/states
    """
    r = requests.post("http://127.0.0.1:5000/api/v1/states/", data={ 'name': "NewState" }, headers={ 'Content-Type': "application/x-www-form-urlencoded" })
    print(r.status_code)