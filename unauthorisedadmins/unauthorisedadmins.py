from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManager
from django.template import loader, Context
from django.db.models import Count, Avg
from server.models import *
from django.shortcuts import get_object_or_404
import server.utils as utils
from django.conf import settings
from datetime import datetime, timedelta

class UnauthorisedAdmins(IPlugin):
    def show_widget(self, page, machines=None, theid=None):
        authorised_admins = settings.AUTHORISED_ADMINS
        # root will always be an admin (or it should!)
        if 'root' not in authorised_admins:
          authorised_admins.extend(['root'])
        if page == 'front':
            t = loader.get_template('grahamgilbert/unauthorisedadmins/templates/front.html')
            if not machines:
                machines = Machine.objects.all()

        if page == 'bu_dashboard':
            t = loader.get_template('grahamgilbert/unauthorisedadmins/templates/id.html')
            if not machines:
                machines = utils.getBUmachines(theid)

        if page == 'group_dashboard':
            t = loader.get_template('grahamgilbert/unauthorisedadmins/templates/id.html')
            if not machines:
                machine_group = get_object_or_404(MachineGroup, pk=theid)
                machines = Machine.objects.filter(machine_group=machine_group)

        if machines:
            facts = Fact.objects.filter(fact_name='mac_admin_users')
            for fact in facts:
              machine_id = fact.machine.id
              if fact.fact_data == "":
                fact_list.remove(item)
                break
              # split the fact data into a list
              fact_list = fact.fact_data.split(', ')
              # for each item that's not root in fact data, see if it's in the list
              for allowed_admin in authorised_admins:
                for item in fact_list:
                  if str(item) == str(allowed_admin):
                    fact_list.remove(item)
                    break
              if len(fact_list) == 0:
                machines = machines.exclude(id=fact.machine.id)
              # if the list has a lenght of 0, remove the machine from the machines result
            count = machines.count()
        else:
          count = 0

        if count == 0:
          size = 0
        else:
          size = 3

        if count == 1:
          label = "Admin"
        else:
          label = "Admins"

        c = Context({
            'title': 'Unathorised Admins',
            'count': count,
            'plugin': 'UnauthorisedAdmins',
            'theid': theid,
            'page': page,
            'label': label
        })
        return t.render(c), size

    def filter_machines(self, machines, data):
        if data == 'admins':
            authorised_admins = settings.AUTHORISED_ADMINS
            # root will always be an admin (or it should!)
            if 'root' not in authorised_admins:
              authorised_admins.extend(['root'])
            facts = Fact.objects.filter(fact_name='mac_admin_users')
            for fact in facts:
              machine_id = fact.machine.id
              if fact.fact_data == "":
                fact_list.remove(item)
                break
              # split the fact data into a list
              fact_list = fact.fact_data.split(', ')
              # for each item that's not root in fact data, see if it's in the list
              for allowed_admin in authorised_admins:
                for item in fact_list:
                  if str(item) == str(allowed_admin):
                    fact_list.remove(item)
                    break
              if len(fact_list) == 0:
                machines = machines.exclude(id=fact.machine.id)
            title = 'Machines with Admin users'

        else:
            machines = None
            title = None

        return machines, title
