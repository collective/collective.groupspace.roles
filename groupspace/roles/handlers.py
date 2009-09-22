from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from Products.GrufSpaces.config import PLACEFUL_WORKFLOW_POLICY
from Products.CMFPlacefulWorkflow.PlacefulWorkflowTool import WorkflowPolicyConfig_id
        
def add_local_groupspace_workflow(groupspace, event):
    """Apply the local workflow when a groupspace is added.
    """
    placeful_workflow = getToolByName(groupspace, 'portal_placeful_workflow')
    groupspace.manage_addProduct['CMFPlacefulWorkflow'].manage_addWorkflowPolicyConfig()
    #
    # Calling getWorkflowPolicyConfig directly is not possible because of an 
    # explicit check in CMFPlacefulWorkflow for the permission "Manage portal",
    # which Contributors don't have. This would only make it possible for 
    # managers to add GroupSpaces, which doesn't make sense.
    #
    # config = placeful_workflow.getWorkflowPolicyConfig(groupspace)
    #
    # Instead need to do what the getWorkflowPolicyConfig method does after
    # the permission check:
    #
    config = getattr(groupspace.aq_explicit, WorkflowPolicyConfig_id)
    config.setPolicyBelow(policy=PLACEFUL_WORKFLOW_POLICY)
        
