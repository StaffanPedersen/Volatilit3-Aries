def get_all_plugins():
    """Return a list of available plugins for different operating systems."""
    try:
        windows_plugins = [
            'windows.info', 'windows.pslist', 'windows.pstree', 'windows.dlldump', 'windows.cmdline',
            'windows.netscan', 'windows.network', 'windows.filescan', 'windows.vaddump', 'windows.malfind',
            'windows.modules', 'windows.registry', 'windows.svcscan', 'windows.callbacks', 'windows.mutantscan',
            'windows.devicetree', 'windows.handles', 'windows.driverirp', 'windows.threads', 'windows.processes',
            'windows.apihooks', 'windows.privs', 'windows.procdump', 'windows.getsids', 'windows.sessions',
            'windows.envars', 'windows.hashdump', 'windows.userassist', 'windows.shellbags', 'windows.mftparser',
            'windows.psxview', 'windows.sockscan', 'windows.idt', 'windows.gdt', 'windows.timers',
            'windows.poolscanner', 'windows.bigpools', 'windows.dumpfiles', 'windows.virtmap', 'windows.kdbgscan',
            'windows.verinfo', 'windows.machoinfo', 'windows.shimcache', 'windows.lsadump', 'windows.dumptimers',
            'windows.threads', 'windows.psscan', 'windows.mbrparser', 'windows.driftdetect', 'windows.malwarebytes'
        ]
        linux_plugins = [
            'linux.info', 'linux.pslist', 'linux.pstree', 'linux.bash', 'linux.lsof',
            'linux.arp', 'linux.arp_cache', 'linux.iptables', 'linux.ifconfig', 'linux.netstat',
            'linux.route', 'linux.pidhashtable', 'linux.dmesg', 'linux.pstree', 'linux.sockstat',
            'linux.process_maps', 'linux.psxview', 'linux.shmodules', 'linux.check_modules', 'linux.cpuinfo',
            'linux.linux_kmsg', 'linux.linux_psaux', 'linux.memmap', 'linux.bash_history', 'linux.check_afinfo',
            'linux.list_afinfo', 'linux.mmap', 'linux.get_current', 'linux.get_system', 'linux.ioports',
            'linux.kconfig', 'linux.kptr_restrict', 'linux.load_modules', 'linux.lsmod', 'linux.mount',
            'linux.net', 'linux.psxview', 'linux.scan_afinfo', 'linux.slabinfo', 'linux.sockets',
            'linux.systemd', 'linux.timers', 'linux.umh', 'linux.unix_sockstat', 'linux.vmstat',
            'linux.mount_cache', 'linux.syscall', 'linux.kallsyms', 'linux.check_syscall'
        ]
        mac_plugins = [
            'mac.info', 'mac.pslist', 'mac.pstree', 'mac.check_syscall', 'mac.bash',
            'mac.lsof', 'mac.check_afinfo', 'mac.check_modules', 'mac.check_ifconfig', 'mac.check_route',
            'mac.check_arp', 'mac.check_netstat', 'mac.get_system', 'mac.get_current', 'mac.load_modules',
            'mac.mount', 'mac.net', 'mac.scan_afinfo', 'mac.slabinfo', 'mac.sockets',
            'mac.systemd', 'mac.timers', 'mac.umh', 'mac.unix_sockstat', 'mac.vmstat',
            'mac.mount_cache', 'mac.syscall', 'mac.kallsyms', 'mac.machoinfo', 'mac.processes',
            'mac.apihooks', 'mac.privs', 'mac.procdump', 'mac.getsids', 'mac.sessions',
            'mac.envars', 'mac.hashdump', 'mac.userassist', 'mac.shellbags', 'mac.mftparser',
            'mac.psxview', 'mac.sockscan', 'mac.idt', 'mac.gdt', 'mac.kdbgscan',
            'mac.verinfo', 'mac.shimcache', 'mac.lsadump', 'mac.dumptimers', 'mac.apihooks'
        ]

        plugin_list = [('Windows', windows_plugins), ('Linux', linux_plugins), ('Mac', mac_plugins)]

        return plugin_list
    except Exception as e:
        print("Exception occurred while fetching plugins:", str(e))
        return []