from zope.interface import Interface
from zope.interface import Attribute
from zope.component.interfaces import IObjectEvent

class ILocalGroupSpacePASRoles(Interface):
    """
    ILocalGroupSpacePASRoles interface

    The user and group roles are handled by the roles view, which will set a
    PersistentMapping on any instances. Local roles are then dynamically
    assigned through the PAS plugin.
    """
    user_roles = Attribute("User Roles")
    group_roles = Attribute("Group Roles")

class ILocalGroupSpacePASRolesChangeEvent(IObjectEvent):
    """
    An event signalling that the local roles are changing.   
    """
    old_user_roles = Attribute("The old user roles for the object.")
    new_user_roles = Attribute("The new user roles for the object.")
    old_group_roles = Attribute("The old group roles for the object.")
    new_group_roles = Attribute("The new group roles for the object.")