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
