# Installation

Create a dir where you want to store your fragments, then add `FRAGMENTS_DIR` to your `settings.py`, it must be an absolute path.

Then add something like this to your `urls.py`

    url(r'^', include('fragments.urls')),

And somewhere in your base template

    <script type="text/javascript" src="{% url fragments %}">
