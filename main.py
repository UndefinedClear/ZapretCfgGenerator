import os

base = '''
@echo off
chcp 65001 > nul
:: 65001 - UTF-8

cd /d "%~dp0"
call service_status.bat zapret
call check_updates.bat soft
echo:

set BIN=%~dp0bin\


start "zapret: general" /min "%BIN%winws.exe" --wf-tcp=80,443 --wf-udp=443,50000-50100 ^
--filter-udp=443 --hostlist="hostlist_file" --dpi-desync=fake --dpi-desync-repeats=6 --dpi-desync-fake-quic="%BIN%quic_initial_www_google_com.bin" --new ^
--filter-udp=50000-50100 --ipset="ipset_file" --dpi-desync=fake --dpi-desync-any-protocol --dpi-desync-cutoff=d3 --dpi-desync-repeats=6 --new ^
--filter-tcp=80 --hostlist="hostlist_file" --dpi-desync=fake,split2 --dpi-desync-autottl=2 --dpi-desync-fooling=md5sig --new ^
--filter-tcp=443 --hostlist="hostlist_file" --dpi-desync=split2 --dpi-desync-split-seqovl=652 --dpi-desync-split-pos=2 --dpi-desync-split-seqovl-pattern="%BIN%tls_clienthello_www_google_com.bin"
'''


# base.replace('hostlist_file', '')
# base.replace('ipset_file', '')


def generate_mega_unblocks():
    mega_ipset = ''
    mega_list = ''

    configs = os.scandir('lists')

    for config in configs:
        if config.is_dir():
            continue

        if config.name.startswith('list'):
            with open(config.path, 'r') as f:
                mega_list += f.read()

        if config.name.startswith('ipset'):
            with open(config.path, 'r') as f:
                mega_ipset += f.read()

    print('✅ Success : Generate Mega Ublocks')

    return [mega_list, mega_ipset]


mega_config = generate_mega_unblocks()

mega_list = mega_config[0]
mega_ipset = mega_config[1]


def stratege_compiler(list_name, ipset_name):
    with open(list_name, 'w') as f:
        f.write(mega_list)

    with open(ipset_name, 'w') as f:
        f.write(mega_ipset)


    print('✅ Success : Compile Stratege')

    return [list_name, ipset_name]

def generate_stratege(stratage: str = 'general_stratege.bat'):
    list_ = 'mega_list.txt'
    ipset_ = 'mega_ipset.txt'

    stratege_compiler(list_, ipset_)

    content = base

    content = content.replace('hostlist_file', list_)
    content = content.replace('ipset_file', ipset_)

    with open(stratage, 'w') as f:
        f.write(content)


    print('✅ Success : Compile Stratege')
    print(f'ℹ️ INFO : Put config and lists in zapret dir:\n-- List_name: {list_}\n-- IPSet_name: {ipset_}\n-- Config_Name: {stratage}')


generate_stratege()