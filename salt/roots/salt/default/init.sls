# -*- mode: yaml -*-

{% set emacs = 'emacs23' %}
{% if salt['grains.get']('oscodename') == 'jessie' %}
{% set emacs = 'emacs24' %}
{% endif %}

pager:
  pkg.installed:
    - name: most
  alternatives.set:
    - name: pager
    - path: /usr/bin/most

emacs:
  pkg.installed:
    - name: {{ emacs }}
  alternatives.set:
    - name: editor
    - path: /usr/bin/{{ emacs }}

basic-tools:
  pkg.installed:
    - pkgs:
      - iotop
      - htop
      - tmux
      - aptitude
      
# some of this is needed for
# building the nodejs package
devpackages:
  pkg.installed:
    - pkgs:
      - git-core
      - devscripts
      - cdbs
      - pkg-config
      - curl
      - zlib1g-dev
      - rubygems
      - ruby-dev

      # python packages
      - python-dev
      - python-requests
      - virtualenvwrapper
      - libpq-dev
      - libpng12-dev
      - libfreetype6-dev
      - libxml2-dev
      - libxslt1-dev
      - libssl-dev
      - libjpeg-dev
      - liblcms2-dev
      
