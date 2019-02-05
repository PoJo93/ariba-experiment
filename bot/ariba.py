import requests
import typing
from bot import Entity
from bot import CAIConversation

import urllib.parse

class AribaClient:
    """This client handles the calls to the Ariba API enpoints"""

    def _call_api(self, cai_conversation, api, parameters):
        return requests.get(api.get_address(parameters), verify=False, headers=api.headers)

    def call_pending_approvables_api(self, cai_conversation):
        parameters = []
        parameters.append(self.build_rsqlfilter(cai_conversation))
        return self._call_api(cai_conversation=cai_conversation, api=PendingApprovablesAPI, parameters=parameters)

    def build_rsqlfilter(self, cai_conversation: CAIConversation):
        expressions = []
        filter_money = []

        for entity in cai_conversation.entities:
            if entity.name in ('documenttype'):
                expressions.append('documentType=={0}'.format(entity.type))

            if entity.name in ('comparator', 'money'):
                filter_money.append(entity)

        if len(filter_money)==2:
            expressions.append('price{0}{1}'.format(filter_money[0].comparator, filter_money[1].amount))

        return 'rsqlfilter=({0})'.format(urllib.parse.quote_plus(' and '.join(expressions)))


    def show_approvables_from_response(self, ariba_response):
        carousel = {
            'type': 'carousel',
            'content': [],
        }
        content = ariba_response.json()['content']
        for element in content:
            subtitle = "This {0} document was approved by {1} with value of ${2}".format(element["documentType"], element['approverId'], element["price"])
            carousel_element = {
                                  'title': element["approvableUniqueName"],
                                  'subtitle': subtitle,
                                  'imageUrl': '',
                                  'buttons': []
                                }
            carousel['content'].append(carousel_element)

        return [carousel]



class AribaApiType:
    base_address = None
    headers = {}

    def get_address(self, parameters):
        return None

    def build_api_request(self, conversation: CAIConversation):
        pass


class PendingApprovablesAPI(AribaApiType):
    base_address = 'https://itg-openapi.aws.ariba.com:8443/api/approval-copilot/v1/sandbox/changes?realm=mytestrealm'
    headers = {"accept": "application/json", "apiKey": "5bb8b7009a294f408fd01a263a3bcd68"}

    @classmethod
    def get_address(cls, parameters):
        address = cls.base_address
        for p in parameters:
            address += '&' + p

        return address


    def build_api_request(self, conversation: CAIConversation):
        return ""









