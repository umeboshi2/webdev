# webdev
setup web development environment in chroot with nodejs, rubygems, compass with plugins, coffeescript, grunt, bower

You will need schroot and an entry in /etc/schroot.conf before running the script.

schroot.conf:
```
[webdev]
type=directory
directory=/srv/chroots/webdev
users=<username>
root-users=<username>
```

`sudo python scripts/make-webdev-schroot.py [options] /srv/chroots/webdev`
