import unittest
from base import PloneTestCase
from collective.groupspace.roles.localroles import allowedLocalUsersAndGroups
from collective.groupspace.roles.localroles import LocalRoles
from collective.groupspace.roles.localroles import setPolicyDefaultLocalRoles

class TestAllowedLocalUsersAndGroups(PloneTestCase):

    def test_allowed_local_users_and_groups_1(self):
        """First test for empty list when no roles are set
        """
        class Dummy:
            user_roles = None
            group_roles = None
        obj = Dummy()
        self.assertEqual((), allowedLocalUsersAndGroups(obj)())

    def test_allowed_local_users_and_groups_2(self):
        """Test with one user
        """
        class Dummy:
            user_roles = {'user1':['role1']}
            group_roles = None
        obj = Dummy()
        expected = ('user:user1',)
        self.assertEqual(expected, allowedLocalUsersAndGroups(obj)())

    def test_allowed_local_users_and_groups_3(self):
        """Test with one group
        """
        class Dummy:
            user_roles = None
            group_roles = {'group1':['role1']}
        obj = Dummy()
        expected = ('group:group1',)
        self.assertEqual(expected, allowedLocalUsersAndGroups(obj)())

    def test_allowed_local_users_and_groups_4(self):
        """Test with one user and one group
        """
        class Dummy:
            user_roles = {'user1':['role1']}
            group_roles = {'group1':['role1']}
        obj = Dummy()
        expected = ('user:user1', 'group:group1')
        self.assertEqual(expected, allowedLocalUsersAndGroups(obj)())

    def test_allowed_local_users_and_groups_5(self):
        """Test with multiple users and one groups
        """
        class Dummy:
            user_roles = {'user1':['role1'], 'user2':['role2'], 'user3':['role3']}
            group_roles = {'group1':['role1'], 'group2':['role2']}
        obj = Dummy()
        expected = ['group:group1', 'group:group2', 'user:user1', 'user:user2', 'user:user3']
        result = allowedLocalUsersAndGroups(obj)()
        result = list(result)
        result.sort()
        self.assertEqual(expected, result)

class TestLocalRoles(PloneTestCase):
    def test___init__(self):
        class Dummy:
            pass
        obj = Dummy()
        local_roles = LocalRoles(obj)
        self.failUnless(local_roles.context == obj)        

    def test_getAllRoles(self):
        """
        Expecting an empty tuple when there are no user or group roles 
        attributes.
        """
        class Dummy:
            pass
        obj = Dummy()
        local_roles = LocalRoles(obj)
        self.assertEqual((), tuple(local_roles.getAllRoles()))

    def test_getAllRoles_1(self):
        """
        Expecting an empty tuple when the user or group roles attributes
        are None
        """
        class Dummy:
            user_roles = None
            group_roles = None
        obj = Dummy()
        local_roles = LocalRoles(obj)
        self.assertEqual((), tuple(local_roles.getAllRoles()))

    def test_getAllRoles_2(self):
        """
        Expecting an empty tuple when the user or group roles attributes
        are dictionaries.
        """
        class Dummy:
            user_roles = {}
            group_roles = {}
        obj = Dummy()
        local_roles = LocalRoles(obj)
        self.assertEqual((), tuple(local_roles.getAllRoles()))

    def test_getAllRoles_3(self):
        """
        Expecting a list of tuples with users and groups and their respective
        roles.
        """
        class Dummy:
            user_roles = {'user1':['role1'], 'user2':['role2'], 'user3':['role3']}
            group_roles = {'group1':['role1'], 'group2':['role2']}
        obj = Dummy()
        local_roles = LocalRoles(obj)
        result = list(local_roles.getAllRoles())
        result.sort()
        expected = [('user2', 'role2'), ('user3', 'role3'), ('user1', 'role1'), 
                    ('group1', 'role1'), ('group2', 'role2')]
        expected.sort()
        self.assertEqual(expected, result)

    def test_getRoles_1(self):
        """
        Expecting an empty list when no user or group roles attributes exist
        """
        class Dummy:
            pass
        obj = Dummy()
        local_roles = LocalRoles(obj)
        self.assertEqual([], local_roles.getRoles('dummy'))

    def test_getRoles_2(self):
        """
        Expecting an empty list when the user and group roles attributes are
        None.
        """
        class Dummy:
            user_roles = None
            group_roles = None
        obj = Dummy()
        local_roles = LocalRoles(obj)
        self.assertEqual([], local_roles.getRoles('dummy'))

    def test_getRoles_3(self):
        """
        Expecting an empty list when the user and group roles attributes are
        empty dictionaries.
        """
        class Dummy:
            user_roles = {}
            group_roles = {}
        obj = Dummy()
        local_roles = LocalRoles(obj)
        self.assertEqual([], local_roles.getRoles('dummy'))

    def test_getRoles_4(self):
        """
        Expecting the list of roles when a user has roles assigned.
        """
        class Dummy:
            user_roles = {'user1':['role1'],}
            group_roles = None
        obj = Dummy()
        local_roles = LocalRoles(obj)
        self.assertEqual(['role1'], local_roles.getRoles('user1'))

    def test_getRoles_5(self):
        """
        Expecting the list of roles when a group has roles assigned.
        """
        class Dummy:
            user_roles = None
            group_roles = {'group1':['role1', 'role2']}
        obj = Dummy()
        local_roles = LocalRoles(obj)
        self.assertEqual(['role1', 'role2'], local_roles.getRoles('group1'))

class TestSetPolicyDefaultLocalRoles(PloneTestCase):
        
    def setUp(self):
        unittest.TestCase.setUp(self)

        class Dummy:
            reindexed = False
            del_roles = []
            set_roles = []
            def manage_delLocalRoles(self, userids):
                self.del_roles = userids
            def manage_setLocalRoles(self, userid, roles):
                self.set_roles.append( (userid, roles) )
            def reindexObjectSecurity(self):
                self.reindexed = True
        self.obj = Dummy()

        class DummyEvent:
            old_user_roles = {}
            new_user_roles = {}
            old_group_roles = {}
            new_group_roles = {}
        self.event = DummyEvent()
        
    def test_set_policy_default_local_roles_1(self):
        """
        When the event has no changes, nothing is reindexed, and no roles
        are deleted or set.
        """
        setPolicyDefaultLocalRoles(self.obj, self.event)
        self.failUnless(self.obj.reindexed == False)
        self.failUnless(self.obj.del_roles == [])
        self.failUnless(self.obj.set_roles == [])

    def test_set_policy_default_local_roles_2(self):
        """
        When the event has new roles for a user without previous roles, user
        becomes GroupReader and the object is reindexed.
        """
        self.event.new_user_roles = {'user1':['role1', 'role2']}
        setPolicyDefaultLocalRoles(self.obj, self.event)
        self.failUnless(self.obj.reindexed == True)
        self.failUnless(self.obj.del_roles == [])
        expected = [('user1', ['GroupReader'])]
        self.failUnless(self.obj.set_roles == expected)

    def test_set_policy_default_local_roles_3(self):
        """
        When the event has new roles for a user with previous roles, the user
        becomes GroupReader again, and the object is reindexed. 
        """
        self.event.old_user_roles = {'user1':['role1']}
        self.event.new_user_roles = {'user1':['role1', 'role2']}
        setPolicyDefaultLocalRoles(self.obj, self.event)
        self.failUnless(self.obj.reindexed == True)
        self.failUnless(self.obj.del_roles == [])
        expected = [('user1', ['GroupReader'])]
        self.failUnless(self.obj.set_roles == expected)

    def test_set_policy_default_local_roles_4(self):
        """
        When the event has old roles for a user, but no current roles, the roles
        for the user get removed, and the object reindexed.
        """
        self.event.old_user_roles = {'user1':['role1', 'role2']}
        self.event.new_user_roles = {} 
        setPolicyDefaultLocalRoles(self.obj, self.event)
        self.failUnless(self.obj.reindexed == True)
        self.failUnless(self.obj.del_roles == ['user1'])
        self.failUnless(self.obj.set_roles == [])

    def test_set_policy_default_local_roles_5(self):
        """
        When the event has new roles for a group without previous roles, the
        group becomes GroupReader and the object is reindexed.
        """
        self.event.new_group_roles = {'group1':['role1', 'role2']}
        setPolicyDefaultLocalRoles(self.obj, self.event)
        self.failUnless(self.obj.reindexed == True)
        self.failUnless(self.obj.del_roles == [])
        expected = [('group1', ['GroupReader'])]
        self.failUnless(self.obj.set_roles == expected)

    def test_set_policy_default_local_roles_6(self):
        """
        When the event has new roles for a group with previous roles, the group
        becomes GroupReader again, and the object is reindexed. 
        """
        self.event.old_group_roles = {'group1':['role1']}
        self.event.new_group_roles = {'group1':['role1', 'role2']}
        setPolicyDefaultLocalRoles(self.obj, self.event)
        self.failUnless(self.obj.reindexed == True)
        self.failUnless(self.obj.del_roles == [])
        expected = [('group1', ['GroupReader'])]
        self.failUnless(self.obj.set_roles == expected)

    def test_set_policy_default_local_roles_7(self):
        """
        When the event has old roles for a group, but no current roles, the roles
        for the group get removed, and the object reindexed.
        """
        self.event.old_group_roles = {'group1':['role1', 'role2']}
        self.event.new_group_roles = {} 
        setPolicyDefaultLocalRoles(self.obj, self.event)
        self.failUnless(self.obj.reindexed == True)
        self.failUnless(self.obj.del_roles == ['group1'])
        self.failUnless(self.obj.set_roles == [])
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestAllowedLocalUsersAndGroups))
    suite.addTest(makeSuite(TestLocalRoles))
    suite.addTest(makeSuite(TestSetPolicyDefaultLocalRoles))
    return suite
    
if __name__ == '__main__':
    unittest.main()
