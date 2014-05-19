from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManager
from django.template import loader, Context
from django.db.models import Count, Avg
from server.models import *
from django.shortcuts import get_object_or_404
import server.utils as utils
from django.conf import settings
from datetime import datetime, timedelta

class MemoryFree(IPlugin):
    def show_widget(self, page, machines=None, theid=None):

        if page == 'front':
            t = loader.get_template('grahamgilbert/memoryfree/templates/front.html')
            if not machines:
                machines = Machine.objects.all()

        if page == 'bu_dashboard':
            t = loader.get_template('grahamgilbert/memoryfree/templates/id.html')
            if not machines:
                machines = utils.getBUmachines(theid)

        if page == 'group_dashboard':
            t = loader.get_template('grahamgilbert/memoryfree/templates/id.html')
            if not machines:
                machine_group = get_object_or_404(MachineGroup, pk=theid)
                machines = Machine.objects.filter(machine_group=machine_group)

        if machines:
            time_90days = datetime.now() - timedelta(days=90)
            for machine in machines:
              memory_avg = HistoricalFact.objects.filter(machine=machine, fact_name='memoryfree_mb', fact_recorded__gte=time_90days).aggregate(Avg('fact_data'))
              if memory_avg['fact_data__avg'] != None:
                memory_avg['fact_data__avg'] = int(memory_avg['fact_data__avg'])
              print memory_avg['fact_data__avg']
              if memory_avg['fact_data__avg'] > 500 or memory_avg['fact_data__avg'] == None:
                machines = machines.exclude(id=machine.id)
            mem_out = machines.count()
        else:
          mem_out = 0

        if mem_out == 0:
          size = 0
        else:
          size = 3
        print machines
        c = Context({
            'title': 'Low Free Memory',
            'count': mem_out,
            'plugin': 'MemoryFree',
            'label': '< 500MB',
            'theid': theid,
            'page': page
        })
        return t.render(c), size

    def filter_machines(self, machines, data):
        time_90days = datetime.now() - timedelta(days=90)
        if data == 'under500':
            for machine in machines:
              memory_avg = HistoricalFact.objects.filter(machine=machine, fact_name='memoryfree_mb', fact_recorded__gte=time_90days).aggregate(Avg('fact_data'))
              if memory_avg['fact_data__avg'] != None:
                memory_avg['fact_data__avg'] = int(memory_avg['fact_data__avg'])
              print memory_avg['fact_data__avg']
              if memory_avg['fact_data__avg'] > 500 or memory_avg['fact_data__avg'] == None:
                machines = machines.exclude(id=machine.id)
            title = 'Machines with an average of less than 500MB of memory free'

        else:
            machines = None
            title = None

        return machines, title
