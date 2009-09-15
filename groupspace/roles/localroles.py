from borg.localrole.interfaces import ILocalRoleProvider
from Products.GrufSpaces.interface import IGroupSpace
from zope.interface import implements
from zope.component import adapts

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

