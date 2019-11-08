# dotfiles

Dotfiles and post install instructions for my Arch Linux setup with i3+plasma

## remember to

* install prezto
* activate services (tlp, lightdm, ...)
* [fix infinality](https://gist.github.com/cryzed/e002e7057435f02cc7894b9e748c5671https://gist.github.com/cryzed/e002e7057435f02cc7894b9e748c5671)

### generate .packages.txt

`pacman -Qet | awk -F' ' '{print $1}' >! .packages.txt`
