#! /usr/bin/env python3

# INFO:
# next to each package you will see a date, this is the date where the optional dependencies were last evaluated

import subprocess
from datetime import date, timedelta
import os

FILE_MIRRORLIST = '/etc/pacman.d/mirrorlist'

##########
########## helper functions
##########

def term(cmds: list[str], *, capture_output:bool=False) -> None | str:
    # TODO: check if fail, and if so, ask the user to continue or quit
    proc = subprocess.run(cmds, check=True, capture_output=capture_output)
    if capture_output:
        return proc.stdout.decode()

def pkg_install(pkgs: list[str]) -> None:
    term(['sudo', 'pacman', '-S', *pkgs])

##########
########## sub-functionalities
##########

def work_pin_mirrorlist_date() -> None:
    today = date.today()
    yesterday = today - timedelta(days=1)

    with open(FILE_MIRRORLIST) as f:
        data = f.readlines()

    data = [f'# {line}' for line in data]
    data = ''.join(data)
    data += '\n'
    data += f'Server=https://archive.archlinux.org/repos/{yesterday.strftime('%Y/%m/%d')}/$repo/os/$arch\n'

    with open(FILE_MIRRORLIST, 'w') as f:
        f.write(data)

    term(['sudo', 'pacman', '-Syyuu'])

def work_install_some_random_software() -> None:
    pkg_install(['discord', 'libappindicator-gtk3', 'libpulse', 'xdg-utils']) # 2025.08.19
    pkg_install(['micro', 'wl-clipboard', 'xclip']) # 2025.08.19
    pkg_install(['firefox', 'hunspell-en_us', 'libnotify', 'xdg-desktop-portal']) # 2025.08.19
    pkg_install(['btop', 'rocm-smi-lib']) # 2025.08.19
    pkg_install(['steam']) # 2025.08.19
    pkg_install(['git', 'less']) # 2025.08.20

def work_video_drivers() -> None:
    # amd
    pkg_install(['lib32-mesa', 'vulkan-radeon', 'lib32-vulkan-radeon', 'vulkan-icd-loader', 'lib32-vulkan-icd-loader']) # never

def work_shell(user: str) -> None:
    pkg_install(['fish', 'python', 'pkgfile', 'groff', 'mandoc', 'xsel', 'xclip', 'wl-clipboard']) # 2025.08.19
    fish_location = term(['which', 'fish'], capture_output=True).strip()
    term(['sudo', 'chsh', '--shell', fish_location, user])

def work_get_user() -> str:
    _, users, _ = next(os.walk('/home'))
    assert len(users) == 1 # IMPROVE
    return users[0]

def work_home_directories(user: str) -> None:
    ... # TODO

##########
########## main
##########

def main():
    user = work_get_user()

    work_pin_mirrorlist_date()
    work_install_some_random_software()
    work_video_drivers()
    work_shell(user)
    work_home_directories(user)
    # TODO: setup swapfile

if __name__ == '__main__':
    main()
