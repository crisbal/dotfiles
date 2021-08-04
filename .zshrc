# Lines configured by zsh-newuser-install
HISTFILE=~/.histfile
HISTSIZE=10000
SAVEHIST=10000
setopt autocd beep notify
bindkey -e
# End of lines configured by zsh-newuser-install
# The following lines were added by compinstall
zstyle :compinstall filename '/home/crisbal/.zshrc'

autoload -Uz compinit
compinit
# End of lines added by compinstall

export EDITOR=nano
export VISUAL=nano

# Source Prezto.
if [[ -s "${ZDOTDIR:-$HOME}/.zprezto/init.zsh" ]]; then
  source "${ZDOTDIR:-$HOME}/.zprezto/init.zsh"
fi

# z jump-around
[[ -r "/usr/share/z/z.sh" ]] && source /usr/share/z/z.sh

# aliases
alias cat=bat
alias pacman=trizen
alias aria='aria2c -c -x5 -s10 -m2'
