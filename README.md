# cmdo


# WHAT IS CMDO (maya commands object)
`cmdo` is a oop python maya wrapperIt is mainly composed of a library of nodes (maya node wrappers)  
and an api to enable high level operations on nodes (ie: lockAndHideTransforms).  
At its core cmdo is built to operate on any kind of maya data, its nodes can be initialised with  
object names, MObjects or cmdo custom nodes

We can feed cmdo nodes to maya.cmds or maya.api.OpenMaya and get the native interaction and results.`*1`

Its purpose is to facilitate the interaction between maya and programmers and to be able to interact with any       
node type found in maya in an oop manner. To do this cmdo uses `maya.api.OpenMaya` for the base of its objects.

Furthermore, all cmdo nodes get data on demand most of the time, so we avoid heavy loading of the library and this  
enables cmdo nodes to always be up to date with their maya counterpart.

---

## Testing:

```python
import cmdo

# feedback is only for the reload function
# it does not act as a logger
cmdo.bigReload(feedback=False, flush=True)
```

## SubModules:
### api:
`cmdo.api` subPackage is dumped into the main namespace of the master package.  
This module is a wrapper of maya cmds/OpenMaya to return python objects  (for oop interaction).  
It is easy to access all functionalities through the main namespace like we would maya.cmds
```python
import cmdo

# returns a Graph object using specified flags (graph is a subclass of MSelectionList)
cameraNames = [
    'perspShape', 'frontShape', 'sideShape', 'topShape', 
    'leftShape', 'bottomShape', 'backShape'
]
graphObject = cmdo.ls(cameraNames, type='camera')

newNode = cmdo.createNode('transform', name='myNewNode')
newNode.name = 'newNodeName' 

# the api has a lot of high level operations
unusedNamespaces = cmdo.getAllUnusedNamespaces()
for namespace in unusedNamespaces:
    cmdo.removeNamespaces(namespace)

```

### nodes :
`cmdo.nodes` is a subPackage holding all maya node wrappers.  
They enable oop interaction with maya nodes and are returned through the api.  
They can take multiple input types such as, python types,  OpenMaya types or custom types


### core :
`cmdo.core` is a subPackage holding some important objets and operations used throughout cmdo.

Notably all classes that serve as a node base and that do not represent specific nodes.
The `graphLib`,  
which is used to interact with maya graphs (ie: ls, listRelatives ect). The `nodeRegistry` that holds a reference to all node  
classes that cmdo can wrap. And some modules to help, like exceptions, decorators ect.


### math :
`cmdo.math` is a library using `maya.api.OpenMaya` objects such as 
MMatrix and MVector to do math operations when possible

If the operation does not exist in the maya library 
it is implemented to return maya objects

---
# Extensions :
### node extensions :
Adding new nodes to `cmdo` is an easy task.  
All that is needed is to create a class that inherits from one of three bases or one of their subclasses.
- `nodeLib.Node`
> This is the most abstract class for cmdo nodes, it inherits directly from `maya.api.OpenMaya.MObject` 
> and implements lots of basic functionality and properties. It does not represent any node type inside maya.

- `dgLib.DGNode`
> This node inherits of `nodeLib.Node`. It represents the base of all non-DAG nodes of maya 
> (DG (Directed Graph): nodes without transforms and/or parenting hierarchy)

- `dagLib.DAGNode`
> This node inherits of `dgLib.DGNode`. It represents the base of all DAG nodes of maya. 
> It implements transform and hierarchy related properties  
> (DAG (Directed Acyclic Graph): nodes with transforms and/or parenting hierarchy)

Then override the `_NODE_TYPE` (maya.cmds type str) and `_API_TYPE` (maya.api.OpenMaya type int)  
class variables to the corresponding node.  
And add the new class to the `nodeRegistry.NodeRegistry` singleton class.  

This can be used to give access to third party nodes to cmdo, like plugin nodes

<details>
<summary> Exemple New Class: </summary>

Create a new class and register it to cmdo NodeRegistry

```python
from typing import List

from maya.api import OpenMaya as om

from cmdo.core.nodeRegistry import NodeRegistry
from cmdo.core.abstract import dagLib

# Create class that inherits from DAGNode
class Locator(dagLib.DAGNode):
    _NODE_TYPE = "locator"  # the maya type from maya.cmds
    _API_TYPE = om.MFn.kLocator  # see types in maya.api.OpenMaya.MFn doc

    @property
    def localScale(self) -> List[float]:
        """
        Get the localScale values
        
        Returns:
            List[float]: the localScale values
        """
        return self['localScale'].value
    
    @localScale.setter
    def localScale(self, value) -> None:
        """
        Set the localScale values
        
        Args:
            value: List[float], the localScale values to set
        """
        self['localScale'] = value
    
    @property
    def localPosition(self) -> List[float]:
        """
        Get the localPosition values
        
        Returns:
            List[float]: the localPosition values
        """
        return self['localPosition'].value
    
    @localPosition.setter
    def localPosition(self, value) -> None:
        """
        Set the localPosition values
        
        Args:
            value: List[float], the localPosition values to set
        """
        self['localPosition'] = value

        
# Register the class so that cmdo can interact with it/create it
NodeRegistry()[Locator.nodeType()] = Locator
```

Later cmdo will be able to wrap locator shapes with this class when they are query or created

```python
import cmdo

trs = cmdo.createNode('locator')
locator_instance = trs.shapes[0] # this will return a Locator class instance

locator_instance.localScale = [5, 5, 5]

```

</details>

---

# Exemples:
<details>

<summary>Exemple 1: Create a transform and get/set its translate and rotate attributes</summary>

```python
import cmdo

# return a transform python object
trs = cmdo.createNode('transform', name='myTransform')
# get the translation component from the new transform as vector3
# type cmdo.math.Vector3 is a subclass of OpenMaya.MVector
pos = trs.translate

# set new object translate and rotate
trs = cmdo.createNode('transform', name='newTransform')
trs.translate = pos
trs.rotate = [3.5, 50, -24.1]
```

</details>

<details>

<summary>Exemple 2: Get all the shapes and set their lineWidth attributes</summary>

```python
import cmdo

# get all controllers from scene 
# use the same syntax as maya ls, but return custom python objects
ctrls = cmdo.ls('*:*_CTRL')
for ctrl in ctrls:
    # get the shapes (Curve objects) of the current controller (Transform object)
    shapes = ctrl.shapes
    if not shapes:
        continue
    
    # for each shape set the lineWidth attribute
    for shape in shapes:
        # replace mc.setAttr(f'{shape}.lineWidth', 2)
        shape.lineWidth = 2
```

</details>

<details>

<summary>Exemple 3: Create, parent and match world transform</summary>

```python
import cmdo

cmdo.bigReload(flush=True)

# initialize an identity matrix as MMatrix (openMaya object)
my_matrix = cmdo.math.identityMatrix4

# get world matrix of the transform
trs1 = cmdo.createNode('transform', name='myTransform1')
trs1.displayLocalAxis = True
trs1.translate = [10, 20.58, 2]
trs1.rotate = [10, 20.58, 2]

prt = cmdo.createNode('transform', name='myTransform2_prt')
prt.translate = [-10, 10.58, -25]
prt.rotate = [0, -90, 54]

trs2 = cmdo.createNode('transform', name='myTransform2')
trs2.displayLocalAxis = True
trs2.parents = prt
trs2.resetTransformationMatrix()
trs2.worldMatrix = trs1.worldMatrix
```

</details>

<details>

<summary>Exemple 4: Create nodes and connect them</summary>

```python
import cmdo


def get_node(node_type, node_name):
    """
    Small function to create a node if it does not exist
    """
    
    if (node := cmdo.ls(node_name)):
       return node[0]
       
    return cmdo.createNode(node_type, name=node_name)

# create or get nodes
trs = get_node('transform', 'blockOutput_grp')
ctrl = get_node('locator', 'blockController_ctrl')
jntRoot = get_node('joint', 'skinJointRoot_skn')
jnt = get_node('joint', 'skinJoint_skn')
mltMtx = get_node('multMatrix', 'skinJoint_mltMtx')
dcpMtx = get_node('decomposeMatrix', 'skinJoint_dcpMtx')

# set some attributes, different ways to do this
# using properties if they exist, the plug name directly or using a dict
trs['displayLocalAxis'] = True
ctrl.parents = trs

kwargs = {
    'localScale': [2, 2, 2],
    'overrideEnabled': True,
    'overrideColor': 13
}
ctrl.shapes[0].setAttrFromDict(kwargs)

jnt.parents = jntRoot
jnt['displayLocalAxis'] = True

# connect the setup using "=" or ">>" 
# "=" connects destination_plug = source_plug (can be used with properties)
# ">>" connects source_plug >> destination_plug
jntRoot.offsetParentMatrix = trs['worldMatrix'][0]

ctrl['worldMatrix'][0] >> mltMtx['matrixIn'][0]
jnt['parentInverseMatrix'][0] >> mltMtx['matrixIn'][1]
mltMtx['matrixSum'] >> dcpMtx['inputMatrix']

for plugName in ['translate', 'rotate', 'scale', 'shear']:
    jnt[plugName] = dcpMtx[f'output{plugName.capitalize()}']
    
# move controller
ctrl.translate = [3, 5, 2]
ctrl.rotate = [-30.2, 17.154, 23]
ctrl.scale = [1.1, 1.2, 1]
```

</details>

---

# TODO:
- Add Undo/Redo:
```python
# TODO: Add Undo/Redo in maya.api.OpenMaya... not looking forward to that... 
#  currently the library that implements OpenMaya behavior doesn't support 
#  undoing or redoing
```

- Add lazy imports to bypass circular/partial import problems
```python
# TODO: Plug.__hash__ need to remove the node hashing and find a way
#  to get the cmdo node without circular import
#  one of the ways would be to add lazy imports to cmdo
```

- Add bifrost node/api:
```python
# TODO: Make bifrost class and api to interact with it
```

- Update api.deformers:
```python
# TODO: upgrade to take om & cmdo types
```

- Update/Remove core.convert (replace in nodes and api)
```python
# TODO: probably remove / rework all of this
```

- Update/Remove core.decorators (replace in nodes and api)
```python
# TODO: probably remove / rework all of this
```

- Update/Remove core.exportLib (move to department specific code)
```python
# TODO: MOVE TO ANOTHER LIBRARY "RIG"
```

- Full refactor core.file_lib (it's legacy code from TAR, it's no good)
```python
# TODO: REFACTOR THE HELL OUT OF THIS MODULE
```

- Update nodes.dag.camera class
```python
# TODO: add useful camera properties
```

- Fix/Update nodes.dg.animCurve_lib
```python
# TODO: find solutions for all the different animCurve types
```

- Update nodes.dg.blendshape_lib
```python
# TODO: I don t want to do it yet... is such an annoying deformer in maya script
# TODO: move some functions to deformer api
```

- Fix nodes.dg.plugMinusAverage interaction
```python
# TODO: ALSO, since input2D and input3D are compoundAttributes
#  containing multiAttributes, to set one of them ie: input2D[index],
#  we need to give as argument an iterable of an iterable
#  ie: pm.setInput2D(index, [[1, 2]])
#  this will set the x and y component of the input2D[index] where x=1 and y=2
#  otherwise we can set specific components of the multiAttribute one by one
#  ie: pm.setInput2Dx(index, 1)
#  ie: pm.setInput2Dy(index, 2)
#  THIS IS ANNOYING WE NEED TO FIX THIS!!!!!
```

- Update nodes.dg.skinCluster, add more interactions
```python
# TODO: continue adding properties and functions
# TODO: add multi-mesh support 
# TODO: refactor some functions to OpenMaya
```

---

# MISC
`*1`: This is True for cmdo objects to OpenMaya, but not yet for maya.cmds


