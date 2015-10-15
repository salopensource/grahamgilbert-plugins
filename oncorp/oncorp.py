from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManager
from django.template import loader, Context
from django.db.models import Count
from server.models import *
from django.shortcuts import get_object_or_404
import server.utils as utils
from django.conf import settings

class OnCorp(IPlugin):
    def plugin_type(self):
        return 'condition'

    def show_widget(self, page, machines=None, theid=None):

        if page == 'front':
            t = loader.get_template('grahamgilbert/oncorp/templates/front.html')

        if page == 'bu_dashboard':
            t = loader.get_template('grahamgilbert/oncorp/templates/id.html')

        if page == 'group_dashboard':
            t = loader.get_template('grahamgilbert/oncorp/templates/id.html')

        if machines:
            oncorp = machines.filter(conditions__condition_name='on_corp', conditions__condition_data='True').count()
            offcorp = machines.filter(conditions__condition_name='on_corp', conditions__condition_data='False').count()
        else:
            oncorp = 0
            offcorp = 0

        c = Context({
            'title': 'Corportate Network',
            'oncorp_label': 'On Corp',
            'oncorp_count': oncorp,
            'offcorp_label': 'Off Corp',
            'offcorp_count': offcorp,
            'plugin': 'OnCorp',
            'theid': theid,
            'page': page
        })
        return t.render(c), 4

    def filter_machines(self, machines, data):
        if data == 'oncorp':
            machines = machines.filter(conditions__condition_name='on_corp', conditions__condition_data='True')
            title = 'Machines on Corportate Network'

        elif data == 'offcorp':
            machines = machines.filter(conditions__condition_name='on_corp', conditions__condition_data='False')
            title = 'Machines off Corportate Network'

        else:
            machines = None
            title = None

        return machines, title
