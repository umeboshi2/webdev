# -*- mode: yaml -*-
{% set pget = salt['pillar.get'] %}

include:
  - default

{% if salt['grains.get']('oscodename') == 'wheezy' %}
node-debian-git-repo:
  git.latest:
    - name: https://github.com/mark-webster/node-debian
    - target: /srv/node-debian

node-debian-build-repo:
  git.latest:
    - require:
      - git: node-debian-git-repo
    - name: /srv/node-debian
    - target: /var/tmp/make-nodejs/node-debian




build-nodejs-package:
  cmd.script:
    - require:
      - sls: default
      - git: node-debian-build-repo
    - unless: test -x /usr/bin/npm
    - source: salt://files/build-nodejs.sh
    - env:
      - NODE_VERSION: {{ pget('node_version') }}
      # YAML inconsistency.  Should these be recast to strings in salt?
      - DEBIAN_CONCURRENCY: "3"

nodejs:
  pkg.installed:
    - require:
      - cmd: build-nodejs-package
{% else %}
nodejs:
  pkg.installed:
    - pkgs:
      - nodejs-legacy
      - npm
{% endif %}

npm-webdev-packages:
  npm.installed:
    - require:
      - pkg: nodejs
    - pkgs:
      - coffee-script
      - grunt-cli
      - bower
      - http-server
      - js2coffee
      - express
