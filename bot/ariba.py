import requests
import typing
from bot import Entity
from bot import CAIConversation


class AribaClient:
    """This client handles the calls to the Ariba API enpoints"""

    def _call_api(self, cai_conversation, api):
        return requests.get(api.address, headers=api.headers)

    def call_pending_approvables_api(self, cai_conversation):
        return self._call_api(cai_conversation=cai_conversation, api=PendingApprovablesAPI)



class AribaApiType:
    address = None
    headers = {}

    def build_api_request(self, conversation: CAIConversation):
        pass


class PendingApprovablesAPI(AribaApiType):
    address = 'https://itg-openapi.aws.ariba.cm:8443/api/approval-copilot/v1/sandbox/changes?realm=mytestrealm'
    headers = {"accept": "application/json", "apiKey": "5bb8b7009a294f408fd01a263a3bcd68"}

    def build_api_request(self, conversation: CAIConversation):
        return ""








