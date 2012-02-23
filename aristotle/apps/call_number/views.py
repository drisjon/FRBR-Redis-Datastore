"""
 mod:`views` Call Number Application Views
"""
__author__ = 'Jeremy Nelson'

import lib.frbr_rda as frbr,redis
from django.views.generic.simple import direct_to_template
from django.http import HttpResponse
import config,commands

redis_server = redis.StrictRedis(host=config.REDIS_HOST,
                                 port=config.REDIS_PORT,
                                 db=4)

def default(request):
    """
    Returns the default view for the Call Number Application
    """
    ## return HttpResponse("Call Number Application index")
    current = redis_server.hgetall('record:78')
    sort_position = int(current['sort-position'])
    return direct_to_template(request,
                              'call_number/default.html',
                              {'aristotle_url':'http://discovery.coloradocollege.edu/catalog/record/',
                               'current':current,
                               'next':commands.get_slice(sort_position-2,
                                                         sort_position-1),
                               'previous':commands.get_slice(sort_position+1,
                                                             sort_position+2)})

def widget(request):
    """
    Returns rendered html snippet of call number browser widget
    """
    return direct_to_template(request,
                              'call_number/snippets/widget.html',
                              {'call_number':'PS21 .D5185 1978'})