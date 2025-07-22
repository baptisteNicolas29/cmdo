from typing import List

from maya import cmds as mc
from maya.api import OpenMaya as om

# * import list
__all__ = [
    'ROOT_NAMESPACE',
    'BASE_NAMESPACES',
    'namespaceExists',
    'getAllNamespaces',
    'getAllUnusedNamespaces',
    'addNamespace',
    'removeNamespace',
    'removeAllNamespaces',
    'getObjectsFromNamespace',
]


# reference to the root namespace function
ROOT_NAMESPACE = om.MNamespace.rootNamespace

# the names of non-deletable namespaces
BASE_NAMESPACES = [':UI', ':shared']


def namespaceExists(namespace: str) -> bool:
    """
    Check if the given namespace exists
    Args:
        namespace: str, the namespace to check

    Returns:
        bool, whether the namespace exists or not
    """

    return om.MNamespace.namespaceExists(namespace)


def getAllNamespaces(recursive: bool = True):
    """
    Gets all the namespaces in the scene and sorts the in ascending order
    (child -> parent). Remove non-deletable namespaces from the list
    Returns:

    """
    all_namespaces = [
        namespace
        for namespace in om.MNamespace.getNamespaces(recurse=recursive)
        if namespace not in BASE_NAMESPACES
    ]
    all_namespaces.sort(key=len, reverse=True)

    return all_namespaces


def getAllUnusedNamespaces(recursive: bool = True) -> List[str]:
    """
    Gets all the namespaces in the scene and sorts them in ascending order
    (child -> parent). Remove namespaces without content
    Returns: a list of namespaces -> ie: ['a:b:c', 'a:b', 'a']

    """

    # get all namespaces that don t have content
    unused_namespaces = [
        namespace for namespace in om.MNamespace.getNamespaces(recurse=recursive)
        if namespace not in BASE_NAMESPACES
        and not om.MNamespace.getNamespaceObjects(namespace, recurse=True)
    ]

    return unused_namespaces


def addNamespace(
    namespace: str,
    parent_namespace: str = None,
    set_current: bool = False
) -> None:
    """
    Create the given namespace to the scene
    Args:
        namespace: str, the name of the new namespace to create
        parent_namespace: str, the name of the parent namespace if any
        set_current: whether to set the new namespace as current

    Returns:

    """
    if namespaceExists(namespace):
        return

    om.MNamespace.addNamespace(namespace, parent=parent_namespace)

    if set_current:
        om.MNamespace.setCurrentNamespace(namespace)


def removeNamespace(namespace: str, delete_content: bool = False) -> None:
    """
    Delete the given namespace and move content to root

    Args:
        namespace: str, the namespace to remove
        delete_content: bool, delete namespace content with namespace

    """
    if not om.MNamespace.namespaceExists(namespace):
        mc.warning(
            f'Namespace does not exist : {namespace}'
            f'\n\tProvide absolute name to remove namespace'
        )
        return

    if delete_content:
        m_objects = getObjectsFromNamespace(namespace)

        for m_object in m_objects:
            if m_object.isNull() or m_object.apiType() != om.MFn.kTransform:
                continue

            obj_name = om.MFnDagNode(m_object).fullPathName()
            if mc.objExists(obj_name):
                mc.delete(obj_name)

    om.MNamespace.moveNamespace(namespace, ROOT_NAMESPACE(), force=True)
    om.MNamespace.removeNamespace(namespace, removeContents=False)


def removeAllNamespaces() -> None:
    """
    Moves the contents of every namespace to the root namespace and deletes it
    Returns:

    """
    for namespace in getAllNamespaces():
        removeNamespace(namespace)


def getObjectsFromNamespace(namespace: str) -> List[om.MObject]:
    """
    Get objects from the given namespace
    Args:
        namespace: str, the namespace to get objects from

    Returns:
        list[str], a list of objects in the given namespace
    """
    if not namespaceExists(namespace):
        return []

    return om.MNamespace.getNamespaceObjects(namespace, recurse=True)
