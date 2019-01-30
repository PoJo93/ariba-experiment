
from flask import jsonify


def build_response(cai_conversation, ariba_response):
    ariba_response_json = ariba_response.json()
    memory_response = cai_conversation.conversation_memory
    memory_response['approvables_totalElements'] = ariba_response_json.get('totalElements', '0')
    memory_response['approvables_content'] = ariba_response_json.get('content', '')
    response = jsonify(
        status=200,
        conversation={
            'memory': memory_response
        }
    )
    return response


class CAIConversation:
    """"Encapsulates the relevant attributes from a cai conversation"""

    @classmethod
    def from_json_payload(cls, payload: dict):
        print(payload)
        message = payload['nlp']['source']
        conversation_memory = payload['conversation']['memory']
        token = conversation_memory.get('token')
        channel = conversation_memory.get('channel')
        timestamp = payload['nlp']['timestamp']
        entities = payload['nlp']['entities']
        contact = conversation_memory.get('contact')
        return CAIConversation(message=message,
                               conversation_memory=conversation_memory,
                               token=token,
                               channel=channel,
                               timestamp=timestamp,
                               contact=contact,
                               entities=entities)

    def __init__(self, message: str, conversation_memory: str, token: str, channel: str, timestamp: str, contact: str, entities):
        self.message = message
        self.conversation_memory = conversation_memory
        self.token = token
        self.channel = channel
        self.timestamp = timestamp
        self.contact = contact
        self.entities = [Entity(n, ee) for n, e in entities.items() for ee in e]





class Entity():
  def __init__(self, name, entity):
    self.name = name

    for k, v in entity.items():
      setattr(self, k, v)

  def __repr__(self):
    attributes = []
    for method in dir(self):
      if not method.startswith('__') and method != 'name':
        value = getattr(self, method)
        attributes.append("{}={}".format(method, value))

    return "{} ({})".format(self.name, ', '.join(attributes))
