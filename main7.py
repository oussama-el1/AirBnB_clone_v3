#!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    """ Get one state
    """
    state_id = '421a55f4-7d82-47d9-b54c-a76916479545'

    """ PUT /api/v1/states/<state_id>
    """
    r = requests.put("http://127.0.0.1:5000/api/v1/states/{}".format(state_id), data={ 'name': "NewStateName" }, headers={ 'Content-Type': "application/x-www-form-urlencoded" })
    print(r.status_code)
    
    #!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    """ POST /api/v1/states
    """
    r = requests.post("http://127.0.0.1:5050/api/v1/states/", data={ 'name': "NewState" }, headers={ 'Content-Type': "application/x-www-form-urlencoded" })
    print(r.status_code)