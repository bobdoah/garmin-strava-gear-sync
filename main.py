#!/usr/bin/python3

import click
import requests

REDIRECT = "https://connect.garmin.com/modern/"
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
URL_GC_LOGIN = 'https://sso.garmin.com/sso/signin?{}'.format(urllib.parse.urlencode(DATA))

def get_session(username, password):
    session = request.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, \
        like Gecko) Chrome/54.0.2816.0 Safari/537.36'})
    session.get(URL_GC_LOGIN)
    login_response = session.post(URL_GC_LOGIN, headers={'referer':URL_GC_LOGIN}, data={
        'username': username,
        'password': password,
        'embed': 'false',
        'rememberme':'on'
    })
    ticket = re.match(r".*\?ticket=([-\w]+)\";.*", login_response.text, flags=re.MULTILINE|re.DOTALL)
    if not(ticket):
        raise Exception('Did not get a ticket in the login response')
    click.echo('ticket: {}'.format(ticket.group(1)))
    return session
    


@click.command()
@click.argument('username')
@click.argument('password')
def get_gear(username, password)
    session = get_session(username, password)


