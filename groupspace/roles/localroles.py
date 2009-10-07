from borg.localrole.interfaces import ILocalRoleProvider
from zope.interface import implements
from zope.component import adapts
from Products.GrufSpaces.interface import IRolesPageRole
from Products.GrufSpaces.permissions import AssignGroupSpaceRoles
from plone.app.workflow import PloneMessageFactory as _
from plone.indexer.decorator import indexer
from groupspace.roles.interfaces import ILocalGroupSpacePASRoles

@indexer(ILocalGroupSpacePASRoles)
def allowedLocalUsersAndGroups(object):
    result = []
    if not object.user_roles is None:
        for user_id in object.user_roles.keys():
            result.append('user:%s' % user_id)            
    if not object.group_roles is None:
        for group_id in object.group_roles.keys():
            result.append('group:%s' % group_id)            
    return tuple(result)

class GroupAdminRole(object):
    implements(IRolesPageRole)
    
    title = _(u"title_can_manage", default=u"Can manage")
    required_permission = AssignGroupSpaceRoles
    
class GroupEditorRole(object):
    implements(IRolesPageRole)
    
    title = _(u"title_can_edit", default=u"Can edit")
    required_permission = AssignGroupSpaceRoles
    
class GroupContributorRole(object):
    implements(IRolesPageRole)
    
    title = _(u"title_can_edit", default=u"Can add")
    required_permission = AssignGroupSpaceRoles
    

class GroupReaderRole(object):
    implements(IRolesPageRole)
    
    title = _(u"title_can_view", default=u"Can view")
    required_permission = AssignGroupSpaceRoles

class LocalRoles(object):
    """Provide a local role manager for group spaces
    """
    implements(ILocalRoleProvider)
    adapts(ILocalGroupSpacePASRoles)

    def __init__(self, context):
        self.context = context

    def getAllRoles(self):
        try:
            self.context.user_roles
            self.context.group_roles
        except:
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
        roles = set()
        try:
            self.context.user_roles
            self.context.group_roles
        except:
            return roles        
        if not self.context.user_roles is None:
            if principal_id in self.context.user_roles.keys():
                for role in self.context.user_roles[principal_id]:
                    roles.add(role)
        if not self.context.group_roles is None:
            if principal_id in self.context.group_roles.keys():
                for role in self.context.group_roles[principal_id]:
                    roles.add(role)
        return roles    

def setPolicyDefaultLocalRoles(object, event):
    """
    Some local workflow policies only work when certain local roles are 
    given by default. A common case is that the search only works when at least
    one local role is present that gives the View permission.
    """
    # Unite user ids
    users = set(event.old_user_roles.keys())
    users.update(set(event.new_user_roles.keys()))
    # Unite group ids
    groups = set(event.old_group_roles.keys())
    groups.update(set(event.new_group_roles.keys()))

    default_roles = ["GroupReader",]

    user_ids_to_clear = []
    for user in users:
        if not event.new_user_roles.has_key(user):
            # The user has all his roles removed, so add it to the list
            user_ids_to_clear.append(user)
        else:                    
            assert(event.new_user_roles[user] != 0)
            # No roles get removed, so enforce the default local roles
            object.manage_setLocalRoles(user, list(default_roles))
            changed = True
    if user_ids_to_clear:
        # Delete all local roles for users
        object.manage_delLocalRoles(userids=user_ids_to_clear)
        changed = True                 

    group_ids_to_clear = []
    for group in groups:
        if not event.new_group_roles.has_key(group):
            # The group has all its roles removed, so add it to the list
            group_ids_to_clear.append(group)
        else:
            assert(event.new_group_roles[group] != 0)
            # No roles get removed, so enforce the default local roles
            object.manage_setLocalRoles(group, list(default_roles))
            changed = True            
    if group_ids_to_clear:
        # Delete all local roles for groups
        object.manage_delLocalRoles(userids=group_ids_to_clear)
        changed = True                 

    if changed:
        # Now that the local roles have changed, it is necessary to reindex
        # the security
        object.reindexObjectSecurity()










