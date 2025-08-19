#! /usr/bin/env python3

import subprocess

"chsh --shell /usr/bin/fish me"

def term(cmds: list[str], *, capture_output:bool=False) -> None | str:
    # TODO: check if fail, and if so, ask the user to continue or quit
    proc = subprocess.run(cmds, check=True, capture_output=capture_output)
    if capture_output:
        return proc.stdout.decode()

def pkg_install(pkgs: list[str]) -> None:
    term(['pacman', '-S', *pkgs])

def main():
    # next to each package you will see a date, this is the date where the optional dependencies were last evaluated

    #####

    pkg_install(['discord', 'libappindicator-gtk3', 'libpulse', 'xdg-utils']) # 2025.08.19
    pkg_install(['micro', 'wl-clipboard', 'xclip']) # 2025.08.19
    pkg_install(['firefox', 'hunspell-en_us', 'libnotify', 'xdg-desktop-portal']) # 2025.08.19
    pkg_install(['btop', 'rocm-smi-lib']) # 2025.08.19
    pkg_install(['steam']) # 2025.08.19

    ##### video drivers

    # amd
    pkg_install(['lib32-mesa', 'vulkan-radeon', 'lib32-vulkan-radeon', 'vulkan-icd-loader', 'lib32-vulkan-icd-loader']) # never

    ##### shell

    pkg_install(['fish', 'python', 'pkgfile', 'groff', 'mandoc', 'xsel', 'xclip', 'wl-clipboard']) # 2025.08.19

    fish_location = term(['which', 'fish'], capture_output=True).strip()

    _, users, _ = next(os.walk('/home'))
    for user in users:
        term(['sudo', 'chsh', '--shell', fish_location, user])

if __name__ == '__main__':
    main()
