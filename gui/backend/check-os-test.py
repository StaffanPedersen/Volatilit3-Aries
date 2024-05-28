import platform

def get_os_info():
    os_type = platform.system()
    os_details = platform.version()
    os_release = platform.release()
    
    return os_type, os_release, os_details

os_type, os_release, os_details = get_os_info()

print(f"Operativsystem: {os_type}")
print(f"Versjon: {os_release}")
print(f"Detaljer: {os_details}")