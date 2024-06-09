#!/bin/sh

# Network Manager icon
nm-applet &

# Volume icon
volumeicon &

# Battery icon
cbatticon -u 5 &

# set background
# bash $HOME/.config/qtile/scripts/.fehbg

# Launch notification daemon
#dunst -config $HOME/.config/qtile/dunstrc &

# picom start
picom --config $HOME/.config/qtile/picom.conf &

# policykit
/usr/lib/x86_64-linux-gnu/libexec/polkit-kde-authentication-agent-1 &
