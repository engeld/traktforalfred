#!/usr/bin/python
# encoding: utf-8

import sys
import logging
from traktapi import TraktAPI
from workflow import Workflow


def main(wf):
    logging.basicConfig(level=logging.DEBUG)

    action = wf.args[0]
    if len(wf.args) > 1:
        params = wf.args[1:]

    traktapi = TraktAPI(wf)

    """
    Actions WITHOUT autentication
    """
    if action == 'auth':
        if traktapi.pin(params[0]):
            print 'Successfully authenticated.'
        else:
            print 'Invalid PIN. Please try again.'
        return

    """
    Actions WITH authentication
    """
    # check authentication
    if not traktapi.checkauth():
        wf.add_item(u'Not Authenticated', u'Please use the keyword trakt-auth and provide a valid PIN.')
        wf.send_feedback()
        return

    if action == 'user':
        user = traktapi.user()
        wf.add_item(user['user']['username'], u'Username')
        if user['user']['name']:
            wf.add_item(user['user']['name'], u'Name') 
        wf.add_item(str(user['user']['private']), u'Private') 
        wf.add_item(str(user['user']['vip']), u'VIP') 
        wf.add_item(user['user']['joined_at'], u'Joined') # FIXME: convert to human time
        if user['user']['location']:
            wf.add_item(user['user']['location'], u'Location')
        if user['user']['about']:
            wf.add_item(user['user']['about'], u'About') 
        if user['user']['gender']:
            wf.add_item(user['user']['gender'], u'Gender') 
        wf.add_item(str(user['user']['age']), u'Age') 
        #wf.add_item(user['user']['images'], u'Images') # FIXME: Add IMG support

    if action == 'calendar':
        calendar = traktapi.calendar()

        if calendar:
            wf.add_item(u'No Upcoming Events', u'No Upcoming events found')

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
