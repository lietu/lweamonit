{% for pkg in 'virtualenv', 'virtualenvwrapper' %}
{{ pkg }}:
    pip.installed:
        - require:
            - pkg: python-pip
{% endfor %}

/home/lweamonit/.virtualenvs:
  file.directory:
      - user: lweamonit
      - group: lweamonit
      - dir_mode: 00755
      - file_mode: 00644
