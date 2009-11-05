"""Base class for integration tests, based on ZopeTestCase and PloneTestCase.

Note that importing this module has various side-effects: it registers a set of
products with Zope, and it sets up a sandbox Plone site with the appropriate
products installed.
"""

from Testing import ZopeTestCase

# Import PloneTestCase - this registers more products with Zope as a side effect
from Products.PloneTestCase.PloneTestCase import PloneTestCase
from Products.PloneTestCase.PloneTestCase import FunctionalTestCase
from Products.PloneTestCase.PloneTestCase import setupPloneSite
from DateTime import DateTime

from zope.interface import alsoProvides
from collective.groupspace.roles.interfaces import ILocalGroupSpacePASRoles
from Globals import PersistentMapping

from zope.interface import implements
from collective.groupspace.roles.interfaces import IRolesPageRole
from plone.app.workflow import PloneMessageFactory as _

# Set up a Plone site - note that the portlets branch of CMFPlone applies
# a portlets profile.
setupPloneSite()

class WorkflowTestCase(PloneTestCase):
    """Base class for integration tests for plone.app.workflow. This may
    provide specific set-up and tear-down operations, or provide convenience
    methods.
    """
    
class ManagerRole(object):
    implements(IRolesPageRole)    
    title = _(u"title_can_manage", default=u"Can manage")
    required_permission = "Change local roles"        
    
class WorkflowFunctionalTestCase(FunctionalTestCase):
    """Base class for functional integration tests for plone.app.workflow. 
    This may provide specific set-up and tear-down operations, or provide 
    convenience methods.
    """

    def afterSetUp(self):

        self.portal.acl_users._doAddUser('manager', 'secret', ['Manager',],[])
        self.portal.acl_users._doAddUser('member', 'secret', ['Member',],[])
        self.portal.acl_users._doAddUser('owner', 'secret', ['Owner',],[])
        self.portal.acl_users._doAddUser('reviewer', 'secret', ['Reviewer',],[])
        self.portal.acl_users._doAddUser('editor', 'secret', ['Editor',],[])
        self.portal.acl_users._doAddUser('reader', 'secret', ['Reader',],[])
        
        self.portal.acl_users._doAddUser('groupadmin', 'secret', ['Member',],[])
        self.portal.acl_users._doAddUser('groupeditor', 'secret', ['Member',],[])
        self.portal.acl_users._doAddUser('groupcontributor', 'secret', ['Member',],[])
        self.portal.acl_users._doAddUser('groupreader', 'secret', ['Member',],[]) 

        self.workflow = self.portal.portal_workflow
        self.workflow.setChainForPortalTypes(('Document',),('one_state_workflow',))    
        self.workflow.setChainForPortalTypes(('Folder',),('one_state_workflow',))    
        self.workflow.setChainForPortalTypes(('News Item',),('one_state_workflow',))    
        self.workflow.setChainForPortalTypes(('Event',),('one_state_workflow',))    
        
        self.setRoles(('Manager',))

        self.portal.invokeFactory('Folder', 'folder')
        self.folder = self.portal.folder
        
        # Make the folder provide the IGroupSpace interface
        self.folder.user_roles = PersistentMapping()
        self.folder.group_roles = PersistentMapping()
        alsoProvides(self.folder, ILocalGroupSpacePASRoles)
        self.folder.reindexObject()
        
        self.folder.invokeFactory('News Item', 'newsitem1')
        self.newsitem = self.folder.newsitem1
        self.folder.invokeFactory('Event', 'event1')
        self.event = self.folder.event1
        self.folder.invokeFactory('Document', 'document1')
        self.document = self.folder.document1
        self.setRoles(('Member',))

        # Provide a role for the roles page
        sm = self.portal.getSiteManager()
        if not sm.queryUtility(IRolesPageRole, name='Manager'):
            sm.registerUtility(ManagerRole(),
                       IRolesPageRole,
                       'Manager')
