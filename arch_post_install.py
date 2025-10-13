#! /usr/bin/env python3

import subprocess
from datetime import date, timedelta
import os
import psutil

FILE_MIRRORLIST = "/etc/pacman.d/mirrorlist"
FILE_FSTAB = "/etc/fstab"
FILE_PACMANCONF = "/etc/pacman.conf"

##########
########## helper functions
##########


def term(cmds: list[str], *, capture_output: bool = False) -> str:
    # TODO: check if fail, and if so, ask the user to continue or quit
    proc = subprocess.run(cmds, check=True, capture_output=capture_output)
    if capture_output:
        return proc.stdout.decode()
    return ""


def pkg_install(pkgs: list[str]) -> None:
    term(["pacman", "-S", *pkgs])


##########
########## sub-functionalities
##########


def work_pin_mirrorlist_date() -> None:
    today = date.today()
    # yesterday = today - timedelta(days=1) # use this if `toda` fails

    with open(FILE_MIRRORLIST) as f:
        data = f.readlines()

    data = [f"# {line}" for line in data]
    data = "".join(data)

    data = (
        f"Server=https://archive.archlinux.org/repos/{today.strftime('%Y/%m/%d')}/$repo/os/$arch\n"
        + data
    )

    with open(FILE_MIRRORLIST, "w") as f:
        f.write(data)

    term(["pacman", "-Syyuu"])


def work_install_some_random_software() -> None:
    # fonts (required by micro and firefox)
    pkg_install(["noto-fonts"])  # regular
    pkg_install(["noto-fonts-cjk"])  # asian

    pkg_install(["discord", "libappindicator-gtk3", "libpulse", "xdg-utils"])
    pkg_install(["micro", "wl-clipboard", "xclip"])
    pkg_install(["firefox", "hunspell-en_us", "libnotify", "xdg-desktop-portal"])
    pkg_install(["btop", "rocm-smi-lib"])
    pkg_install(["steam", "polkit", "xdg-desktop-portal-impl"])
    pkg_install(["git", "less"])
    pkg_install(["mpv", "yt-dlp"])
    pkg_install(
        [
            "yt-dlp",
            "ffmpeg",
            "rtmpdump",
            "atomicparsley",
            "python-mutagen",
            "python-pycryptodome",
            "python-pycryptodomex",
            "python-websockets",
            "python-brotli",
            "python-brotlicffi",
            "python-xattr",
            "python-secretstorage",
        ]
    )  # TODO: install `phantomjs` using AUR helper # not needed: aria2

    # python dev
    pkg_install(["pyright"])

    pkg_install(["mangohud", "lib32-mangohud"])  # TODO: update environment


def work_video_drivers() -> None:
    # amd
    pkg_install(
        [
            "lib32-mesa",
            "vulkan-radeon",
            "lib32-vulkan-radeon",
            "vulkan-icd-loader",
            "lib32-vulkan-icd-loader",
        ]
    )


def work_shell(user: str) -> None:
    pkg_install(
        [
            "fish",
            "python",
            "pkgfile",
            "groff",
            "mandoc",
            "xsel",
            "xclip",
            "wl-clipboard",
        ]
    )
    fish_location = term(["which", "fish"], capture_output=True).strip()
    term(["chsh", "--shell", fish_location, user])


def work_get_user() -> str:
    _, users, _ = next(os.walk("/home"))
    assert len(users) == 1  # IMPROVE
    return users[0]


def work_swap_file() -> None:
    if psutil.swap_memory().total > 0:
        return

    term(["mkswap", "-U", "clear", "--size", "80G", "--file", "/swapfile"])
    term(["swapon", "/swapfile"])

    with open(FILE_FSTAB, "r") as f:
        data = f.read()

    data += "\n"
    data += "/swapfile none swap defaults 0 0\n"
    data += "\n"


def work_pacman_config() -> None:
    with open(FILE_PACMANCONF, "r") as f:
        data = f.read()

    data = data.replace("\n#Color\n", "\nColor\n")
    data = data.replace("\n#VerbosePkgLists\n", "\nVerbosePkgLists\n")

    with open(FILE_PACMANCONF, "w") as f:
        f.write(data)


def work_desktop_environment() -> None:
    # TODO
    ...


##########
########## main
##########


def main():
    user = work_get_user()

    work_pin_mirrorlist_date()
    work_pacman_config()

    work_video_drivers()

    work_install_some_random_software()  # needs to be ran after `work_video_drivers` - otherwise the user would get asked for a video driver because of steam
    work_shell(user)
    # work_home_structure(user)
    work_swap_file()
    work_desktop_environment()


if __name__ == "__main__":
    main()
