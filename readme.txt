IDE
idle3.8 finlename &


SELINUX should be set to permissive
setenfoce 0
also edit /etc/selinux/config
set to permissive in there


disable firewalld


NETWORKING ISSUE
for some reason, netork may not start properly

This is not getting run automatically
It enables NetworkManager - even though its started in systemctl
nmcli networking on

This should show everything green and all cols populated
nmcli conn show

network config is in /etc/sysconfig/network-scripts

nmcli 
nmtui (text netwrk ui)

/etc/resolv.conf is DNS setup


