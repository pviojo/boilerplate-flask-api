import sendgrid

class SendgridProvider(object):

    config = None
    def __init__(self, config):
        self.config = config
        self.provider = sendgrid.SendGridAPIClient(api_key=config['apikey'])

    def send(self, data):

        email_data = {
            "personalizations": [
                {
                    "to": [data['to']],
                    "subject": data['subject']
                }
            ],
            "from": data['from'],
            "content": [
                {
                    "type": "text/html",
                    "value": data['html']
                }
            ],
            "categories":data['categories']
        }
        try:
            response = self.provider.client.mail.send.post(request_body=email_data)
            return {
                'status_code': response.status_code,
                'message': 'OK' if response.status_code==202 else 'Error'
            }
        except Exception as e:
            print(e)
            return {
                'status_code': '400',
                'message': 'Error ({})'.format(e)
            }

        
