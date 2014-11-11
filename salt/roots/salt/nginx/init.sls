fonts-dejavu-core:
    pkg.installed

/var/www:
    file.directory:
        - user: www-data
        - group: www-data
        - mode: 755
        - makedirs: True

nginx:
    user.present:
        - name: www-data
        - fullname: www-data
        - shell: /usr/bin/nologin
        - home: /var/www
        - groups:
            - www-data
            - lweamonit
    pkg.installed:
        - require:
            - pkg: fonts-dejavu-core
    service.running:
        - enable: True
        - require:
            - pkg: nginx
        - watch:
            - file: /etc/nginx/nginx.conf

{% for dir in '/etc/nginx/sites-enabled/', '/etc/nginx/sites-available/', '/var/lib/nginx', '/var/lib/nginx/tmp/' %}
{{ dir }}:
    file.directory:
        - user: www-data
        - group: www-data
        - mode: 755
        - makedirs: True
{% endfor %}

{% for path in '/etc/nginx/sites-enabled/default', %}
{{ path }}:
    file.absent
{% endfor %}

/etc/nginx/nginx.conf:
    file.managed:
        - source: salt://nginx/nginx.conf
        - require:
            - pkg: nginx

/etc/nginx/sites-available/images.conf:
    file.managed:
        - source: salt://nginx/images.conf
        - require:
            - pkg: nginx
        - watch_in:
            - service: nginx

/etc/nginx/sites-enabled/images.conf:
    file.symlink:
        - target: /etc/nginx/sites-available/images.conf