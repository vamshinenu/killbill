'''kbf'''
import psutil as p
import win32gui
import win32process
import getpass as gp
from re import search
import json
import os

'''
we by default give all the necesary processes that should
run and other than those process all other gets terminated
if user needs some exceptional processes that the script
should not affect then he can add processes into the list
the data is dumped into a exceptional_processes.json file
'''


def editExceptionalProcesses():
    process = {}
    process['tasks'] = []

    ip = input('\nenter process to add to execptional list:   ').split()

    with open('exceptional_processes.json') as sb:
        data = json.lo(sb)
        for p in ip:
            data['tasks'].append({'name': p+'.exe', 'type': 'user'})

        data['tasks'] = list(
            {
                each['name']:
                each for each in data['tasks']
            }.values()
            )
    sb.close()
    with open('exceptional_processes.json', 'w') as sb:
        json.dump(data, sb)
        # time.sleep(0.5)
        sb.close()


'''
getAllProcess is used to get all the processes using psutil module
and dumps the data into a all_processes.json file
'''


def getAllProcess():
    all_processes = {}
    all_processes['tasks'] = []

    with open('all_processes.json', 'w') as data_file:
        for process in p.process_iter(['pid', 'name', 'username']):
            all_processes['tasks'].append(process.info)

        json.dump(all_processes, data_file)
        data_file.close()


''' 
getUserProcess gets all the processes which are running under
the current user who is logined in by checking all_process.json
file for all the user process this removes all the system and
windows processes from the list
and appends the data into a user_processes.json file
'''


def getUserProcess():
    current_user = gp.getuser()
    user_processes = {}
    user_processes['tasks'] = []
    user_processes['timestamp'] = '0'

    with open('all_processes.json', 'r') as data_file:
        with open('user_processes.json', 'w') as user_data_file:

            data = (json.load(data_file))
            data_length = len(data['tasks'])

            for i in range(data_length):

                user = data['tasks'][i]['username']
                valid_user = user != None

                if valid_user and search(current_user, user):
                    user_processes['tasks'].append(data['tasks'][i])

            json.dump(user_processes, user_data_file)

        user_data_file.close()
    data_file.close()


''' 
This get all the user processes and all processes details
by using getUserProcess() and getallProcess() functions
'''


def getProcessesInfo():

    user_process_file_exists = True

    if os.path.exists('all_processes.json'):
        if os.path.exists('user_processes.json'):
            user_process_file_exists = False
        else:
            user_process_file_exists = True
    else:
        # print('getting all the processes...')
        getAllProcess()

        if user_process_file_exists:
            # print('getting all the user processes...')
            getUserProcess()
            user_process_file_exists = False

    if user_process_file_exists:
        # print('getting all the user processes...')
        getUserProcess()
        # value = terminateProcessess()


''' 
terminateProcesses gets all the processes and verifies
current process with user processes and exceptional processes
the processes which are not in exceptional processes will be terminated
'''


def terminateProcessess():
    gotvalue = True
    j = 0
    with open('exceptional_processes.json', 'r') as exec_data_file:
        with open('user_processes.json', 'r') as user_data_file:

            with open('active_processes.json') as active_data_file:
                active_data = json.load(active_data_file)
                adi = active_data['tasks']
                allen = len(adi)
                active_list = []
                try:
                    for i in range(allen):
                        active_list.append(adi[i]['name'])
                except:
                    pass
                    # print(active_list[0])

                exec_data = (json.load(exec_data_file))
                exec_data_length = len(exec_data['tasks'])
                exec_list = []
                for i in range(exec_data_length):
                    exec_list.append(exec_data['tasks'][i]['name'])

                user_data = (json.load(user_data_file))
                user_data_length = len(user_data['tasks'])

                for process in p.process_iter():
                    processname = process.name().lower()

                    while gotvalue and j < user_data_length:
                        if processname == user_data['tasks'][j]['name'].lower():
                            gotvalue = False
                        j += 1

                    if not gotvalue and processname not in exec_list:
                        if processname not in active_list:
                            # print(processname + ' stopped.')
                            # not printing the process name so that its no annyoing to me when it runs often!!!
                            process.kill()

                    j = 0
                    gotvalue = True

            active_data_file.close()
        user_data_file.close()
    exec_data_file.close()


'''
deleteDataFiles deletes all the files that are created
so that each time the script run new processes can be added
to the processes list
'''


def deleteDataFiles(delmsg):
    if os.path.exists('user_processes.json'):
        os.remove('user_processes.json')
    if os.path.exists('all_processes.json'):
        os.remove('all_processes.json')
    if os.path.exists('active_processes.json'):
        os.remove('active_processes.json')
    if delmsg:
        pass
        # print('deleteing cache data...')


# def editUserExceptionList():

    # with open()

def checkFile():
    basic_process_dict = {"tasks": []}
    if not os.path.exists('active_processes.json'):
        with open('active_processes.json', 'w') as file:
            json.dump(basic_process_dict, file)
            file.close()

    if not os.path.exists('temp.json'):
        with open('temp.json', 'w') as file:
            json.dump(basic_process_dict, file)
            file.close()


# def killbill():
#     print('''                                                                                                    
#    .mmmm.`hmmm.-mmmm``dmmm/   dmmm/       /mmmmmmdy/  .mmmm. dmmm+   ommmh      
#    -MMMM-oMMMs :MMMM``NMMM/   NMMM+       +MMMMymMMMo -MMMM. mMMMo   sMMMd      
#    -MMMM/NMMm` :MMMM``NMMM/   NMMM+       +MMMN /MMMy -MMMM. mMMMo   sMMMd      
#    -MMMMNMMM:  :MMMM``NMMM/  `NMMM+       +MMMNodMMm: -MMMM. NMMMo   yMMMd      
#     syyyyyyy-  .yhhh` yhhh:  `hmmN/       +MMMMmMMNh: -MMMM. NMMMo   yMMMd      
#     mMMMhMMMM.  NMMM+ sMMMd   ommmh       .hddh-.hddh.`hddd- yddd+   ommmh      
#     mMMMoyMMMh `NMMM+ yMMMd   yMMMm       .MMMM+`NMMM+ mMMMs sMMMm   -MMNN.     
#     mMMMo.NMMM/`NMMM+ yMMMMmm+yMMMMmmo    .MMMMdhMMMM: mMMMs sMMMMmms-MMMMmmh   
#     hmmm+ ommmh`dmmm/ ommmmmm+ommmmmmo    `ddddddddh+  hmmm+ +mmmmmms-mmmmmmh 
#                                                              kill bill v0.0.1
#                         Copyright (C) puppet Corporation. All rights reserved.''')


def get_window_pid(title):

    piditem = 0
    if title != '':
        hwnd = win32gui.FindWindow(None, title)
        pid = win32process.GetWindowThreadProcessId(hwnd)
        piditem = pid[1]

    with open('temp.json') as sb:
        data = json.load(sb)
        data['tasks'].append({'pid': piditem})
    sb.close()

    with open('temp.json', 'w') as sb:
        json.dump(data, sb)
        sb.close()


def winEnumHandler(hwnd, ctx):

    if win32gui.IsWindowVisible(hwnd):
        temp = win32gui.GetWindowText(hwnd)
        get_window_pid(temp)


def get_window_name():
    temp = []
    with open('temp.json') as file:
        data = (json.load(file))
        data_length = len(data['tasks'])

        for process in p.process_iter(['pid', 'name', 'username']):
            for i in range(data_length):
                if process.pid == data['tasks'][i]['pid']:
                    temp.append(process.info['name'].lower())

        temp = list(set(temp))
    file.close()
    with open('active_processes.json') as ap:
        data = json.load(ap)
        for prc in temp:
            data['tasks'].append({'name': prc})
    ap.close()

    with open('active_processes.json', 'w') as ap:
        json.dump(data, ap)
        ap.close()


def fileChecker():
    basic_process_dict = {"tasks": []}

    if not os.path.exists('active_processes.json'):
        with open('active_processes.json', 'w') as file:
            json.dump(basic_process_dict, file)
            file.close()

    if not os.path.exists('temp.json'):
        with open('temp.json', 'w') as file:
            json.dump(basic_process_dict, file)
            file.close()


def active_window():
    fileChecker()
    win32gui.EnumWindows(winEnumHandler, None)
    get_window_name()
    os.remove('temp.json')
