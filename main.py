#!/usr/bin/python3
import json
import re

import click
import requests

WEBHOST = "https://connect.garmin.com"
REDIRECT = "https://connect.garmin.com/modern/"
BASE_URL = "https://connect.garmin.com/en-US/signin"
SSO = "https://sso.garmin.com/sso"
CSS = "https://static.garmincdn.com/com.garmin.connect/ui/css/gauth-custom-v1.2-min.css"
DATA = {
    'service': REDIRECT,
    'webhost': WEBHOST,
    'source': BASE_URL,
    'redirectAfterAccountLoginUrl': REDIRECT,
    'redirectAfterAccountCreationUrl': REDIRECT,
    'gauthHost': SSO,
    'locale': 'en_US',
    'id': 'gauth-widget',
    'cssUrl': CSS,
    'clientId': 'GarminConnect',
    'rememberMeShown': 'true',
    'rememberMeChecked': 'false',
    'createAccountShown': 'true',
    'openCreateAccount': 'false',
    'usernameShown': 'false',
    'displayNameShown': 'false',
    'consumeServiceTicket': 'false',
    'initialFocus': 'true',
    'embedWidget': 'false',
    'generateExtraServiceTicket': 'true',
    'generateTwoExtraServiceTickets': 'false',
    'generateNoServiceTicket': 'false',
    'globalOptInShown': 'true',
    'globalOptInChecked': 'false',
    'mobile': 'false',
    'connectLegalTerms': 'true',
    'locationPromptShown': 'true',
    'showPassword': 'true'
}
URL_GC_LOGIN = 'https://sso.garmin.com/sso/signin'
URL_GC_ACTIVITIES = 'https://connect.garmin.com/modern/activities?'

def get_session(username, password):
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, \
        like Gecko) Chrome/54.0.2816.0 Safari/537.36'})
    session.get(URL_GC_LOGIN, params=DATA)
    login_response = session.post(URL_GC_LOGIN, params=DATA, headers={'referer':URL_GC_LOGIN}, data={
        'username': username,
        'password': password,
        'embed': 'false',
        'rememberme':'on'
    })
    login_response.raise_for_status()
    ticket = re.match(r".*\?ticket=([-\w]+)\";.*", login_response.text, flags=re.MULTILINE|re.DOTALL)
    if not(ticket):
        raise Exception('Did not get a ticket in the login response')
    click.echo('ticket: {}'.format(ticket.group(1)))
    login_auth_response = session.get(URL_GC_ACTIVITIES, params={'ticket': ticket})
    login_auth_response.raise_for_status()
    return session
    
GC_GEAR_TYPE_BIKE=1602583635934

def get_user_profile_pk(session):
    return 4726237

@click.command()
@click.argument('username')
@click.argument('password')
def get_gear_bike(username, password):
    session = get_session(username, password)
    response = session.get('https://connect.garmin.com/modern/proxy/gear-service/gear/filterGear', params={
        'userProfilePk': get_user_profile_pk(session),
        '_':GC_GEAR_TYPE_BIKE
    })
    gear = r.json()
    click.echo("Got gear:\n{}".format(json.dumps(gear)))

if __name__ == "__main__":
    get_gear()
