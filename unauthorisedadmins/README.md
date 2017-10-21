# Unauthorised Admins

This plugin will show machines that have admin users that aren't defined in ``settings.py`` in ``AUTHORISED_ADMINS``. 

``AUTHORISED_ADMINS = [ 'someadminuser', 'anotheradminuser']``

This plugin requires the ``mac_admin_users`` fact from [mac_facts](https://github.com/grahamgilbert/grahamgilbert-mac_facts) to be installed as per the [Sal documentation](https://github.com/salopensource/sal/wiki/Installing-and-using-plugins).
