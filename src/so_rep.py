#!/usr/bin/env python
## so_rep.py -- Show the SO reputation -*- Python -*-
## Time-stamp: "2009-03-10 14:26:58 ghoseb"

## Copyright (c) 2009, oCricket.com

import os
import re
import urllib
from django.utils import simplejson

from google.appengine.api import memcache
from google.appengine.ext.webapp import template

R_BADGES = re.compile("<a [^>]+ class=\"badge\"><span class=\"(.*?)\">.*?</span>.*?</a>(.*?)<br>", re.IGNORECASE)
R_MULTIPLIERS = re.compile("<span class=\"item-multiplier\">&times;&nbsp;(?P<multiplier>.*?)</span>", re.IGNORECASE)
R_REPUTATION = re.compile("<div class=\"summarycount\">[\D]+(?P<reputation>.*?)</div>", re.IGNORECASE)
R_NAME = re.compile("<div id=\"subheader\">\r\n[^<]+<h1>(?P<name>.*?)</h1>", re.IGNORECASE)
R_GRAVATAR = re.compile("<img src=\"(?P<gravatar_url>.*?)\?[^\"]+\" height=\"128\" width=\"128\"[^>]*>", re.IGNORECASE)

SO_URL = "http://stackoverflow.com/users/%s/"

def get_profile(user_id):
    """Get the profile of the user
    
    Arguments:
    - `user_id`: The SO User ID
    """
    data = memcache.get(user_id)
    if data is None:
        data = urllib.urlopen(SO_URL % user_id).read()
        memcache.set(user_id, data, 3600)
    return data

def sanitize_badges(badges):
    """Sanitize the badge data
    
    Arguments:
    - `badges`: Badge data
    """
    badge_codes = {'badge3': 'bronze',
                   'badge2': 'silver',
                   'badge1': 'gold'}

    def _get_badge_name(badge_code):
        return badge_codes.get(badge_code, None)

    def _get_badge_multiplier(badge_multiplier_data):
        try:
            return int(R_MULTIPLIERS.search(badge_multiplier_data).group('multiplier'))
        except AttributeError:
            return 1

    _badges = {}
    _badge_data = [(_get_badge_name(badge[0]), _get_badge_multiplier(badge[1])) for badge in badges]

    for badge in _badge_data:
        _badges[badge[0]] = _badges.get(badge[0], 0) + badge[1]

    return _badges

def get_badges(profile):
    """Get the badges that the user has
    
    Arguments:
    - `profile`: The profile data
    """
    return sanitize_badges(R_BADGES.findall(profile))


def get_reputation(profile):
    """Get the reputation of the user
    
    Arguments:
    - `profile`: The profile data
    """
    return R_REPUTATION.search(profile).group('reputation')

def get_name(profile):
    """Get the name of the user
    
    Arguments:
    - `profile`: The profile data
    """
    try:
        return R_NAME.search(profile).group('name')
    except AttributeError:
        return ""

def get_gravatar(profile):
    """Get the gravatar of the user
    
    Arguments:
    - `profile`: The profile data
    """
    try:
        return R_GRAVATAR.search(profile).group('gravatar_url') + '?s=48&d=identicon&r=PG'
    except AttributeError:
        return ""

def get_so_info(user_id, raw=False):
    """Get consolidated info about a SO user
    
    Arguments:
    - `user_id`: The user id
    """
    profile = get_profile(user_id)
    template_path = os.path.join(os.path.dirname(__file__), 'reputation.html')

    if raw:
        return simplejson.dumps({'user_id': user_id,
                                 'name': get_name(profile),
                                 'gravatar': get_gravatar(profile),
                                 'reputation': get_reputation(profile),
                                 'badges': get_badges(profile)})
    badges = get_badges(profile)
    template_values = {'user_id': user_id,
                       'name': get_name(profile),
                       'gravatar': get_gravatar(profile),
                       'reputation': get_reputation(profile),
                       'gold': badges.get('gold', None),
                       'silver': badges.get('silver', None),
                       'bronze': badges.get('bronze', None)}
    return simplejson.dumps({'data': template.render(template_path, template_values)})

if __name__ == '__main__':
    print get_so_info('8024', True)
