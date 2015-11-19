from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManager
from django.template import loader, Context
from django.db.models import Count
from server.models import *
from django.shortcuts import get_object_or_404
import server.utils as utils
from django.conf import settings
import logging

class NetworkCheck(IPlugin):

    def widget_width(self):
        return 4
    
    def widget_content(self, page, machines=None, theid=None):
        if settings.DEBUG:
            logging.basicConfig(level=logging.INFO)
            logging.getLogger('yapsy').setLevel(logging.INFO)
        # The data is data is pulled from the database and passed to a template.

        # There are three possible views we're going to be rendering to - front, bu_dashbaord and group_dashboard. If page is set to bu_dashboard, or group_dashboard, you will be passed a business_unit or machine_group id to use (mainly for linking to the right search).
        if page == 'front':
            t = loader.get_template('grahamgilbert/shard/templates/front.html')

        if page == 'bu_dashboard':
            t = loader.get_template('grahamgilbert/shard/templates/id.html')

        if page == 'group_dashboard':
            t = loader.get_template('grahamgilbert/shard/templates/id.html')

        try:
            s1 = machines.filter(conditions__condition_name='shard', conditions__condition_data__lte='25').count()
        except:
            s1 = 0
        try:
            s2 = machines.filter(conditions__condition_name='shard', conditions__condition_data__lte='50').count()
        except:
            s2 = 0

        try:
            s3 = machines.filter(conditions__condition_name='shard', conditions__condition_data__lte='75').count()
        except:
            s3 = 0

        c = Context({
            'title': 'Shard',
            's1': s1,
            's2': s2,
            's3': s3,
            'plugin': 'Shard',
            'theid': theid,
            'page': page
        })
        print c
        return t.render(c)

    def filter_machines(self, machines, data):

        if data == 's1':
            machines = machines.filter(conditions__condition_name='shard', conditions__condition_data__lte='25')
            title = 'Machines in Shard 1'

        if data == 's2':
            machines = machines.filter(conditions__condition_name='shard', conditions__condition_data__lte='50')
            title = 'Machines in Shard 2'

        if data == 's3':
            machines = machines.filter(conditions__condition_name='shard', conditions__condition_data__lte='75')
            title = 'Machines in Shard 3'

        return machines, title
