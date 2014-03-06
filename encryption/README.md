# Encryption

This plugin relies on the client having the [mac_facts](https://github.com/grahamgilbert/grahamgilbert-mac_facts) custom Facts installed, either through Puppet's built in plugin sync (if using Puppet), or by copying the .rb files to ``/usr/local/sal/facter``.

## Settings

This plugin has the option of showing both laptops and desktops (the default) or just laptops.

``` python
ENCRYPTION_SHOW_DESKTOPS = False
```

Will only show laptops.
