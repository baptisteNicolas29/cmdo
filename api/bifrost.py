"""
Api interaction with maya bifrost
"""

from maya import cmds


# TODO: Make bifrost class and api to interact with it

# def create_bifrost_applyDeformationDeltas() -> str:
#
#     # Create bifrost graph shape and retrieve it
#     bifrost_board = cmds.createNode('bifrostGraphShape', name='c_applyDeformationDeltas_bifGrf').shapes[0]
#
#     # add applyDeformationDeltas compound to graph
#     cmds.vnnCompound(bifrost_board, '/', addNode='BifrostGraph,User::Compounds,applyDeformationDeltas')
#
#     # create input / output attributes in the graph
#     cmds.vnnNode(bifrost_board, '/input', createOutputPort=('originalGeometry', 'Object'), portValues=True)
#     cmds.vnnNode(bifrost_board, '/input', createOutputPort=('targetGeometries', 'array<Object>'), portValues=True)
#     cmds.vnnNode(bifrost_board, '/output', createInputPort=('outMesh', 'Object'), portValues=True)
#
#     # connect compound to input / output
#     cmds.vnnConnect(bifrost_board, '/input.originalGeometry', '/applyDeformationDeltas.originalGeometry', copyMetaData=True)
#     cmds.vnnConnect(bifrost_board, '/input.targetGeometries', '/applyDeformationDeltas.targetGeometries', copyMetaData=True)
#     cmds.vnnConnect(bifrost_board, '/applyDeformationDeltas.outMesh', '/output.outMesh')
#
#     return bifrost_board
