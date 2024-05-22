import os
import subprocess

from libqtile import widget
from libqtile.bar import Bar
from libqtile.config import Screen
from libqtile.log_utils import logger

from settings.themes import Colors
from settings.vars import ROOT

FONTS = "Fira code"
ICONS = "Fira Code"


def primary_widgets(colors: Colors):
    default_config = dict(background=colors["bg"], foreground=colors["fg"])
    return [
        *secondary_widgets(colors)[:-1],
        widget.Systray(**default_config, padding=8),
        widget.Clock(**default_config, format="%Y-%m-%d %a %I:%M %p"),
        widget.ThermalSensor(**default_config),
    ]


def secondary_widgets(colors: Colors):
    default_config = dict(background=colors["bg"], foreground=colors["fg"])
    return [
        widget.GroupBox(
            font=ICONS,
            padding=8,
            disable_drag=True,
            background=colors["bg"],
            highlight_method="block",
            this_current_screen_border=colors["selection"],
            this_screen_border="#2f343f",
        ),
        widget.Prompt(**default_config),
        widget.TaskList(
            **default_config,
            margin=0,
            padding=8,
            icon_size=16,
            highlight_method="block",
            max_title_width=128,
            border=colors["selection"],
        ),
        widget.Chord(
            **default_config,
            chord_colors={"launch": ("#ff0000", "#ffffff")},
            name_transform=lambda name: name.upper(),
        ),
        widget.Clock(**default_config, format="%Y-%m-%d %a %I:%M %p"),
    ]


def create_screens(colors: Colors):
    wallpaper_path = os.path.join(ROOT, "wallpapers", "1290914.png")
    screens = [
        Screen(
            wallpaper=wallpaper_path,
            wallpaper_mode="fill",
            top=Bar(
                widgets=primary_widgets(colors),
                size=32,
                opacity=0.96,
                margin=[5, 5, 0, 5],
            ),
        )
    ]
    xrandr_command = "xrandr --listmonitors | cut -d ' ' -f 2 | grep : | wc -l"
    process = subprocess.run(
        xrandr_command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if process.returncode != 0:
        error = process.stderr.decode("UTF-8")
        logger.error(f"Failed counting monitors using {xrandr_command}:\n{error}")
        connected_monitors = 1
    else:
        connected_monitors = int(process.stdout.decode("UTF-8"))

    if connected_monitors > 1:
        for _ in range(1, connected_monitors):
            screens.append(
                Screen(
                    wallpaper=wallpaper_path,
                    wallpaper_mode="fill",
                    top=secondary_widgets(colors),
                )
            )

    return screens
