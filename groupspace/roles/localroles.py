from borg.localrole.interfaces import ILocalRoleProvider
from Products.GrufSpaces.interface import IGroupSpace
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
    adapts(IGroupSpace)

    def __init__(self, context):
        self.context = context

    def getAllRoles(self):
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
        if not self.context.user_roles is None:
            if principal_id in self.context.user_roles.keys():
                for role in self.context.user_roles[principal_id]:
                    roles.add(role)
        if not self.context.group_roles is None:
            if principal_id in self.context.group_roles.keys():
                for role in self.context.group_roles[principal_id]:
                    roles.add(role)
        return roles    

