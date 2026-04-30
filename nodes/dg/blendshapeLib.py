from typing import List, Union, Dict
import dataclasses

from ... import cmds, om

from ...core.cmdoTyping import CmdoObject
from ...core.abstract import geometryFilterLib
from ...core.nodeRegistry import NodeRegistry
from ...core.exceptions import CmdoException


@dataclasses.dataclass(kw_only=True)
class DefaultTarget:
    name: str
    weight: float
    weightIndex: int
    index: int
    value: float
    attr: str
    inputTarget: str
    targetGeometry: str
    inbetweens: List = dataclasses.field(default_factory=list)
    isEditing: bool = False
    isComboShape: bool = False


@dataclasses.dataclass(kw_only=True)
class InbetweenTarget:
    index: int
    value: float
    attr: str
    inputTarget: int
    targetGeometry: str


class BlendShape(geometryFilterLib.GeometryFilter):
    _NODE_TYPE = 'blendShape'
    _API_TYPE = om.MFn.kBlendShape

    @property
    def inbetweenTypeList(self):
        return ['relative', 'absolute']

    @property
    def attrStringTemplate(self):
        return (
                self.name + ".inputTarget[{inputTarget}]."
                            "inputTargetGroup[{targetIndex}].inputTargetItem"
        )

    def getTargets(self) -> List[DefaultTarget]:
        targetList: List[DefaultTarget] = []

        aliases = cmds.aliasAttr(self.name, query=True) or []
        inputTargets = cmds.getAttr(
            f"{self}.inputTarget",
            multiIndices=True
        ) or [0]

        for i in range(0, len(aliases), 2):

            name = aliases[i]
            wAttr = aliases[i + 1]

            tgtIndex = int(wAttr[wAttr.find('[') + 1: wAttr.find(']')])

            # current weight value
            current = cmds.getAttr(f"{self}.{name}")

            weightInfo = {
                "name": name,
                "weight": current,
                'weightIndex': tgtIndex
            }

            # Iterate over all targets (only index 0 is used usually)
            currentTarget = None
            inbetweens = []
            for it in inputTargets:
                base = self.attrStringTemplate.format(
                    inputTarget=it,
                    targetIndex=tgtIndex
                )

                items = cmds.getAttr(base, multiIndices=True) or []
                for idx in items:
                    plug = f"{base}[{idx}].inputGeomTarget"
                    inputGeom = cmds.connectionInfo(plug,
                                                    sourceFromDestination=True)
                    if cmds.objExists(plug):

                        if int((idx - 5000) / 1000.0) == 1:
                            currentTarget = DefaultTarget(
                                name=name,
                                weight=current,
                                weightIndex=tgtIndex,
                                index=idx,
                                value=(idx - 5000) / 1000.0,
                                attr=plug,
                                inputTarget=it,
                                targetGeometry=inputGeom
                            )
                        else:
                            inbetweens.append(InbetweenTarget(
                                index=idx,
                                value=(idx - 5000) / 1000.0,
                                attr=plug,
                                inputTarget=it,
                                targetGeometry=inputGeom
                            ))

            currentTarget.inbetweens = sorted(inbetweens, key=lambda x: x.index)
            targetList.append(currentTarget)

        return targetList

    def getInfo(self) -> List[Dict]:
        """
        Get blendShape target and weight info as a dictionary

        :return: List[Dict]
        """

        info = []
        aliases = cmds.aliasAttr(self.name, query=True) or []
        inputTargets = cmds.getAttr(
            f"{self}.inputTarget",
            multiIndices=True
        ) or [0]

        for i in range(0, len(aliases), 2):

            name = aliases[i]
            wAttr = aliases[i + 1]

            tgtIndex = int(wAttr[wAttr.find('[') + 1: wAttr.find(']')])

            # current weight value
            current = cmds.getAttr(f"{self}.{name}")

            weightInfo = {
                'name': name,
                'weight': current,
                'weightIndex': tgtIndex
            }

            # Iterate over all targets (only index 0 is used usually)
            currentTarget = None
            inbetweens = []
            for it in inputTargets:
                base = self.attrStringTemplate.format(
                    inputTarget=it,
                    targetIndex=tgtIndex
                )

                items = cmds.getAttr(base, multiIndices=True) or []
                for idx in items:
                    plug = f"{base}[{idx}].inputGeomTarget"
                    inputGeom = cmds.connectionInfo(plug, sourceFromDestination=True)
                    if cmds.objExists(plug):

                        if int((idx - 5000) / 1000.0) == 1:
                            weightInfo["defaultWeight"] = {
                                "index": idx,
                                "value": (idx - 5000) / 1000.0,
                                "attr": plug,
                                "inputTarget": it,
                                "targetGeometry": inputGeom
                            }

                        else:
                            inbetweens.append({
                                "index": idx,
                                "value": (idx - 5000) / 1000.0,
                                "attr": plug,
                                "inputTarget": it,
                                "targetGeometry": inputGeom
                            })

            weightInfo["inbetweens"] = sorted(
                inbetweens,
                key=lambda x: x["index"]
            )
            info.append(weightInfo)

        return info

    def getTargetInfo(self, index: Union[int, str]) -> Dict:
        return targetInfo[0] if (targetInfo := list(filter(
            lambda info: info["weightIndex"] == index
                if isinstance(index, int)
                else info["name"] == index,
            self.getInfo()
        ))) else {}

    def getTarget(self, value: Union[int, str]) -> Union[DefaultTarget, None]:
        match value:
            case int():
                return targetInfo[0] if (targetInfo := list(filter(
                    lambda target: target.weightIndex == value,
                    self.getTargets()
                ))) else None

            case str():
                return targetInfo[0] if (targetInfo := list(filter(
                    lambda target: target.name == value,
                    self.getTargets()
                ))) else None

            case _:
                raise CmdoException(f'Value needs to be of type in or str, got : {type(value)}')

    def getTargetInbetweenInfo(self, index: Union[int, str]) -> Dict:
        return self.getTargetInfo(index).get("inbetweens")

    @property
    def targetCount(self) -> int:
        return len(cmds.ls(f'{self}.weight[*]'))

    @property
    def targetNames(self) -> list[str]:
        return [target['name'] for target in self.getInfo()]

    def getTargetNameFromIndex(self, index: int) -> str:
        return self.getTargetInfo(index).get('name')

    def getTargetIndexFromName(self, name: str) -> int:
        return self.getTargetInfo(name).get('weightIndex')

    def targetHasInbetweens(self, index: int) -> bool:
        return bool(self.getTargetInbetweenInfo(index))

    def getEditingShape(self) -> bool:
        return cmds.blendShape(self.name, editTarget=True, query=True) or []

    def addTarget(self, sourceMesh: str) -> Dict:
        """
        Add a target mesh to the blendShape deformer.

        :param sourceMesh: mesh use to sculpt the target, defaults to None
        :param destinationMesh: mesh affected by the target, defaults to None

        :return: Dict, the target info
        """

        cmds.blendShape(
            self.name,
            edit=True,
            target=(
                self.outputGeometry[0],
                self.targetCount,
                sourceMesh,
                1.0
            ),
            weight=(self.targetCount, 0.0)
        )

        return self.getTargetInfo(self.targetCount)

    def addInbetweenTarget(self, sourceMesh: str, targetIndex: Union[int, str],
                           inbetweenWeight: float,
                           inbetweenType: str = 'absolute') -> Dict:
        """
        Adds an inbetween shape to a target

        :param sourceMesh: mesh to add as en inbetween shape
        :param targetIndex: the target index or name to add the inbetween to
        :param inbetweenWeight: the weight of the inbetween
        :param inbetweenType: the type of the inbetween ['relative', 'absolute']

        :return: Dict, the target info
        """
        if isinstance(targetIndex, str):
            targetIndex = self.getTargetIndexFromName(targetIndex)

        cmds.blendShape(
            self.name,
            edit=True,
            inBetween=True,
            inBetweenType=inbetweenType,
            target=(
                self.outputGeometry[0],
                targetIndex,
                sourceMesh,
                inbetweenWeight
            ),
        )

        return self.getTargetInfo(targetIndex)

    def addComboShape(self):
        ...

    def removeTarget(self, targetIndex: Union[int, str]):
        targetInfo = self.getTargetInfo(targetIndex)
        weightIndex = targetInfo.get('weightIndex')
        inputTargetIndex = targetInfo.get('inputTarget')

        weightAttribute = f"{self.name}.weight[{weightIndex}]"
        groupAttribute = f"{self.name}.inputTarget[{inputTargetIndex}].inputTargetGroup[{weightIndex}]"

        # b is the long name of the flag and if True,
        # it disconnects plugs before deleting
        cmds.removeMultiInstance(weightAttribute, b=True)
        cmds.removeMultiInstance(groupAttribute, b=True)

    def resetAllTargetWeights(self):
        return NotImplementedError('resetting all targets')

    def resetTargetWeight(self, arg: Union[int, str]):
        return NotImplementedError(f'Resetting target from idx {arg}')

    # TODO: move transfer to api
    def transferTo(self, arg: Union[str, om.MObject]):
        return NotImplementedError(f'Transferring target to obj {arg}')

    # TODO: maybe rebuild functions move to api as well
    def rebuildAllTargets(self):
        return NotImplementedError(f'Rebuilding all target')

    def rebuildTarget(self, arg: Union[int, str]):
        return NotImplementedError(f'Rebuilding target {arg}')


NodeRegistry()[BlendShape.nodeType()] = BlendShape
