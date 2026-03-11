from typing import List, Any

from maya import cmds
from maya.api import OpenMaya as om

# * import list
__all__: List[str] = [
    'ROOT_NAMESPACE',
    'BASE_NAMESPACES',
    'namespaceExists',
    'getAllNamespaces',
    'getAllUnusedNamespaces',
    'addNamespace',
    'removeNamespace',
    'removeAllNamespaces',
    'getObjectsFromNamespace',
    'moveNamespace',
]


# reference to the root namespace function
ROOT_NAMESPACE = om.MNamespace.rootNamespace

# the names of non-deletable namespaces
BASE_NAMESPACES = [':UI', ':shared']


def namespaceExists(namespace: str) -> bool:
    """
    Check if the given namespace exists

    :param namespace: str, the namespace to check

    :return: bool, whether the namespace exists or not
    """

    return om.MNamespace.namespaceExists(namespace)


def getAllNamespaces(recursive: bool = True) -> List[str]:
    """
    Gets all the namespaces in the scene and sorts the in ascending order
    (child -> parent). Remove non-deletable namespaces from the list

    :param recursive: bool, whether to check children namespaces recursively

    :return: List[str], list of all namespaces in the scene
    """
    
    allNamespaces = [
        namespace
        for namespace in om.MNamespace.getNamespaces(recurse=recursive)
        if namespace not in BASE_NAMESPACES
    ]
    allNamespaces.sort(key=len, reverse=True)

    return allNamespaces


def getAllUnusedNamespaces(recursive: bool = True) -> List[str]:
    """
    Get all namespace without content aka "unused"

    :param recursive: bool, whether to check children namespaces recursively

    :return: List[str], a list of unused namespaces
    """

    # get all namespaces that don t have content
    unusedNamespace = [
        namespace for namespace in om.MNamespace.getNamespaces(recurse=recursive)
        if namespace not in BASE_NAMESPACES
        and not om.MNamespace.getNamespaceObjects(namespace, recurse=True)
    ]

    return unusedNamespace


def addNamespace(namespace: str, parentNamespace: str = None, setCurrent: bool = False) -> None:
    """
    Create the given namespace

    :param namespace: str, the name of the new namespace to create
    :param parentNamespace: str, the name of the parent namespace if any
    :param setCurrent: whether to set the new namespace as current
    """

    if namespaceExists(namespace):
        return

    om.MNamespace.addNamespace(namespace, parent=parentNamespace)

    if setCurrent:
        om.MNamespace.setCurrentNamespace(namespace)


def removeNamespace(namespace: str, deleteContent: bool = False) -> None:
    """
    Delete the given namespace and move content to root or delete content

    :param namespace: str, the namespace to remove
    :param deleteContent: bool, delete namespace content with namespace
    """

    if not om.MNamespace.namespaceExists(namespace):
        cmds.warning(
            f'Namespace does not exist : {namespace}'
            f'\n\tProvide absolute name to remove namespace'
        )
        return

    if deleteContent:
        mObjects = getObjectsFromNamespace(namespace)

        objectsToDelete = []
        for mObject in mObjects:
            if mObject.isNull():
                continue

            objectName = om.MFnDependencyNode(mObject).uniqueName()
            if objectName.startswith(':'):
                objectName = objectName[1:]

            objectsToDelete.append(objectName)

        cmds.delete(*cmds.ls(*objectsToDelete))

    om.MNamespace.moveNamespace(namespace, ROOT_NAMESPACE(), force=True)
    om.MNamespace.removeNamespace(namespace, removeContents=False)


def removeAllNamespaces() -> None:
    """
    Moves the contents of every namespace to the root namespace and deletes it

    """

    for namespace in getAllNamespaces():
        removeNamespace(namespace)


def getObjectsFromNamespace(namespace: str) -> List[om.MObject]:
    """
    Get objects from the given namespace

    :param namespace: str, the namespace to get objects from

    :return: list[str], a list of objects in the given namespace

    """

    if not namespaceExists(namespace):
        return []

    return om.MNamespace.getNamespaceObjects(namespace, recurse=True)


def moveNamespace(source: str, destination: str, force: bool = False, ensureExists: bool = True) -> None:
    """
    Move the contents of the namespace 'source' into the namespace 'destination'

    :param source: str, the source namespace
    :param destination: str, the destination namespace
    :param force: bool, force move the namespace
    :param ensureExists: bool, if True, create the namespaces if any do not exist

    """

    if not om.MNamespace.namespaceExists(source) and ensureExists:
        om.MNamespace.addNamespace(source)

    if not om.MNamespace.namespaceExists(destination) and ensureExists:
        om.MNamespace.addNamespace(destination)

    om.MNamespace.moveNamespace(source, destination, force=force)
