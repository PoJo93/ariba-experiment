import requests


class DynalistClient:
    #TODO add class description

    def _call_api(self, recast_conversation, api):
        payload = api.build_api_request(self, recast_conversation=recast_conversation)
        print(payload)
        return requests.post(api.address, json=payload)

    def call_check_token_api(self, recast_conversation):
        return self._call_api(recast_conversation=recast_conversation, api=CheckTokenAPI)

    def call_inbox_add_api(self, recast_conversation):
        return self._call_api(recast_conversation=recast_conversation, api=InboxAddAPI)


class DynalistApiType:
    address = None

    def build_api_request (self, recast_conversation):
        pass

class CheckTokenAPI(DynalistApiType):
    address = 'https://dynalist.io/api/v1/file/list'

    def build_api_request(self, recast_conversation):
        return {"token": recast_conversation.token}

class InboxAddAPI(DynalistApiType):
    address = 'https://dynalist.io/api/v1/inbox/add'

    def build_api_request(self, recast_conversation):
        note = str(DynalistNote.from_recast_conversation(recast_conversation))
        return {
            "token": recast_conversation.token,
            "content": recast_conversation.message,
            "note": note
        }



class DynalistNote:
    #TODO add class description

    @classmethod
    def from_recast_conversation(cls, response):
        return DynalistNote(response.channel, response.timestamp, response.contact)

    def __init__(self, channel, timestamp, contact):
        self.channel = channel
        self.timestamp = timestamp
        self.contact = contact

    def __str__(self):
        if self.channel:
            channel_str = '@' + self.channel
        else:
            channel_str = '@' + 'channel'

        time_str = '!(' + self.timestamp + ')'

        if self.contact:
            contact_str = '@' + self.contact
        else:
            contact_str = '@' + 'AContact'

        return '#message on {0} from {1} {2}'.format(channel_str, contact_str, time_str)