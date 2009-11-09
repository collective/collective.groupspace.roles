#
# Test the roles browser view.
#
import unittest

from zope.component import getMultiAdapter
from base import WorkflowTestCase

from zope.interface import alsoProvides
from collective.groupspace.roles.interfaces import ILocalGroupSpacePASRoles
from Globals import PersistentMapping
from collective.groupspace.roles.browser.roles import RolesView

class TestRolesView(WorkflowTestCase):

    def afterSetUp(self):
        self.portal.acl_users._doAddUser('testuser', 'secret', ['Member'], [])
        self.portal.acl_users._doAddUser('nonasciiuser', 'secret', ['Member'], [])
        nonasciiuser = self.portal.portal_membership.getMemberById('nonasciiuser')
        nonasciiuser.setMemberProperties(dict(fullname=u'\xc4\xdc\xdf'.encode('utf-8')))
        self.loginAsPortalOwner()
        self.portal.invokeFactory('Folder', id='folder')
        self.folder = self.portal.folder
        # Make the folder provide the ILocalGroupSpacePASRoles interface
        self.folder.user_roles = PersistentMapping()
        self.folder.group_roles = PersistentMapping()
        user_roles = {'delegate_admin': ['GroupAdmin',],
                      'delegate_editor': ['GroupEditor',],
                      'delegate_contributor': ['GroupContributor',],
                      'delegate_reader': ['GroupReader',],
                      }
        self.folder.user_roles.update(user_roles)
        alsoProvides(self.folder, ILocalGroupSpacePASRoles)
        self.folder.reindexObject()
        
    def test_search_by_login_name(self):
        """Make sure we can search by login name on the Roles tab.
        """
        request = self.app.REQUEST
        request.form['search_term'] = 'testuser'
        view = getMultiAdapter((self.folder, request), name='roles')
        results = view.user_search_results()
        self.failUnless(len(results) and results[0].get('id') == 'testuser', 
                      msg="Didn't find testuser when I searched by login name.")

    def test_search_with_nonascii_users(self):
        """Make sure we can search with users that have non-ascii-chars in their fullname.
        """
        request = self.app.REQUEST
        request.form['search_term'] = 'nonasciiuser'
        view = getMultiAdapter((self.folder, request), name='roles')
        results = view.role_settings()
        self.failUnless(len(results) and results[0].get('title') == '\xc3\x84\xc3\x9c\xc3\x9f', msg="Umlaute")

    def test_existing_role_settings(self):
        context = None
        request = {}
        roles_view = RolesView(self.folder, request)
        self.assertEqual([], roles_view.existing_role_settings())
        
    def test_roles(self):
        context = None
        request = {}
        roles_view = RolesView(self.folder, request)
        expected = [{'id': u'GroupAdmin', 'title': u'title_can_manage'}, 
                    {'id': u'GroupContributor', 'title': u'title_can_edit'}, 
                    {'id': u'GroupEditor', 'title': u'title_can_edit'}, 
                    {'id': u'GroupReader', 'title': u'title_can_view'}]
        self.assertEqual(expected, roles_view.roles())
        
    def test_update_inherit(self):
        context = None
        request = {}
        roles_view = RolesView(self.folder, request)
        status = None
        reindex = False
        self.assertEqual(False, roles_view.update_inherit(status, reindex))
        
    def test_update_role_settings(self):
        context = None
        request = {}
        roles_view = RolesView(self.folder, request)
        new_settings = []
        reindex = False
        self.assertEqual(False, roles_view.update_role_settings(new_settings, reindex))
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestRolesView))
    return suite
if __name__ == '__main__':
    unittest.main()
