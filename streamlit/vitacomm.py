import requests

from utils.time import generate_start_and_end_datetime
from utils.tokenmanager import TokenManager
from config.settings import VITACOMM_URL, VITACOMM_API_KEY#, APPLIKATOR_BASE_URL 


def get_active_citizens():
    with TokenManager() as tm:
        token = tm.get_token()
        count = 100
        offset = 0
        overall_count = None

        users = []

        #url = APPLIKATOR_BASE_URL + '/dialogNet/accountOverview/getAccountDetailsPage'
        url = None

        payload ={'offset': offset, 'count': count, 'includeOverallEntryCount': True,
        'sortInfo':[{'sortDirection': 1,'sortProperty': 3}],'modelType': 'GetAccountDetailsPageRequest','roles':{'value':['Resident']},
        'actorStateToExclude':{'value': 4},'hasUserOptions':{'value':1},'includeDeletedUsers':{'value': False}}

        headers = {
            'Authorization': f'{token}',
            'Content-Type': 'application/json'
        }


        while overall_count is None or overall_count > offset:
            token = tm.get_token()
            headers = {'Authorization': f'{token}','Content-Type': 'application/json'}
            payload['offset'] = offset

            response = requests.post(url, json=payload, headers=headers)

            if response.status_code == 200:
                data =  response.json()
                overall_entry_count = data.get('errorOrValue', {}).get('value', {}).get('overallEntryCount')
                if overall_entry_count is not None:
                    overall_count = overall_entry_count
                    entries = data.get('errorOrValue', {}).get('value', {}).get('entries', [])
                    new_users = [entry.get('actor', {}).get('user', {})  for entry in entries]
                    if None in users:
                        raise ValueError('Last users value not available.')
                    else:
                        users =  users + new_users
                        offset = offset + count
                else:
                    raise Exception('Error: Failed to get the Overall Entry Count')
            else:
                raise Exception(response.text)
               
    return users

def get_call_log_api(days=30, start=None, end=None):
    start_datetime, end_datetime = generate_start_and_end_datetime(days, start, end)

    if (end_datetime - start_datetime).days > 30:
        raise Exception('Max date range is 30 days')
    
    params = {
        'api_key': VITACOMM_API_KEY, 
        'from': start_datetime.strftime('%Y-%m-%dT%H:%M:%S'),
        'to': end_datetime.strftime('%Y-%m-%dT%H:%M:%S')
    }

    response = requests.get(VITACOMM_URL, params=params)

    if response.status_code == 200:
       return response.content.decode('utf-8')
    else:
        raise Exception(response.text)