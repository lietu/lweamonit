lweamonit:
    group.present:
        - system: False
    user.present:
        - fullname: lweamonit system
        - shell: /bin/bash
        - home: /home/lweamonit
        - groups:
            - lweamonit

/home/lweamonit/:
    file.directory:
        - user: lweamonit
        - group: lweamonit
        - mode: 750
        - makedirs: True

/home/lweamonit/.bashrc:
    file.managed:
        - source: salt://basic/bashrc
        - user: lweamonit
        - group: lweamonit
        - mode: 700

# Generic tools we'll want on the machine
{% for pkg in 'wget', 'subversion' %}
{{ pkg }}:
    pkg.installed
{% endfor %}
