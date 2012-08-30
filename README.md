# Introduction

Often, when you use a client-side javascript framework (e.g. backbone/ember/angular/wathever), you'll want small templates to render your page. The problem starts when:
* you still want to be able to use django template engine
* and you want a cool place to define your small templates.

Those are the 2 issues that this django app tries to address. It also comes with helper functionalities for those kind of templates, like the `verbatim` templatetags from django 1.5 dev code that allows you to define a zone where django won't interpret anything to avoid conflicts with template languages like `mustache.js`.

With it, you define all your small templates in the same directory and you'll be able to access them in the `fragments` javascript object that contains the (rendered by django) templates.

# Installation

Create a dir where you want to store your fragments, then add `FRAGMENTS_DIR` to your `settings.py`, it must be an absolute path.

I like to define my `FRAGMENTS_DIR` like this:

    import os
    PROJECT_PATH = os.path.abspath(os.path.split(__file__)[0])
    SUBPROJECT_PATH = os.path.split(PROJECT_PATH)[0]

    FRAGMENTS_DIR = os.path.join(SUBPROJECT_PATH, "fragments")

This will set it to the directory `project_name/fragments` (where your `settings.py` is in `project_name/project_name/settings.py`).

Next, write some small html snippets in this dir.

Then add something like this to your `urls.py`

    url(r'^', include('fragments.urls')),

And somewhere in your base template

    <script type="text/javascript" src="{% url fragments %}" />

This will give you a javascript object `fragments` containing all your fragments, the key is the filename of the fragment without the extension.

Example: `object_list.html` will be accessible in the `fragments` object like this: `fragments.object_list`

If you put the fragment in a subdir in the `FRAGMENTS_DIR`, the key will be the filename without its extension joined with the subdir path where the `/` are replaced by `_`.

Not clear? Here is an example: the file `FRAGMENTS_DIR/one/two/three.html` will be accessible at the key `one_two_three`.

# HamlPy support

If you have [HamlPy](https://github.com/jessemiller/HamlPy) installed and that your fragment name ends with `.haml`, django-template-fragments will take it into account and use HamlPy to generate the html.

# Verbatim tag

**You have to put `fragments` in your installed apps in settings.py for this to work**.

I've taken code from the dev branch of django 1.5 to allow the use of the
[verbatim](https://docs.djangoproject.com/en/dev/ref/templates/builtins/#verbatim)
templatetags to avoid conflicts between django template syntax and other
template engine syntax (e.g. mustache).

Example:

    {% load fragments %}

    {{ will_be_interpreted }}
    {% verbatim %}
    {{ wont_be_interpredted }}
    {% endverbatim %}

You can also choose a specific closing tag as described in django documentation.

Example from the doc:

    {% load fragments %}

    {% verbatim myblock %}
        Avoid template rendering via the {% verbatim %}{% endverbatim %} block.
    {% endverbatim myblock %}

# Ignored files extensions

By default `django-template-fragments` ignores every files that ends with one of those: `.pyc` `.swo` `.swp` `~`

You can specify your own list by defining `FRAGMENTS_IGNORED_FILE_TYPES` in your `settings.py`.
