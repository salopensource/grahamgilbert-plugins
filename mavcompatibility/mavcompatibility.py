from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManager
from django.template import loader, Context
from django.db.models import Count
from server.models import *

class MavCompatibility(IPlugin):
    def show_widget(self, page, machines=None, theid=None):

        if page == 'front':
            t = loader.get_template('grahamgilbert/mavcompatibility/templates/front.html')
        
        if page == 'bu_dashboard':
            t = loader.get_template('grahamgilbert/mavcompatibility/templates/id.html')
        
        if page == 'group_dashboard':
            t = loader.get_template('grahamgilbert/mavcompatibility/templates/id.html')
            
        
        not_compatible = machines.filter(conditions__condition_name='supported_major_os_upgrades').exclude(conditions__condition_name='supported_major_os_upgrades', conditions__condition_data__contains='10.9').count()
        
        if not_compatible:
            size = 3
        else:
            size = 0

        c = Context({
            'title': '10.9 Compatibility',
            'not_compatible': not_compatible,
            'page': page,
            'theid': theid
        })
        return t.render(c), size
        
    def filter_machines(self, machines, data):
        if data == 'notcompatible':
            machines = machines.filter(conditions__condition_name='supported_major_os_upgrades').exclude(conditions__condition_name='supported_major_os_upgrades', conditions__condition_data__contains='10.9')
            title = 'Macs not compatible with OS X 10.9'
        else:
            machines = None
            title = None
        
        return machines, title