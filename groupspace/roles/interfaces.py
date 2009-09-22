from zope.interface import Interface
from zope.interface import Attribute

class ILocalGroupSpacePASRoles(Interface):
    """
    ILocalGroupSpacePASRoles interface

    The user and group roles are handled by the roles view, which will set a
    PersistentMapping on any instances. Local roles are then dynamically
    assigned through the PAS plugin.
    """
    user_roles = Attribute("User Roles")
    group_roles = Attribute("Group Roles")
