"""
Common configuration constants for collective.groupspace.roles
"""

from Products.CMFCore.permissions import setDefaultRoles

# Controls access to the "roles" page
ROLE_ASSIGNMENT_PERMISSION = "collective.groupspace.roles: Assign GroupSpace Roles"
setDefaultRoles(ROLE_ASSIGNMENT_PERMISSION, ('Manager', 'Owner', 'GroupAdmin' ))

