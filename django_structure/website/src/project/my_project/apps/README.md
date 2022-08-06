# this directory place creation your apps 


...
## this directory for core apps the project

# Using model mixins
In object-oriented languages, such as Python, a mixin class can be viewed as an interface
with implemented features. When a model extends a mixin, it implements the interface and
includes all of its fields, attributes, properties, and methods. The mixins in Django models
can be used when you want to reuse the generic functionalities in different models multiple
times. The model mixins in Django are abstract base model classes. We will explore them in
the next few recipes.

# Getting ready
First, you will need to create reusable mixins. A good place to keep your model mixins is in
a myproject.apps.core app. If you create a reusable app that you will share with others,
keep the model mixins in the reusable app itself, possibly in a base.py file.