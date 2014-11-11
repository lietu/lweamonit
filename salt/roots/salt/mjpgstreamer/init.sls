{% for pkg in 'libv4l-dev', 'libjpeg62', 'libjpeg62-dev' %}
{{ pkg }}:
    pkg.installed
{% endfor %}

/root/install_mjpgstreamer.sh:
    file.managed:
        - source: salt://mjpgstreamer/install.sh
        - mode: 700
    cmd.run:
        - stateful: True
        - require:
            - pkg: wget
