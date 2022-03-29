import psutil


def getProcList():
    procList = []
    for proc in psutil.process_iter(attrs=['pid', 'name', 'username', 'memory_info', 'exe']):
       try:
           # Fetch process details as dict
           pinfo = proc.as_dict(attrs=['pid', 'name', 'username', 'exe'])
           pinfo['vms'] = proc.memory_info().vms / (1024 * 1024)
           # Append dict to list
           procList.append(pinfo)
       except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
           pass
    return procList

def getListOfProcessSortedByMemory():
    """
    Get list of running process sorted by Memory Usage
    """
    # Sort list of dict by key vms i.e. memory usage
    listOfProcObjects = sorted(getProcList(), key=lambda proc: proc['vms'], reverse=False)
    return listOfProcObjects

def getListOfProcessSortedByCPU():
    procList = []
    for proc in psutil.process_iter(attrs=['pid', 'name', 'username', 'cpu_percent', 'memory_info', 'exe']):
        try:
            # Fetch process details as dict
            pinfo = proc.as_dict(attrs=['pid', 'name', 'username', 'exe'])
            pinfo['cpu_percent'] = proc.cpu_percent(0.2) / psutil.cpu_count()
            pinfo['vms'] = proc.memory_info().vms / (1024 * 1024)
            # Append dict to list
            procList.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    procList = sorted(procList, key=lambda proc: proc['cpu_percent'], reverse=False)
    return procList

def killProcess(pid: int):
    proc = psutil.Process(pid)
    proc.terminate()

def printList(lst: list):
    for item in lst:
        print(item)

def main():
    option = ''
    while option != 'e':
        option = input('Выберите что вы хотите сделать:\n' +
                   'm: список процессов по потребяемой памяти\n' +
                   'c: список процессов по cpu\n' +
                   'k: убить процесс по его pid\n' +
                   'e: выйти из программы\n')
        if option == 'm':
            printList(getListOfProcessSortedByMemory())
        if option == 'c':
            printList(getListOfProcessSortedByCPU())
        if option == 'k':
            pid = input('Введите pid процесса: ')
            killProcess(int(pid))

if __name__ == '__main__':
   main()
