from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManager
from django.template import loader, Context
from django.db.models import Count
from server.models import *
from django.shortcuts import get_object_or_404
import server.utils as utils
from django.conf import settings

class Encryption(IPlugin):
    def widget_width(self):
        return 4
        
    def widget_content(self, page, machines=None, theid=None):

        try:
            show_desktops = settings.ENCRYPTION_SHOW_DESKTOPS
        except:
            show_desktops = True

        # The data is data is pulled from the database and passed to a template.

        # There are three possible views we're going to be rendering to - front, bu_dashbaord and group_dashboard. If page is set to bu_dashboard, or group_dashboard, you will be passed a business_unit or machine_group id to use (mainly for linking to the right search).
        if page == 'front':
            if show_desktops:
                t = loader.get_template('grahamgilbert/encryption/templates/front_desktops.html')
            else:
                t = loader.get_template('grahamgilbert/encryption/templates/front_laptops.html')

        if page == 'bu_dashboard':
            if show_desktops:
                t = loader.get_template('grahamgilbert/encryption/templates/id_desktops.html')
            else:
                t = loader.get_template('grahamgilbert/encryption/templates/id_laptops.html')

        if page == 'group_dashboard':
            if show_desktops:
                t = loader.get_template('grahamgilbert/encryption/templates/id_desktops.html')
            else:
                t = loader.get_template('grahamgilbert/encryption/templates/id_laptops.html')

        try:
            laptop_ok = machines.filter(facts__fact_name='mac_encryption_enabled', facts__fact_data='true').filter(facts__fact_name='mac_laptop', facts__fact_data='mac_laptop').count()
        except:
            laptop_ok = 0
        try:
            desktop_ok = machines.filter(facts__fact_name='mac_encryption_enabled', facts__fact_data__exact='true').filter(facts__fact_name='mac_laptop', facts__fact_data__exact='mac_desktop').count()
        except:
            desktop_ok = 0

        try:
            laptop_alert = machines.filter(facts__fact_name='mac_encryption_enabled', facts__fact_data__exact='false').filter(facts__fact_name='mac_laptop', facts__fact_data__exact='mac_laptop').count()
        except:
            laptop_alert = 0

        try:
            desktop_alert = machines.filter(facts__fact_name='mac_encryption_enabled', facts__fact_data__exact='false').filter(facts__fact_name='mac_laptop', facts__fact_data__exact='mac_desktop').count()
        except: 
            desktop_alert = 0

        c = Context({
            'title': 'Encryption',
            'laptop_label': 'Laptops',
            'laptop_ok_count': laptop_ok,
            'laptop_alert_count': laptop_alert,
            'desktop_ok_count': desktop_ok,
            'desktop_alert_count': desktop_alert,
            'desktop_label': 'Desktops',
            'plugin': 'Encryption',
            'theid': theid,
            'page': page
        })
        return t.render(c)

    def filter_machines(self, machines, data):
        if data == 'laptopok':
            machines = machines.filter(facts__fact_name='mac_encryption_enabled', facts__fact_data='true').filter(facts__fact_name='mac_laptop', facts__fact_data='mac_laptop')
            title = 'Laptops with encryption enabled'

        elif data == 'desktopok':
            machines = machines.filter(facts__fact_name='mac_encryption_enabled', facts__fact_data__exact='true').filter(facts__fact_name='mac_laptop', facts__fact_data__exact='mac_desktop')
            title = 'Desktops with encryption enabled'

        elif data == 'laptopalert':
            machines = machines.filter(facts__fact_name='mac_encryption_enabled', facts__fact_data__exact='false').filter(facts__fact_name='mac_laptop', facts__fact_data__exact='mac_laptop')
            title = 'Laptops without encryption enabled'

        elif data == 'desktopalert':
            machines = machines.filter(facts__fact_name='mac_encryption_enabled', facts__fact_data__exact='false').filter(facts__fact_name='mac_laptop', facts__fact_data__exact='mac_desktop')
            title = 'Desktops without encryption enabled'

        else:
            machines = None
            title = None

        return machines, title
