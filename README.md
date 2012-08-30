# Introduction

Objectif: to be used with a javascript mvc client-side framework.

# Installation

Create a dir where you want to store your fragments, then add `FRAGMENTS_DIR` to your `settings.py`, it must be an absolute path.

Write some small html snippets in this dir.

Then add something like this to your `urls.py`

    url(r'^', include('fragments.urls')),

And somewhere in your base template

    <script type="text/javascript" src="{% url fragments %}">

This will give you a javascript object `fragments` that is a object that contains all your fragments, the key is the filename of the fragment without the extention.

Exemple: `object_list.html` will be accessible in the `fragments` object like this: `fragments.object_list`

# Verbatim tag

**You have to put `fragments` in you installed apps in settings.py for this to work**.

I've extracted code from the dev branch of django 1.5 to allow the use of the
[verbatim](https://docs.djangoproject.com/en/dev/ref/templates/builtins/#verbatim)
templatetags to avoid conflicts between django template syntaxe and other
template engine syntaxe (eg: mustache).

Example:

    {% load fragments %}

    {{ will_be_interpreted }}
    {% verbatim %}
    {{ wont_be_interpredted }}
    {% endverbatim %}

You can also designate a specifif closing tag like describe in django doc.

Example from the doc:

    {% load fragments %}

    {% verbatim myblock %}
        Avoid template rendering via the {% verbatim %}{% endverbatim %} block.
    {% endverbatim myblock %}

# Ignored files extensions

By default `django-template-fragments` ignores every files that ends with one of those: `.pyc` `.swo` `.swp` `~`

You can specify your own list by defining `FRAGMENTS_IGNORED_FILE_TYPES` in you `settings.py`.
