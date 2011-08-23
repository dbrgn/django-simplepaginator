django-simplepaginator
======================

django-simplepaginator is a small wrapper around the standard Django paginator. It simplifies the
creation of a paginator and provides templates for column titles and page navigation. It supports
sorting and orphans.

Most of the display logic is done inside the templates. That's why those templates are pretty ugly,
sorry about that...

Install
-------

Copy the messagegroups folder to your project or install it into your pythonpath:

    # python setup.py install

Then add messagegroups to your `INSTALLED_APPS` setting.

Usage
-----

The SimplePaginator object accepts the following keyword arguments:

* `request` -- The request object
* `prefix` -- The prefix for the controls' css-class and for the GET parameters
* `data` -- Elements to paginate
* `columns` -- A tuple of tuples containing column name and key (default None)
* `per_page` -- How many elements to display per page (default 20)
* `orphans` -- Whether to move orphans to the previous page (default 1)

In the view, use the `paginate()`-shortcutfunction to return pagination items. Remember that each
pagination on a page must have a distinct prefix.

### Example:

```python
from django.shortcuts import render_to_response
import simple_paginator

try:
    objects = models.Example.objects.filter(id__lte=100)
except ObjectDoesNotExist:
    objects = None

prefix = 'itemlist'
columns = (
    ('Column1', 'modelfield1'),
    ('Column2', 'modelfield2'),
    ('Column3', 'modelfield3'),
)
items, order = simple_paginator.paginate(request, prefix, functions, columns)

context = {
    'items': items,
    'prefix': prefix,
    'columns': columns,
    'order': order
}
return render_to_response('template.html', context)
```

And in the template:

```html
<h1>Pagination demo</h1>
<p>This pagination shows all Example objects with an id <= 100.</p>

<div class="simple_paginator">
    <table>
        {% include 'simple_paginator/paginator_header.html' %}
            {% for item in items.object_list %}
                <tr class="{% cycle 'odd' 'even' %}">
                    <td>{{ item.modelfield1 }}</td>
                    <td>{{ item.modelfield2 }}</td>
                    <td>{{ item.modelfield3 }}</td>
                </tr>
            {% endfor %}
    </table>

    {% include 'simple_paginator/paginator_control.html' %}
</div>
```

If the column feature is not used, some parts can be omitted:

```html
<h1>Pagination demo</h1>
<p>This pagination lists some items.</p>

<div class="simple_paginator">
    {% for item in items.object_list %}
        <div class="item">{{ item }}</div>
    {% endfor %}

    {% include 'simple_paginator/paginator_control.html' %}
</div>
```

Customize
---------

You can customize the paginator header and control templates by copying them to your project
folder and editing them, or by adding completely new templates. They should be put in a
directory called "simple_paginator" inside your template folder.

License
-------

Copyright 2011 Factor AG (http://factor.ch/)

This program is free software: you can redistribute it and/or modify it under the terms of the GNU
Lesser General Public License as published by the Free Software Foundation, either version 3 of the
License, or any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser
General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with this program.
If not, see http://www.gnu.org/licenses/lgpl.html.
