import unittest

from collective.groupspace.roles.browser.roles import LocalGroupSpacePASRolesChangeEvent

class TestLocalGroupSpacePASRolesChangeEvent(unittest.TestCase):
    def test___init__(self):
        object = None
        old_user_roles = 1
        new_user_roles = 2
        old_group_roles = 3
        new_group_roles = 4
        event = LocalGroupSpacePASRolesChangeEvent(object, 
                                                   old_user_roles, 
                                                   new_user_roles, 
                                                   old_group_roles, 
                                                   new_group_roles)
        self.failUnless(event.old_user_roles == old_user_roles)
        self.failUnless(event.new_user_roles == new_user_roles)
        self.failUnless(event.old_group_roles == old_group_roles)
        self.failUnless(event.new_group_roles == new_group_roles)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestLocalGroupSpacePASRolesChangeEvent))
    return suite
            
if __name__ == '__main__':
    unittest.main()
