from zope.interface import Interface
from zope.interface import Attribute
from zope import schema
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

class IRolesPageRole(Interface):
    """
    A named utility providing information about roles that are managed by the
    roles page.
    
    Utility names should correspond to the role name.
    
    A user will be able to delegate the given role if a utility can be found
    and the user has the required_permission (or it's None).
    """

    title = schema.TextLine(title=u"A friendly name for the role")

    required_permission = schema.TextLine(
        title=u"Permission required to manage this local role",
        required=False
    )

