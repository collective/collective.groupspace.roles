"""
My groups portlet
"""
from types import StringTypes

from zope.interface import implements

from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from plone.memoize.compress import xhtml_compress
from plone.memoize import ram
from plone.memoize.instance import memoize
from plone.app.portlets.cache import render_cachekey

class IMyGroupsPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IMyGroupsPortlet)

    def __init__(self):
        pass

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return "My Groups"


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    _template = ViewPageTemplateFile('mygroupsportlet.pt')

    @ram.cache(render_cachekey)
    def render(self):
        """
        Render the My groups portlet
        """
        return xhtml_compress(self._template())

    @property
    def available(self):
        """
        Only available if the user can access a groupspace
        """
        return len(self._data())

    def allowed_groupspaces(self):
        """
        Returns the groupspaces a user is allowed to see.
        """
        return self._data()

    @memoize
    def _data(self):
        """
        Return the catalog brains of all accessible groupspaces.        
        """
        context = aq_inner(self.context)

        catalog = getToolByName(context, 'portal_catalog')

        allowed = self._getUserAndGroupIds()
        if allowed == []:
            return []
            
        return catalog(portal_type='GroupSpace',
                       allowedLocalUsersAndGroups=allowed,
                       sort_on='sortable_title')


    def _getUserAndGroupIds(self):
        """
        Return a list of allowed groups and users usable in a
        catalog search of allowedLocalUsersAndGroups.
        """
        membership = getToolByName(self.context, 'portal_membership', None)
        if membership is None or membership.isAnonymousUser():
            return []
        member = membership.getAuthenticatedMember()
        if not member:
            return []
        member_id = member.getId()
        if member_id is None:
            # Basic users such as the special Anonymous users have no
            # id, but we can use their username instead.
            try:
                member_id = member.getUserName()
            except AttributeError:
                pass
        if not member_id:
            return []
        allowed = ['user:%s' % member_id]
        groups = member.getGroups()
        for group in groups:
            if type(group) in StringTypes:
                allowed.append('group:%s' % group)
        return allowed
        
class AddForm(base.NullAddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """

    def create(self):
        """
        Construct the added assignment.
        """
        return Assignment()
