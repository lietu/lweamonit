ntpdate:
    pkg.installed

ntpd:
    pkg.installed:
        - name: ntp
    service.running:
        - name: ntp
        - enable: True
        - require:
            - pkg: ntp
