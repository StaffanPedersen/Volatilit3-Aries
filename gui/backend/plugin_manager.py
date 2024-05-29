import frontend
import volatility3
import subprocess

def get_plugins(path_entry, plugin_entry, option_entry):
    # Get the input values
    path = path_entry.get()
    plugin = plugin_entry.get()
    option = option_entry.get()

    # List of valid plugins (replace this with the actual list of plugins)
    valid_plugins = [
        'banners.Banners', 'configwriter.ConfigWriter', 'frameworkinfo.FrameworkInfo', 'isfinfo.IsfInfo',
        'layerwriter.LayerWriter', 'linux.bash.Bash', 'linux.capabilities.Capabilities',
        'linux.check_afinfo.Check_afinfo',
        'linux.check_creds.Check_creds', 'linux.check_idt.Check_idt', 'linux.check_modules.Check_modules',
        'linux.check_syscall.Check_syscall', 'linux.elfs.Elfs', 'linux.envars.Envars', 'linux.iomem.IOMem',
        'linux.keyboard_notifiers.Keyboard_notifiers', 'linux.kmsg.Kmsg', 'linux.library_list.LibraryList',
        'linux.lsmod.Lsmod', 'linux.lsof.Lsof', 'linux.malfind.Malfind', 'linux.mountinfo.MountInfo',
        'linux.proc.Maps', 'linux.psaux.PsAux', 'linux.pslist.PsList', 'linux.psscan.PsScan', 'linux.pstree.PsTree',
        'linux.sockstat.Sockstat', 'linux.tty_check.tty_check', 'mac.bash.Bash', 'mac.check_syscall.Check_syscall',
        'mac.check_sysctl.Check_sysctl', 'mac.check_trap_table.Check_trap_table', 'mac.dmesg.Dmesg',
        'mac.ifconfig.Ifconfig',
        'mac.kauth_listeners.Kauth_listeners', 'mac.kauth_scopes.Kauth_scopes', 'mac.kevents.Kevents',
        'mac.list_files.List_Files', 'mac.lsmod.Lsmod', 'mac.lsof.Lsof', 'mac.malfind.Malfind', 'mac.mount.Mount',
        'mac.netstat.Netstat', 'mac.proc_maps.Maps', 'mac.psaux.Psaux', 'mac.pslist.PsList', 'mac.pstree.PsTree',
        'mac.socket_filters.Socket_filters', 'mac.timers.Timers', 'mac.trustedbsd.Trustedbsd',
        'mac.vfsevents.VFSevents',
        'timeliner.Timeliner', 'windows.bigpools.BigPools', 'windows.callbacks.Callbacks', 'windows.cmdline.CmdLine',
        'windows.crashinfo.Crashinfo', 'windows.devicetree.DeviceTree', 'windows.dlllist.DllList',
        'windows.driverirp.DriverIrp', 'windows.drivermodule.DriverModule', 'windows.driverscan.DriverScan',
        'windows.dumpfiles.DumpFiles', 'windows.envars.Envars', 'windows.filescan.FileScan',
        'windows.getservicesids.GetServiceSIDs', 'windows.getsids.GetSIDs', 'windows.handles.Handles',
        'windows.info.Info', 'windows.joblinks.JobLinks', 'windows.ldrmodules.LdrModules', 'windows.malfind.Malfind',
        'windows.mbrscan.MBRScan', 'windows.memmap.Memmap', 'windows.modscan.ModScan', 'windows.modules.Modules',
        'windows.mutantscan.MutantScan', 'windows.poolscanner.PoolScanner', 'windows.privileges.Privs',
        'windows.pslist.PsList', 'windows.psscan.PsScan', 'windows.pstree.PsTree',
        'windows.registry.certificates.Certificates', 'windows.registry.hivelist.HiveList',
        'windows.registry.hivescan.HiveScan', 'windows.registry.printkey.PrintKey',
        'windows.registry.userassist.UserAssist', 'windows.sessions.Sessions', 'windows.ssdt.SSDT',
        'windows.statistics.Statistics', 'windows.strings.Strings', 'windows.symlinkscan.SymlinkScan',
        'windows.thrdscan.ThrdScan', 'windows.truecrypt.Passphrase', 'windows.vadinfo.VadInfo',
        'windows.vadwalk.VadWalk', 'windows.virtmap.VirtMap'
    ]

   
    # Run the main script of your project and capture its output
    result = subprocess.run(['python', 'vol.py', '-f', path, plugin, option], stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)

    # Construct the command list
    command = ['python', 'vol.py', '-f', path, plugin]
    if option:
        command.append(option)

    print("Running command:", command)
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def get_plugins_from_file(path):
    print("hi")

def get_plugins_from_env(environment_variable):
    print("yo")