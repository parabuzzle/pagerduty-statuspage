import os
from pdpyras import APISession

API_KEY = os.getenv('PDSTATUS_API_KEY')

session = APISession(API_KEY)

def top_level_services():
    data = session.get('business_services/impacts', headers={'X-EARLY-ACCESS': 'business-impact-early-access'}, params={'limit':50})
    return data.json()

def fetch_impacting(service_id):
    url = f'business_services/{service_id}/supporting_services/impacts'
    data = session.get(url, headers={'X-EARLY-ACCESS': 'business-impact-early-access'}, params={'limit':50})
    return data.json()

def fetch_impactors(service_id):
    url = 'business_services/impactors'
    data = session.get(url, headers={'X-EARLY-ACCESS': 'business-impact-early-access'}, params={'limit':50, 'ids[]':service_id})
    return data.json()

def fetch_incident_log(id):
    url = f'/incidents/{id}/log_entries'
    data = session.get(url, params={'limit':50})
    return data.json()

def fetch_incident(id):
    url = f'/incidents/{id}'
    data = session.get(url, params={'limit':50})
    return data.json()

def fetch_business_service(id):
    url = f'business_services/{id}'
    data = session.get(url, headers={'X-EARLY-ACCESS': 'business-impact-early-access'})
    return data.json()