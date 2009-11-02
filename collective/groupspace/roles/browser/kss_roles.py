from zope.interface import implements
from zope.component import getMultiAdapter

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from kss.core.interfaces import IKSSView
from plone.app.kss.plonekssview import PloneKSSView as base


class KSSRolesView(base):
    """KSS view for roles page.
    """
    implements(IKSSView)

    template = ViewPageTemplateFile('groupspace_roles.pt')
    macro_wrapper = ViewPageTemplateFile('macro_wrapper.pt')
    
    def updateRolesInfo(self, search_term=''):
        roles = getMultiAdapter((self.context, self.request,), name="roles")
    
        # get the html from a macro
        ksscore = self.getCommandSet('core')

        the_id = 'user-group-roles'
        macro = self.template.macros[the_id]
        res = self.macro_wrapper(the_macro=macro, instance=self.context, view=roles)
        ksscore.replaceHTML(ksscore.getHtmlIdSelector(the_id), res)

        return self.render()

