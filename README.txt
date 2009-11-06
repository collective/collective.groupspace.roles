Introduction
============

Implements a roles tab for any content type implementing the ILocalGroupSpacePASRoles
interface. An example content type is contained in collective.groupspace.content.

The tab looks exactly like the Plone sharing tab, but local roles for users and 
groups are stored in two attributes on the content type. The local roles can then 
be assigned in the context of a GroupSpace, and are dynamically added to the roles
of a visiting user with borg.localrole.

This package is part of the collective.groupspace suite, whose components should
be installed as needed:

* collective.groupspace.workflow

* collective.groupspace.content

* collective.groupspace.mail

