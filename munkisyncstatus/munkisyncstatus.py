from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManager
from django.template import loader, Context
from django.db.models import Count, Avg
from server.models import *
from django.shortcuts import get_object_or_404
import server.utils as utils
from django.conf import settings
from datetime import datetime, timedelta

class MunkiSyncstatus(IPlugin):
    def show_widget(self, page, machines=None, theid=None):
        authorised_admins = settings.AUTHORISED_ADMINS
        # root will always be an admin (or it should!)
        if 'root' not in authorised_admins:
          authorised_admins.extend(['root'])
        if page == 'front':
            t = loader.get_template('grahamgilbert/munkisyncstatus/templates/front.html')
            if not machines:
                machines = Machine.objects.all()

        if page == 'bu_dashboard':
            t = loader.get_template('grahamgilbert/munkisyncstatus/templates/id.html')
            if not machines:
                machines = utils.getBUmachines(theid)

        if page == 'group_dashboard':
            t = loader.get_template('grahamgilbert/munkisyncstatus/templates/id.html')
            if not machines:
                machine_group = get_object_or_404(MachineGroup, pk=theid)
                machines = Machine.objects.filter(machine_group=machine_group)

        if machines:
            local = machines.filter(condition__condition_name='location', condition__condition_data='Local').count()
            cloud = machines.filter(condition__condition_name='location', condition__condition_data='Cloud').count()
            out_of_sync = machines.filter(condition__condition_name='location', condition__condition_data='Out-of-sync').count()

        else:
          local = 0
          cloud = 0
          out_of_sync = 0

        size = 3

        c = Context({
            'title': 'Munki Software Repository',
            'local_count': local,
            'local_label': 'Local',
            'cloud_count': cloud,
            'cloud_label': 'Cloud',
            'oos_count': out_of_sync,
            'oos_label': 'Out of sync',
            'plugin': 'MunkiSyncStatus',
            'theid': theid,
            'page': page,
            'label': label
        })
        return t.render(c), size

    def filter_machines(self, machines, data):
        if data == 'local':
            machines = machines.filter(condition__condition_name='location', condition__condition_data='Local')
            title = 'Machines using a local MSU cache'

        elif data == 'cloud':
            machines = machines.filter(condition__condition_name='location', condition__condition_data='Cloud')
            title = 'Machines using the Cloud MSU instance'

        elif data == 'out-of-sync':
            machines = machines.filter(condition__condition_name='location', condition__condition_data='Out-of-sync')
            title = 'Machines using the Cloud due to a sync error'

        else:
            machines = None
            title = None

        return machines, title
