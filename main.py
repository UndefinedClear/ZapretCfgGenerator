import os
from zipfile import PyZipFile, ZipFile
from bases import Bases, os_type

windows_bases = Bases('Windows')
linux_bases = Bases('Linux')


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

def generate_stratege(base_content, out_file: str = 'general_stratege_hyper.bat'):
    list_ = 'mega_list.txt'
    ipset_ = 'mega_ipset.txt'

    stratege_compiler(list_, ipset_)

    content = base_content

    content = content.replace('hostlist_file', list_)
    content = content.replace('ipset_file', ipset_)
        
    with open(out_file, 'w') as f:
        f.write(content)

    print('✅ Success : Compile Stratege')
    print(f'ℹ️ INFO : Put config and lists in zapret dir:\n-- List_name: {list_}\n-- IPSet_name: {ipset_}\n-- Config_Name: {out_file}')

    return [list_, ipset_, out_file]

def zip_it(zip_name : str = 'config.zip', listfile : str = '', ipsetfile : str = '', config : str = '', exclude: str = ''):
    with ZipFile(zip_name, 'w') as myzip:
        myzip.write(listfile)
        myzip.write(ipsetfile)
        myzip.write(config)
        myzip.write(exclude)

    print(f'ℹ️ Drop zip({zip_name}) into zapret dir and use "unzip {zip_name}"')


def clear_files(list_final, ipset_final, stratage_final):
    try:
        if os.path.exists(list_final):
            os.remove(list_final)
            print('✅ Success : Cleared ' + list_final)

        if os.path.exists(ipset_final):
            os.remove(ipset_final)
            print('✅ Success : Cleared ' + ipset_final)

        if os.path.exists(stratage_final):
            os.remove(stratage_final)
            print('✅ Success : Cleared ' + stratage_final)
        
    except Exception as e:
        print('❌ Error : Clear files : ' + str(e))
    else:
        print('✅ Success : Clear files')



def main():
    list_final, ipset_final, stratage_final = '', '', ''

    print('''Roblox works only on 1.9.0b of Zapret\n''')

    os_name = input('Enter os \n(1) Windows\n(2) Linux\n> ')

    if os_name == '1':
        print('\n\n' + '='*10 + 'Configs' + '='*10)

        for path in os.listdir('windows_bases'):
            print(path + '\n')

        alt = input('Enter alt name (just copy): ')

        alt_base = windows_bases.get_base_content(alt)

        # Use the alt filename (without extension) for the output file
        alt_name = os.path.splitext(alt)[0]  # Remove file extension
        list_final, ipset_final, stratage_final = generate_stratege(
            base_content=alt_base, 
            out_file=f'hyper_stratege_{alt_name}.bat'
        )

    elif os_name == '2':
        print('\n\n' + '='*10 + 'Configs' + '='*10)

        for path in os.listdir('linux_bases'):
            print(path + '\n')

        alt = input('Enter alt name (just copy): ')

        alt_base = linux_bases.get_base_content(alt)

        # Use the alt filename (without extension) for the output file
        alt_name = os.path.splitext(alt)[0]  # Remove file extension
        list_final, ipset_final, stratage_final = generate_stratege(
            base_content=alt_base, 
            out_file=f'general_hyper_stratege_{alt_name}.bat'  # general in the begining for detecting on linux
        )

    zip_it(listfile=list_final, ipsetfile=ipset_final, config=stratage_final, exclude= 'list-exclude.txt')

    clear_files(list_final, ipset_final, stratage_final)


main()