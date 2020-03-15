from flask import Blueprint, jsonify, request, redirect
import os, urllib
import requests
import slack

blueprint = Blueprint('slack', __name__, url_prefix='/slack')

AUTHORIZE_URL = 'https://slack.com/oauth/v2/authorize?'
ACCESS_URL = 'https://slack.com/api/oauth.v2.access'

@blueprint.route('/authorize', methods=['GET'])
def slack_authorize():
    scope = 'team:read,users:read,channels:join,chat:write'
    client_id = os.environ['SLACK_CLIENT_ID']
    redirect_uri = os.environ['SLACK_REDIRECT_URI']
    return redirect(AUTHORIZE_URL + urllib.parse.urlencode({ 'scope': scope, 'client_id': client_id, 'redirect_uri': redirect_uri }))

@blueprint.route('/access_redirect', methods=['GET'])
def slack_access_redirect():
    code = request.args.get('code')
    client_id = os.environ['SLACK_CLIENT_ID']
    client_secret = os.environ['SLACK_CLIENT_SECRET']

    #response = requests.get(ACCESS_URL, params={ 'client_id': client_id, 'client_secret': client_secret, 'code': code })
    
    client = slack.WebClient(token="")
    response = client.oauth_v2_access(client_id=client_id, client_secret=client_secret, code=code)
    os.environ['SLACK_BOT_ACCESS_TOKEN'] = response['access_token']

    client = slack.WebClient(token=os.environ['SLACK_BOT_ACCESS_TOKEN'])
    response = client.channels_join(name='#general')
    print(response)

    response = client.chat_postMessage(channel='#general', text='hello')
    print(response)

    return jsonify({'status': 'ok'})
