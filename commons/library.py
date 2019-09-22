import requests
from datetime import date, datetime, time, timedelta
from django.conf import settings
from django.urls import reverse


def send_slack_message(slack_id, menu_id):
    url = "{}{}".format(settings.SLACK_SERVICE_URL, slack_id)
    link = reverse('delivery-selection', kwargs={'id': str(menu_id)})
    message = "Hola\n El menu lo puedes encontar \n <{}{}|Aqui>\nQue tengas un bello dia"\
        .format(settings.BASE_URL, link)

    headers = {
        'content-type': 'application/json',
    }
    data = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": message
                }
            }
        ]
    }
    response = requests.post(
        url,
        headers=headers,
        data=str(data)
    )
    return response


def is_number_or_string(value):
    return isinstance(value, int) or isinstance(value, str)


def get_index_value(elem):
    return str(elem) if is_number_or_string(elem) else str(elem.id)


def get_datetime(hours):
    return datetime.combine(date.today(), time()) + timedelta(hours=hours)
