from typing import Optional, List, Union

from maya.api import OpenMaya as om

from ...core.abstract import dgLib
from ...core.nodeRegistry import NodeRegistry


class AbstractMaterial(dgLib.DGNode):

    """
    An abstract class with all properties shared across materials

    """

    _colorAttributes = {
        'standardSurface': 'baseColor',
        'lambert': 'color',
        'blinn': 'color',
        'phong': 'color',
        'phongE': 'color',
        'usdPreviewSurface': 'diffuseColor',
    }

    @property
    def diffuseValue(self) -> List[float]:
        """
        Get the value of color attribute.

        Works for:
            - standardSurface
            - lambert
            - blinn
            - phong
            - phongE
            - usdPreviewSurface

        :return: List[float], the value of the color attribute
        """

        # baseColor is the attribute of standardSurface material and
        # should be considered the default material type
        return self[self._colorAttributes.get(self.type, 'color')].value

    @diffuseValue.setter
    def diffuseValue(self, value: List[float]) -> None:
        """
        Set the value of color attribute.

        Works for:
            - standardSurface
            - lambert
            - blinn
            - phong
            - phongE
            - usdPreviewSurface

        :param value: List[float], the value of the color attribute
        """

        # baseColor is the attribute of standardSurface material and
        # should be considered the default material type
        self[self._colorAttributes.get(self.type, 'color')] = value

    @property
    def outColor(self) -> List[float]:
        """
        Get the outColor value

        :return: List,[float]: the outColor value
        """

        return [
            self.outColorR,
            self.outColorG,
            self.outColorB
        ]

    @outColor.setter
    def outColor(self, value: List[float]):
        """
        Set the outColor value

        :param value: List[float], the outColor value
        """

        self['outColor'] = value

    @property
    def outColorR(self) -> float:
        """
        Get the outColorR value

        :return: float, the outColorR value
        """

        return self['outColorR'].asFloat()

    @outColorR.setter
    def outColorR(self, value: float) -> None:
        """
        Set the outColorR value

        :param value: float, the outColorR value
        """

        self['outColorR'] = value

    @property
    def outColorG(self) -> float:
        """
        Get the outColorG value

        :return: float, the outColorG value
        """

        return self['outColorG'].asFloat()

    @outColorG.setter
    def outColorG(self, value: float) -> None:
        """
        Set the outColorG value

        :param value: float, the outColorG value
        """

        self['outColorG'] = value

    @property
    def outColorB(self) -> float:
        """
        Get the outColorB value

        :return: float, the outColorB value
        """

        return self['outColorB'].asFloat()

    @outColorB.setter
    def outColorB(self, value: float) -> None:
        """
        Set the outColorB value

        :param value: float, the outColorB value
        """

        self['outColorB'] = value

    @property
    def outTransparency(self) -> List[float]:
        """
        Get the outTransparency value

        :return: List,[float]: the outTransparency value
        """

        return [
            self.outTransparencyR,
            self.outTransparencyG,
            self.outTransparencyB
        ]

    @outTransparency.setter
    def outTransparency(self, value: List[float]):
        """
        Set the outTransparency value

        :param value: List[float], the outTransparency value
        """

        self['outTransparency'] = value

    @property
    def outTransparencyR(self) -> float:
        """
        Get the outTransparencyR value

        :return: float, the outTransparencyR value
        """

        return self['outTransparencyR'].asFloat()

    @outTransparencyR.setter
    def outTransparencyR(self, value: float) -> None:
        """
        Set the outTransparencyR value

        :param value: float, the outTransparencyR value
        """

        self['outTransparencyR'] = value

    @property
    def outTransparencyG(self) -> float:
        """
        Get the outTransparencyG value

        :return: float, the outTransparencyG value
        """

        return self['outTransparencyG'].asFloat()

    @outTransparencyG.setter
    def outTransparencyG(self, value: float) -> None:
        """
        Set the outTransparencyG value

        :param value: float, the outTransparencyG value
        """

        self['outTransparencyG'] = value

    @property
    def outTransparencyB(self) -> float:
        """
        Get the outTransparencyB value

        :return: float, the outTransparencyB value
        """

        return self['outTransparencyB'].asFloat()

    @outTransparencyB.setter
    def outTransparencyB(self, value: float) -> None:
        """
        Set the outTransparencyB value

        :param value: float, the outTransparencyB value
        """

        self['outTransparencyB'] = value


class Lambert(AbstractMaterial):
    _NODE_TYPE = "lambert"
    _API_TYPE = om.MFn.kLambert

    @property
    def color(self) -> List[float]:
        """
        Get the color value

        :return: List,[float]: the color value
        """

        return [
            self.colorR,
            self.colorG,
            self.colorB
        ]

    @color.setter
    def color(self, value: List[float]):
        """
        Set the color value

        :param value: List[float], the color value
        """

        self['color'] = value

    @property
    def colorR(self) -> float:
        """
        Get the colorR value

        :return: float, the colorR value
        """

        return self['colorR'].asFloat()

    @colorR.setter
    def colorR(self, value: float) -> None:
        """
        Set the colorR value

        :param value: float, the colorR value
        """

        self['colorR'] = value

    @property
    def colorG(self) -> float:
        """
        Get the colorG value

        :return: float, the colorG value
        """

        return self['colorG'].asFloat()

    @colorG.setter
    def colorG(self, value: float) -> None:
        """
        Set the colorG value

        :param value: float, the colorG value
        """

        self['colorG'] = value

    @property
    def colorB(self) -> float:
        """
        Get the colorB value

        :return: float, the colorB value
        """

        return self['colorB'].asFloat()

    @colorB.setter
    def colorB(self, value: float) -> None:
        """
        Set the colorB value

        :param value: float, the colorB value
        """

        self['colorB'] = value


class Blinn(Lambert):
    _NODE_TYPE = "blinn"
    _API_TYPE = om.MFn.kBlinn


class Phong(Lambert):
    _NODE_TYPE = "phong"
    _API_TYPE = om.MFn.kPhong


class PhongE(Lambert):
    _NODE_TYPE = "phongE"
    _API_TYPE = om.MFn.kPhongExplorer


class StandardSurface(AbstractMaterial):
    _NODE_TYPE = "standardSurface"
    _API_TYPE = om.MFn.kStandardSurface

    @property
    def baseColor(self) -> List[float]:
        """
        Get the baseColor value

        :return: List,[float]: the baseColor value
        """

        return [
            self.baseColorR,
            self.baseColorG,
            self.baseColorB
        ]

    @baseColor.setter
    def baseColor(self, value: List[float]):
        """
        Set the baseColor value

        :param value: List[float], the baseColor value
        """

        self['baseColor'] = value

    @property
    def baseColorR(self) -> float:
        """
        Get the baseColorR value

        :return: float, the baseColorR value
        """

        return self['baseColorR'].asFloat()

    @baseColorR.setter
    def baseColorR(self, value: float) -> None:
        """
        Set the baseColorR value

        :param value: float, the baseColorR value
        """

        self['baseColorR'] = value

    @property
    def baseColorG(self) -> float:
        """
        Get the baseColorG value

        :return: float, the baseColorG value
        """

        return self['baseColorG'].asFloat()

    @baseColorG.setter
    def baseColorG(self, value: float) -> None:
        """
        Set the baseColorG value

        :param value: float, the baseColorG value
        """

        self['baseColorG'] = value

    @property
    def baseColorB(self) -> float:
        """
        Get the baseColorB value

        :return: float, the baseColorB value
        """

        return self['baseColorB'].asFloat()

    @baseColorB.setter
    def baseColorB(self, value: float) -> None:
        """
        Set the baseColorB value

        :param value: float, the baseColorB value
        """

        self['baseColorB'] = value


class UsdPreviewSurface(AbstractMaterial):
    _NODE_TYPE = "usdPreviewSurface"
    _API_TYPE = om.MFn.kPluginDependNode

    @property
    def diffuseColor(self) -> List[float]:
        """
        Get the diffuseColor value

        :return: List,[float]: the diffuseColor value
        """

        return [
            self.diffuseColorR,
            self.diffuseColorG,
            self.diffuseColorB
        ]

    @diffuseColor.setter
    def diffuseColor(self, value: List[float]):
        """
        Set the diffuseColor value

        :param value: List[float], the diffuseColor value
        """

        self['diffuseColor'] = value

    @property
    def diffuseColorR(self) -> float:
        """
        Get the diffuseColorR value

        :return: float, the diffuseColorR value
        """

        return self['diffuseColorR'].asFloat()

    @diffuseColorR.setter
    def diffuseColorR(self, value: float) -> None:
        """
        Set the diffuseColorR value

        :param value: float, the diffuseColorR value
        """

        self['diffuseColorR'] = value

    @property
    def diffuseColorG(self) -> float:
        """
        Get the diffuseColorG value

        :return: float, the diffuseColorG value
        """

        return self['diffuseColorG'].asFloat()

    @diffuseColorG.setter
    def diffuseColorG(self, value: float) -> None:
        """
        Set the diffuseColorG value

        :param value: float, the diffuseColorG value
        """

        self['diffuseColorG'] = value

    @property
    def diffuseColorB(self) -> float:
        """
        Get the diffuseColorB value

        :return: float, the diffuseColorB value
        """

        return self['diffuseColorB'].asFloat()

    @diffuseColorB.setter
    def diffuseColorB(self, value: float) -> None:
        """
        Set the diffuseColorB value

        :param value: float, the diffuseColorB value
        """

        self['diffuseColorB'] = value


NodeRegistry()[Lambert.nodeType()] = Lambert
NodeRegistry()[Blinn.nodeType()] = Blinn
NodeRegistry()[Phong.nodeType()] = Phong
NodeRegistry()[PhongE.nodeType()] = PhongE
NodeRegistry()[StandardSurface.nodeType()] = StandardSurface
NodeRegistry()[UsdPreviewSurface.nodeType()] = UsdPreviewSurface
