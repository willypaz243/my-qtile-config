import os
import subprocess

from libqtile import widget
from libqtile.bar import Bar
from libqtile.config import Screen
from libqtile.log_utils import logger

from settings.icons import calenic, clockic
from settings.themes import Colors
from settings.vars import ROOT

FONTS = "Fira code"
ICONS = "Material Icons"


def add_icon(icon, fg, bg):
    default_config = dict(background=bg, foreground=fg)
    return widget.TextBox(
        **default_config,
        font=ICONS,
        fontsize=15,
        text=icon,
        padding_x=16,
        margin=0,
    )


def primary_widgets(colors: Colors):
    default_config = dict(background=colors["bg"], foreground=colors["fg"])
    return [
        *secondary_widgets(colors)[:-1],
        widget.Systray(**default_config, padding_x=16, padding_y=8),
        add_icon("|", colors["fg"], colors["bg"]),
        add_icon(calenic, colors["green"], colors["bg"]),
        widget.Clock(**default_config, format="%b %d-%Y"),
        add_icon(clockic, colors["magenta"], colors["bg"]),
        widget.Clock(**default_config, format="%I:%M %p"),
    ]


def secondary_widgets(colors: Colors):
    default_config = dict(
        background=colors["bg"],
        foreground=colors["fg"],
        padding=8,
        margin=3,
        borderwidth=5,
    )
    return [
        widget.GroupBox(
            **default_config,
            font=ICONS,
            disable_drag=True,
            highlight_method="block",
            this_current_screen_border=colors["selection"],
            this_screen_border="#2f343f",
        ),
        widget.CurrentLayout(**default_config),
        widget.Prompt(**default_config),
        widget.TaskList(
            **{k: v for k, v in default_config.items() if k != "margin"},
            margin=1,
            icon_size=12,
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
    wallpaper_path = os.path.join(ROOT, "wallpapers", "2449340.png")
    screens = [
        Screen(
            wallpaper=wallpaper_path,
            wallpaper_mode="fill",
            top=Bar(
                widgets=primary_widgets(colors),
                size=32,
                opacity=0.96,
                margin=[5, 8, 0, 5],
            ),
        )
    ]
    xrandr_command = "xrandr --listmonitors | cut -d ' ' -f 2 | grep : | wc -l"
    process = subprocess.run(
        xrandr_command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )

    if process.returncode != 0:
        error = process.stderr.decode("UTF-8")
        logger.error("Failed counting monitors using %s:\n%s", xrandr_command, error)
        connected_monitors = 1
    else:
        connected_monitors = int(process.stdout.decode("UTF-8"))

    if connected_monitors > 1:
        for _ in range(1, connected_monitors):
            screens.append(
                Screen(
                    wallpaper=wallpaper_path,
                    wallpaper_mode="fill",
                    top=Bar(
                        widgets=secondary_widgets(colors),
                        size=32,
                        opacity=0.96,
                        margin=[5, 8, 0, 5],
                    ),
                )
            )

    return screens
