from unittest.mock import patch


@patch('deliveries.celery.call_send_link_task')
def mock_call_send_link_task(*args, **keywargs):
    '''
    Mock for call function send link to slack in celery
    '''
    def call_function(link, delivery_id):
        return "{} {}".format(link, delivery_id)
    return call_function('', '')
