Introduction
============

Implements a roles tab for any content type implementing the ILocalGroupSpacePASRoles
interface. An example content type is contained in collective.groupspace.content.

The tab looks exactly like the Plone sharing tab, but local roles for users and 
groups are stored in two attributes on the content type. The local roles can then 
be assigned in the context of a GroupSpace, and are dynamically added to the roles
of a visiting user with borg.localrole.

collective.groupspace.roles Installation
----------------------------------------

To install collective.groupspace.roles into the global Python environment (or a workingenv),
using a traditional Zope 2 instance, you can do this:

* When you're reading this you have probably already run 
  ``easy_install collective.groupspace.roles``. Find out how to install setuptools
  (and EasyInstall) here:
  http://peak.telecommunity.com/DevCenter/EasyInstall

* Create a file called ``collective.groupspace.roles-configure.zcml`` in the
  ``/path/to/instance/etc/package-includes`` directory.  The file
  should only contain this::

    <include package="collective.groupspace.roles" />


Alternatively, if you are using zc.buildout and the plone.recipe.zope2instance
recipe to manage your project, you can do this:

* Add ``collective.groupspace.roles`` to the list of eggs to install, e.g.:

    [buildout]
    ...
    eggs =
        ...
        collective.groupspace.roles
       
* Tell the plone.recipe.zope2instance recipe to install a ZCML slug:

    [instance]
    recipe = plone.recipe.zope2instance
    ...
    zcml =
        collective.groupspace.roles

* Tell Plone where to find the package:

    develop =
        ...
        src/collective.groupspace.roles

* Make a checkout of ``collective.groupspace.roles`` to the src folder:

    $ cd src
    $ svn co https://svn.plone.org/svn/collective/collective.groupspace.roles/trunk collective.groupspaces.roles
      
* Re-run buildout, e.g. with:

    $ ./bin/buildout
        
You can skip the ZCML slug if you are going to explicitly include the package
from another package's configure.zcml file.
