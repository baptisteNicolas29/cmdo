# cmdo


# WHAT IS CMDO (maya commands object)
cmdo is a oop python maya wrapper. It is mainly composed of a library of nodes (wrapped maya nodes) and an api to operate the nodes.
At its core cmdo is built to operate on any kind of maya data. cmdo nodes can be initialised with object names, MObjects or cmdo custom nodes

We can feed cmdo nodes to maya.cmds or maya.api.OpenMaya and get the native interaction and results.

Its purpose is to facilitate the interaction between maya and programmers and to be able to interact with any node type found in maya in an oop manner.
To do this cmdo uses ```maya.api.OpenMaya``` for the base of its objects.


## SubModules:
### api:
```cmdo.api``` subPackage is dumped into the main namespace of the master package.

This module is a wrapper of maya cmds/OpenMaya to return python objects  (for oop interaction)

It is easy to access all functionalities through the main namespace like we would maya.cmds
```python
import cmdo

# returns a Graph object using specified flags (graph is a subclass of MSelectionList)
graph_object = cmdo.ls('someObjectName', flag='value')



```

### nodes:
```cmdo.nodes``` is a subPackage holding all maya node wrappers

They enable oop interaction with maya nodes and are returned through the api.

They can take multiple input types such as, python types,  OpenMaya types or custom types
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

### core:
```cmdo.core``` is a subPackage holding some important objets and operations used throughout cmdo.

Notably

### math
```cmdo.math``` is a library using ```maya.api.OpenMaya``` objects such as 
MMatrix and MVector to do math operations when possible

If the operation does not exist in the maya library 
it is implemented to return maya objects

```python
import cmdo

# initialize an identity matrix as MMatrix (openMaya object)
my_matrix = cmdo.math.identityMatrix

# get world matrix of the transform
trs = cmdo.createNode('transform', name='myTransform')
trs.worldMatrix = my_matrix
```




