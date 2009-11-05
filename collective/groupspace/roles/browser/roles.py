from itertools import chain

from zope.component import getUtilitiesFor
from zope.component import getMultiAdapter

import zope.interface
from zope.event import notify

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Acquisition import aq_inner
from zExceptions import Forbidden

from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage

from plone.app.vocabularies.users import UsersSource
from plone.app.vocabularies.groups import GroupsSource

from plone.memoize.instance import memoize
from plone.memoize.instance import clearafter

from plone.app.workflow import PloneMessageFactory as _
from plone.app.workflow.browser.sharing import SharingView
from collective.groupspace.roles.interfaces import IRolesPageRole

from Globals import PersistentMapping

from zope.component.interfaces import ObjectEvent
from zope.app.container.interfaces import IObjectMovedEvent

from collective.groupspace.roles.interfaces import ILocalGroupSpacePASRolesChangeEvent

class LocalGroupSpacePASRolesChangeEvent(ObjectEvent):
    """
    Local roles for a GroupSpace are changing
    """
    zope.interface.implements(ILocalGroupSpacePASRolesChangeEvent)

    def __init__(self, object, old_user_roles, new_user_roles, old_group_roles, 
                 new_group_roles):
        ObjectEvent.__init__(self, object)
        self.old_user_roles = old_user_roles
        self.new_user_roles = new_user_roles
        self.old_group_roles = old_group_roles
        self.new_group_roles = new_group_roles
        
class RolesView(SharingView):
    """
    The sharing view already does the heavy lifting of searching users and
    groups, so we just tap into the existing implementation.
    
    Reindexing the security is not necessary in the case of this roles tab,
    so we return False in the update_inherit and update_role_settings methods.
    """
    
    template = ViewPageTemplateFile('groupspace_roles.pt')
    
    def update_inherit(self, status=True, reindex=True):
        """
        Not used in the roles form
        """
        return False # Such as to not reindex the security

    # View    
    @memoize
    def roles(self):
        """Get a list of roles that can be managed.
        
        Returns a list of dicts with keys:
        
            - id
            - title
        """
        context = aq_inner(self.context)
        portal_membership = getToolByName(context, 'portal_membership')
        
        pairs = []
        
        for name, utility in getUtilitiesFor(IRolesPageRole):
            permission = utility.required_permission
            if permission is None or portal_membership.checkPermission(permission, context):
                pairs.append(dict(id = name, title = utility.title))
                
        pairs.sort(key=lambda x: x["id"])
        return pairs

        
    # helper functions
    
    @memoize
    def existing_role_settings(self):
        """Get current settings for users and groups that have already got
        at least one of the managed roles.

        Returns a list of dicts as per role_settings()
        """
        context = aq_inner(self.context)
        
        # Compile a list of user and group information with their roles
        info = []
 
        # Only accept known roles in the result list
        knownroles = self.roles()
                      
        if context.user_roles:
            userssource = UsersSource(context)
            for user_id, user_roles in context.user_roles.items():
                # Fetch the user and compile the existing role settings
                user = userssource.get(user_id)
                if user is None:
                    continue
                roles = {}
                for role in knownroles:
                    # Only return information on any known roles
                    if role['id'] in user_roles:
                        roles[role['id']] = True
                    else:
                        roles[role['id']] = False
                if roles:
                    # Only add the user info if he has any role
                    info.append({'type': 'user',
                                 'id': user_id,
                                 'title': user.getProperty('fullname', None) or user.getId(),
                                 'roles': roles,
                            })

        if context.group_roles:
            groupssource = GroupsSource(context)
            for group_id, group_roles in context.group_roles.items():
                # Fetch the group and compile the existing role settings
                group = groupssource.get(group_id)
                if group is None:
                    continue
                roles = {}
                for role in knownroles:
                    # Only return information on any known roles
                    if role['id'] in group_roles:
                        roles[role['id']] = True
                    else:
                        roles[role['id']] = False
                if roles:
                    # Only add the group info if it has any role
                    info.append({'type': 'group',
                                 'id': group_id,
                                 'title': group.getProperty('title', None) or group.getId(),
                                 'roles': roles,
                                })

        return info
                            
    @clearafter
    def update_role_settings(self, new_settings, reindex=False):
        """Update the role settings.
        
        new_settings is a list of dicts with keys id, for the user/group id;
        type, being either 'user' or 'group'; and roles, containing the list
        of role ids that are set.
        """
        context = aq_inner(self.context)            

        # Collect all roles for users and groups according to the new settings
        user_roles = {}
        group_roles = {}

        # Make sure to only set roles that are known
        knownroles = self.roles()
                        
        for principal in new_settings:
            roles = []
            for role in knownroles:
                # Only set whatever roles are known
                if role['id'] in principal['roles']:
                    # Only set whatever toles are set
                    roles.append(role['id'])
            if roles:
                # No need to store an empty list of roles
                if principal['type'] == 'user':
                    # The roles for this user will be stored
                    user_roles[principal['id']]=roles
                elif principal['type'] == 'group':
                    # The roles for this user will be stored
                    group_roles[principal['id']]=roles

        # Store changes for LocalGroupSpacePASRolesChangeEvent
        old_user_roles = {}
        new_user_roles = {}
        old_group_roles = {}
        new_group_roles = {}

        # Take care to only set any values if something has really changed
        if context.user_roles != user_roles:
            if context.user_roles is None:
                # Now is the time to make this a persistent mapping
                context.user_roles = PersistentMapping()

            # Keep track of the changes for LocalGroupSpacePASRolesChangeEvent
            old_user_roles = context.user_roles.copy()
            new_user_roles = user_roles.copy()
            
            # Instead of going through the changes individually, just set them
            context.user_roles.clear()
            context.user_roles.update(user_roles)
        
        # Take care to only set any values if something has really changed
        if context.group_roles != group_roles:
            if context.group_roles is None:
                # Now is the time to make this a persistent mapping
                context.group_roles = PersistentMapping()

            # Keep track of the changes for LocalGroupSpacePASRolesChangeEvent
            old_group_roles = context.group_roles.copy()
            new_group_roles = group_roles.copy()

            # Instead of going through the changes individually, just set them
            context.group_roles.clear()
            context.group_roles.update(group_roles)

        # The user can decide whether to send the notifications or not
        if old_user_roles or new_user_roles or old_group_roles or new_group_roles:
            # In case there are some changes, trigger the event
            event = LocalGroupSpacePASRolesChangeEvent(self.context,
                                                       old_user_roles, 
                                                       new_user_roles, 
                                                       old_group_roles, 
                                                       new_group_roles)
            notify(event)
        
        # Just reindex allowedLocalUsersAndGroups
        context.reindexObject(idxs=['allowedLocalUsersAndGroups'])
        
        return False # Such as to not reindex the security


