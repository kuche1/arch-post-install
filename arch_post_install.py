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


def pkg_install(pkgs: list[str], *, dep: bool = False) -> None:
    # `--needed` should not be a problem considering the fact that we
    # are supposed to do a full system upgrade beforehand
    arg_dep = [] if dep is False else ["--asdep"]
    term(["pacman", "-S", "--needed", *arg_dep, *pkgs])


##########
########## sub-functionalities
##########


def work_pin_mirrorlist_date() -> None:
    # TODO: need to make this check if the work has already been done
    # and if so, return

    today = date.today()  # using this sometimes fails, you need to use yesterday's date
    yesterday = today - timedelta(days=1)  # use this if `toda` fails

    with open(FILE_MIRRORLIST) as f:
        data = f.readlines()

    data = [f"# {line}" for line in data]
    data = "".join(data)

    data = (
        f"Server=https://archive.archlinux.org/repos/{yesterday.strftime('%Y/%m/%d')}/$repo/os/$arch\n"
        + data
    )

    with open(FILE_MIRRORLIST, "w") as f:
        f.write(data)

    term(["pacman", "-Syyuu"])


def work_some_user_software() -> None:
    pkg_install(["rsync"])
    pkg_install(["python"], dep=True)

    pkg_install(["sshfs"])

    pkg_install(["discord"])
    pkg_install(["libappindicator-gtk3", "libpulse", "xdg-utils"], dep=True)

    pkg_install(["micro"])
    pkg_install(["wl-clipboard", "xclip"], dep=True)

    pkg_install(["firefox"])
    pkg_install(["hunspell-en_us", "libnotify", "xdg-desktop-portal"], dep=True)

    pkg_install(["btop"])
    pkg_install(["rocm-smi-lib"], dep=True)

    pkg_install(["steam"])
    pkg_install(["polkit", "xdg-desktop-portal-impl"], dep=True)

    pkg_install(["git"])
    pkg_install(["less"], dep=True)

    pkg_install(["mpv"])
    pkg_install(["yt-dlp"], dep=True)

    pkg_install(["yt-dlp"])
    pkg_install(
        [
            # "aria2"
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
        ],
        dep=True,
    )
    # TODO: install `phantomjs` using AUR helper

    # python dev
    # pkg_install(["pyright"])

    # rust dev
    pkg_install(["rustup"])
    pkg_install(["lldb", "gdb"], dep=True)

    pkg_install(["mangohud", "lib32-mangohud"])
    # TODO: update /etc/environment


def work_video_drivers() -> None:
    # required by steam

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
    pkg_install(["fish"])
    pkg_install(
        [
            "python",
            "pkgfile",
            "groff",
            "mandoc",
            "xsel",
            "xclip",
            "wl-clipboard",
        ],
        dep=True,
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
        data_original = f.read()

    data_new = data_original
    data_new = data_new.replace("\n#Color\n", "\nColor\n")
    data_new = data_new.replace("\n#VerbosePkgLists\n", "\nVerbosePkgLists\n")

    if data_original != data_new:
        print(f"Updating {FILE_PACMANCONF}")
        with open(FILE_PACMANCONF, "w") as f:
            f.write(data_new)


def work_desktop_environment() -> None:
    "Install niri."

    # I prefer this over the default niri terminal alacritty
    pkg_install(["gnome-terminal"])
    pkg_install(["libnautilus-extension"], dep=True)

    pkg_install(["niri"])
    pkg_install(
        [
            "xdg-desktop-portal-impl",  # TODO: pick one: xdg-desktop-portal-gtk, xdg-desktop-portal-kde, xdg-desktop-portal-gnome, xdg-desktop-portal-hyprland, xdg-desktop-portal-lxqt, xdg-desktop-portal-wlr, xdg-desktop-portal-xapp, xdg-desktop-portal-dde, xdg-desktop-portal-cosmic, xdg-desktop-portal-kde
            # "alacritty",
            "bash",
            "fuzzel",
            "mako",
            "org.freedesktop.secrets",  # TODO: pick one: gnome-keyring, keepassxc, kwallet
            "swaybg",
            "swaylock",
            "waybar",
            "xdg-desktop-portal-gnome",
            "xdg-desktop-portal-gtk",
            "xwayland-satellite",
        ],
        dep=True,
    )


def work_fonts() -> None:
    pkg_install(
        [
            "noto-fonts",  # regular # for micro and firefox
            "noto-fonts-cjk",  # asian # for some websites in firefox
            "otf-font-awesome",  # for some icons in waybar
        ]
    )


##########
########## main
##########


def main():
    user = work_get_user()

    # pacman
    work_pin_mirrorlist_date()
    work_pacman_config()

    # software dependencies
    work_video_drivers()
    work_fonts()

    work_shell(user)
    # work_home_structure(user)
    work_swap_file()
    work_desktop_environment()

    work_some_user_software()


if __name__ == "__main__":
    main()
