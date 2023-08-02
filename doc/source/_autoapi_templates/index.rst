API reference
=============

This page contains the ``review-bot`` API reference.

.. toctree::
   :titlesonly:

   {% for page in pages %}
   {% if (page.top_level_object or page.name.split('.') | length == 2) and page.display %}
   {{ page.include_path }}
   {% endif %}
   {% endfor %}
