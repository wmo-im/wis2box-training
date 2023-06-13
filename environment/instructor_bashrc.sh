
# execute the below to remove color formatting from instructor VM
# in order to improve display when projecting

export PS1="\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[01;32m\]:\$ "
unalias ls
