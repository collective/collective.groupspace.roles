"""
Local roles for PAS
"""

from borg.localrole.interfaces import ILocalRoleProvider
from zope.interface import implements
from zope.component import adapts
from collective.groupspace.roles.interfaces import IRolesPageRole
from collective.groupspace.roles.config import ROLE_ASSIGNMENT_PERMISSION
from plone.app.workflow import PloneMessageFactory as _
from plone.indexer.decorator import indexer
from collective.groupspace.roles.interfaces import ILocalGroupSpacePASRoles

@indexer(ILocalGroupSpacePASRoles)
def allowedLocalUsersAndGroups(obj):
    """
    A catalog index similar to allowedRolesAndUsers, but for local roles
    of users and groups only.

    The ILocalGroupSpacePASRoles must be implemented by the objects, so
    the user_roles and group_roles attributes must be present.
    
    The actual roles assigned to the users are not checked, and it is 
    assumed that any user that has any role will be allowed.
    
    This method returns a tuple of the form:
    
    ('user:sampleuser1', 'user:sampleuser2', 'group:samplegroup1'}
    """
    result = []
    if not obj.user_roles is None:
        for user_id in obj.user_roles.keys():
            result.append('user:%s' % user_id)            
    if not obj.group_roles is None:
        for group_id in obj.group_roles.keys():
            result.append('group:%s' % group_id)            
    return tuple(result)

class GroupAdminRole(object):
    """Admin role for groupspaces"""
    implements(IRolesPageRole)
    
    title = _(u"title_can_manage", default=u"Can manage")
    required_permission = ROLE_ASSIGNMENT_PERMISSION
    
class GroupEditorRole(object):
    """Editor role for groupspaces"""
    implements(IRolesPageRole)
    
    title = _(u"title_can_edit", default=u"Can edit")
    required_permission = ROLE_ASSIGNMENT_PERMISSION
    
class GroupContributorRole(object):
    """Contributor role for groupspaces"""
    implements(IRolesPageRole)
    
    title = _(u"title_can_add", default=u"Can add")
    required_permission = ROLE_ASSIGNMENT_PERMISSION
    

class GroupReaderRole(object):
    """Reader role for groupspaces"""
    implements(IRolesPageRole)
    
    title = _(u"title_can_view", default=u"Can view")
    required_permission = ROLE_ASSIGNMENT_PERMISSION

class LocalRoles(object):
    """Provide a local role manager for group spaces that allows querying the
       local roles on an object.
    """
    implements(ILocalRoleProvider)
    adapts(ILocalGroupSpacePASRoles)

    def __init__(self, context):
        self.context = context

    def getAllRoles(self):
        """Returns an iterable consisting of tuples of the form:
           (principal_id, sequence_of_roles)
        """
        try:
            self.context.user_roles
            self.context.group_roles
        except AttributeError:
            return
        if not self.context.user_roles is None:
            for user_id, user_roles in self.context.user_roles.items():
                for role in user_roles:
                    yield (user_id, role)
        if not self.context.group_roles is None:
            for group_id, group_roles in self.context.group_roles.items():
                for role in group_roles:
                    yield (group_id, role)

    def getRoles(self, principal_id):            
        """Returns an iterable of roles granted to the specified user object
        """
        roles = set()
        try:
            self.context.user_roles
            self.context.group_roles
        except AttributeError:
            return list(roles)        
        if not self.context.user_roles is None:
            if principal_id in self.context.user_roles.keys():
                for role in self.context.user_roles[principal_id]:
                    roles.add(role)
        if not self.context.group_roles is None:
            if principal_id in self.context.group_roles.keys():
                for role in self.context.group_roles[principal_id]:
                    roles.add(role)
        return list(roles)    

def setPolicyDefaultLocalRoles(obj, event):
    """
    Some local workflow policies only work when certain local roles are 
    given by default. A common case is that the search only works when 
    at least one local role is present that gives the View permission.
    """
    # Just one role is needed to give the View permission
    # GroupReader is the minimal role needed, so use this
    default_roles = ["GroupReader", ]

    remove, add = _local_roles_to_remove_and_add(event)

    if remove:
        # Delete all local roles for the principals
        obj.manage_delLocalRoles(userids=remove)

    for principal in add:
        # Enforce just the default local roles
        obj.manage_setLocalRoles(principal, list(default_roles))

    if remove or add:
        # Now that the local roles have changed, it is necessary to reindex
        # the security
        obj.reindexObjectSecurity()


def _local_roles_to_remove_and_add(event):

    # Unite user ids
    users = set(event.old_user_roles.keys())
    users.update(set(event.new_user_roles.keys()))

    # Unite group ids
    groups = set(event.old_group_roles.keys())
    groups.update(set(event.new_group_roles.keys()))

    remove = []
    add = []    
    for user in users:
        if not event.new_user_roles.has_key(user):
            # The user has all his roles removed, so add it to the list
            remove.append(user)
        else:
            # The user just has his roles changed
            add.append(user)

    for group in groups:
        if not event.new_group_roles.has_key(group):
            # The group has all its roles removed, so add it to the list
            remove.append(group)
        else:
            # The group just has its roles changed
            add.append(group)
    return remove, add
