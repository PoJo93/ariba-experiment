#coding: utf-8

import os, json

from flask import Flask, request
from bot import cai, ariba


port = int(os.getenv("PORT"))
app = Flask(__name__)
ariba_client = ariba.AribaClient()

@app.route("/approvables/show", methods=['POST'])
def show_approvables():
    cai_json = json.loads(request.get_data().decode('utf-8'))
    cai_conversation = cai.CAIConversation.from_json_payload(cai_json)

    response = ariba_client.call_pending_approvables_api(cai_conversation)

    messages = ariba_client.process_ariba_response_approvables(response)
    return cai.build_response(cai_conversation, response, messages)


@app.route("/approvables/check", methods=['POST'])
def check_approvables():
    cai_json = json.loads(request.get_data().decode('utf-8'))
    cai_conversation = cai.CAIConversation.from_json_payload(cai_json)

    response = ariba_client.call_pending_approvables_api(cai_conversation)

    messages = ''
    return cai.build_response(cai_conversation, response, messages)


@app.route("/dialogflow/test", methods=['POST'])
def debug_dialogflow():
    request_json =json.loads(request.get_data().decode('utf-8'))
    print(json.dumps(request_json, indent=5, sort_keys=False))




if __name__ == '__main__':
   app.run(host='0.0.0.0', port=port)

