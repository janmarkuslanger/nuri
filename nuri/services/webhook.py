import requests
from nuri.models import WebhookItem, RequestMethod


def fetch(url, method):
    try:
        if method == RequestMethod.GET:
            response = requests.get(url)
        elif method == RequestMethod.POST:
            response = requests.post(url)
            
        response.raise_for_status()
    except:
        pass


def trigger(webhook_type):
    try:
        items = WebhookItem.query.filter(WebhookItem.type == webhook_type).all()
    except:
        items = []
        
    for item in items:
        fetch(item.webhook.url, item.webhook.request_method)