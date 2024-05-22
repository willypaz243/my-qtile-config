cd ~/
sudo apt install -y software-properties-common

sudo add-apt-repository non-free contrib -y

sudo apt install -y sudo git zsh curl wget neovim \
    alacritty chromium xserver-xorg xinit \
    libpangocairo-1.0-0 python3-pip \
    python3-xcffib python3-cairocffi \
    lightdm picom arandr fonts-firacode \
    hyfetch btop blueman volumeicon-alsa \
    ibus python3-psutil thunar pavucontrol \
    vlc

git clone https://github.com/qtile/qtile

cp qtile/resources/*.desktop /usr/share/xsessions/

sudo pip install qtile --break-system-packages

git clone https://github.com/newmanls/rofi-themes-collection.git

cd rofi-themes-collection

mkdir -p ~/.local/share/rofi/themes/

mv ./themes/* ~/.local/share/rofi/themes/

cd ..

rm -r rofi-themes-collection

cp .config/qtile/apps_configs/config.rasi .config/rofi/config.rasi