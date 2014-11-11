{% for pkg in 'python-setuptools', 'python-dev', 'python-pip' %}
{{ pkg }}:
    pkg.installed
{% endfor %}
