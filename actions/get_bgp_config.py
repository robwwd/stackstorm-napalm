from napalm import get_network_driver

from lib.action import NapalmBaseAction

class NapalmGetBGPConfig(NapalmBaseAction):

    def run(self, hostname, driver, port, credentials, group, neighbour):

        # Look up the driver  and if it's not given from the configuration file
        # Also overides the hostname since we might have a partial host i.e. from
        # syslog such as host1 instead of host1.example.com
        #
        (hostname, driver, credentials) = self.find_device_from_config(hostname, driver, credentials)

        if not driver:
            raise ValueError('Can not find driver for host {}, try with driver parameter.'.format(hostname))

        if not credentials:
            raise ValueError('Can not find credentials for host {}, try with credentials parameter.'.format(hostname))

        login = self._get_credentials(credentials)
        
        try:

            if not port:
                optional_args=None
            else:
                optional_args={'port': str(port)}

            with get_network_driver(driver)(
                hostname=str(hostname),
                username=login['username'],
                password=login['password'],
                optional_args=optional_args
            ) as device:

                if not group:
                    if not neighbour:
                        bgpconf = device.get_bgp_config()
                    else:
                        bgpconf = device.get_bgp_config(neighbor=neighbour)
                else:
                    if not neighbour:
                        bgpconf = device.get_bgp_config(group=group)
                    else:
                        bgpconf = device.get_bgp_config(group=group, neighbor=neighbour)

        except Exception, e:
            self.logger.error(str(e))
            return (False, str(e))

        return (True, bgpconf)
