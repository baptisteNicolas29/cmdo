from typing import Any, Union

import math


__all__ = [
    'angle_between',
    'get_barycenter',
    'Vector3'
]


NumType = int | float
NumList = tuple[NumType] | list[NumType]


def angle_between(vector1: NumList, vector2: NumList) -> float | None:
    """
    Return the angle between two vectors

    Args:
        vector1 NumList: a vector
        vector2 NumList: a vector

    Returns:
        float: The angle between the vectors
    """

    if len(vector1) != len(vector2):
        raise ValueError("Both vectors need to be of equal length")
    
    vector_length = len(vector1)
    
    vector_sum = sum(vector1[i] * vector2[i] for i in range(vector_length))
    vector1_sqrt = math.sqrt(sum(vector1[i] ** 2 for i in range(vector_length)))
    vector2_sqrt = math.sqrt(sum(vector2[i] ** 2 for i in range(vector_length)))

    return math.acos(vector_sum / vector1_sqrt * vector2_sqrt)


def get_barycenter(point_vectors):

    x_center, y_center, z_center = [], [], []

    for point_vector in point_vectors:
        x_center.append(point_vector[0])
        y_center.append(point_vector[1])
        z_center.append(point_vector[2])

    barycentric_position = (
        sum(x_center) / (len(x_center) or 1),
        sum(y_center) / (len(y_center) or 1),
        sum(z_center) / (len(z_center) or 1)
    )

    print(f'{barycentric_position = }')
    return barycentric_position


class Vector3(object):
    """
    Implementation of a Vector 3 Class

    Args:
        list|Tuple[int|float] | Vector3, list of values or Vector3 object

    Kwargs:
        dict, key, value pairs representing a vector3
    """

    @classmethod
    def unit_vector(cls):
        return cls(1, 1, 1)

    @classmethod
    def is_vector3(cls, vector: Any) -> bool:
        """
        Test if the input is an instance of Vector3

        Args:
            vector: the object to test
        Returns:
            bool : is it a Vector3 or not
        """
        return isinstance(vector, cls)

    @staticmethod
    def is_equal(a: NumType, b: NumType, epsilon: NumType = 0.0001) -> bool:
        """
        Test floating point number approximative equality
        
        Args:
            a: int|float, the first number to test
            b: int|float, the second number to test
            epsilon: int|float, the accepted threshold difference between a & b
        """
        return abs(a - b) < epsilon

    @staticmethod
    def is_num_type(number: NumType) -> bool:
        """
        Test if the input is an instance of int or float

        Args:
            number: int | float: the number to test
        Return:
            bool : is it a Vector3 or not
        """
        return isinstance(number, NumType)

    @staticmethod
    def from_dict(**kwargs) -> tuple:
        """
        Get vector3 components from a dictionary
        
        Args:
            kwargs: dict, dictionary holding xyz components
        
        Returns:
            tuple, x, y, z components
        """
        x = kwargs.get('x') or kwargs.get('X')
        y = kwargs.get('y') or kwargs.get('Y')
        z = kwargs.get('z') or kwargs.get('Z')
        return x, y, z

    @staticmethod
    def from_list(*args) -> tuple:
        """
        Get vector3 components from a list

        Args:
            args: tuple, a list holding xyz components or parts of it

        Returns:
            tuple, x, y, z components or None, None, None
        """
        length = length if (length := len(args)) != 3 else 3
        fill_list = [0 for _ in range(3 - length)]
        
        if not all(Vector3.is_num_type(num) for num in args):
            raise TypeError(
                f"{Vector3.__name__}.from_list only accepts -> {NumList}."
                f"\n\tGot args: {type(args)}<{args}>"
            )
        
        return tuple(list(args[:3]) + fill_list)

    @staticmethod
    def get_components(*args: list, **kwargs: dict) -> tuple:
        """
        Get the xyz component from supported input type

        Args:
            args: Vector3 | list | tuple | dict
            kwargs: dict['x':, 'y':, 'z':]

        Returns:
            tuple, x, y, z components
        """

        if args and Vector3.is_vector3(args[0]):
            xyz = Vector3.x, Vector3.y, Vector3.z

        elif args:
            xyz = Vector3.from_list(*args)

        elif kwargs:
            xyz = Vector3.from_dict(**kwargs)

        else:
            xyz = 0, 0, 0

        return xyz

    def __init__(self, *args, **kwargs) -> None:
        self.x, self.y, self.z = self.get_components(*args, **kwargs)

    @property
    def x(self) -> NumType:
        return self._x

    @x.setter
    def x(self, value: NumType) -> None:
        if not self.is_num_type(value):
            raise TypeError(
                f"{self.__class__.__name__}.x only accepts {NumType}."
                f"\n\tGot x: {type(value)}<{value}>"
            )

        self._x = value

    @property
    def y(self) -> NumType:
        return self._y

    @y.setter
    def y(self, value: NumType) -> None:
        if not self.is_num_type(value):
            raise TypeError(
                f"{self.__class__.__name__}.y only accepts {NumType}."
                f"\n\tGot y: {type(value)}<{value}>"
            )
        self._y = value

    @property
    def z(self) -> NumType:
        return self._z

    @z.setter
    def z(self, value: NumType) -> None:
        if not self.is_num_type(value):
            raise TypeError(
                f"{self.__class__.__name__}.z only accepts {NumType}."
                f"\n\tGot z: {type(value)}<{value}>"
            )

        self._z = value

    @property
    def xyz(self) -> NumList:
        return [self.x, self.y, self.z]

    @property
    def is_null(self):
        """
        Test if the current Vector3 is null (zero vector)

        Returns:
            bool: if all the components are equal to zero
        """

        return all(self.is_equal(x, 0) for x in self.xyz)

    @property
    def norm(self) -> float:
        """
        The Length of the current Vector3 instance

        Returns:
            scalar: int | float, the norm of the vector
        """
        return float(math.sqrt(self.x ** 2.0 + self.y ** 2.0 + self.z ** 2.0))

    @property
    def normalized(self) -> 'Vector3':
        """
        Gives the normalized version of the current Vector3

        Returns:
            Vector3 : normalized Vector3
        """
        return Vector3(
            [self.x / self.norm, self.y / self.norm, self.z / self.norm]
        )

    def __repr__(self) -> str:
        """
        The representation of the current Vector3

        Return:
            list : the output vector
        """
        # obj_repr = f"<{self.__class__} {id(self)}>"
        return f"{self.__class__.__name__}({self.x}, {self.y}, {self.z})"

    def __getitem__(self, index: int) -> NumType:
        """
        Get the element of the current Vector3 using the input index

        Args:
            index: the index to get
        Return:
            scalar : the output element
        """

        if -3 <= index <= 2:
            return [self.x, self.y, self.z][index]

        raise IndexError(
            f"{self.__class__.__name__} incorrect index: {index}"
            f"\n\tValid index range : [{-len(self)}, {len(self)-1}]"
        )

    def __add__(self, vector: Union[NumList, dict, 'Vector3']) -> 'Vector3':
        """
        Add the input vector to the current Vector3

        Args:
            vector: Vector3 | list | tuple | dict
        Return:
            Vector3 : new Vector3 with the added values
        """
        xyz = self.get_components(vector)

        if xyz:
            return Vector3(
                self.x + xyz[0],
                self.y + xyz[1],
                self.z + xyz[2],
            )

        raise TypeError(
            f"Unsupported type for __add__ -> {type(vector)}"
            f"\n Supported Types are:"
            f"\n\t- {self.__class__.__name__}, {NumType}, dict"
        )

    def __sub__(self, vector: Union[NumList, dict, 'Vector3']) -> 'Vector3':
        """
            Description:
                Subtract the input Vector3 from the current Vector3
            Arguments:
                vector: the Vector3 to Subtract
            Return:
                Vector3 : the output Vector3
        """
        xyz = self.get_components(vector)
        if xyz:
            return Vector3(
                self.x - xyz[0],
                self.y - xyz[1],
                self.z - xyz[2],
            )

        raise TypeError(
            f"Unsupported type for __add__ -> {type(vector)}"
            f"\n Supported Types are:"
            f"\n\t- {self.__class__.__name__}, {NumType}, dict"
        )

    def __eq__(self, vector: 'Vector3') -> bool:
        """
            Description:
                Test is equal to
            Arguments:
                vector: the Vector3 to test against
            Return:
                bool : if the xyz components of both vectors are equal
        """
        if self.is_vector3(vector):
            x_eq = self.is_equal(self.x, vector.x)
            y_eq = self.is_equal(self.y, vector.y)
            z_eq = self.is_equal(self.z, vector.z)

            return x_eq and y_eq and z_eq

        raise TypeError(
            f"Unsupported type for equality<__eq__>  -> {type(vector)}"
            f"\n Supported Types are:"
            f"\n\t- {self.__class__.__name__}"
        )

    def __ne__(self, vector: 'Vector3') -> bool:
        """
            Description:
                Test is not equal to
            Arguments:
                vector: the Vector3 to test against
            Return:
                bool : if the current Vector3 is not equal to the input Vector3
        """
        if self.is_vector3(vector):
            x_eq = not self.is_equal(self.x, vector.x)
            y_eq = not self.is_equal(self.y, vector.y)
            z_eq = not self.is_equal(self.z, vector.z)

            return x_eq and y_eq and z_eq

        raise TypeError(
            f"Unsupported type for not equality<__ne__> -> {type(vector)}"
            f"\n Supported Types are:"
            f"\n\t- {self.__class__.__name__}"
        )

    def __len__(self) -> int:
        """
        The length of the vector (3)

        Return:
            scalar : the length of the vector
        """
        return len(self.xyz)

    def __mul__(self, factor: NumType) -> 'Vector3':
        """
        Multiply the vector by a scalar

        Args:
            factor: int | float, the scalar to multiply the vector with
        Returns:
            Vector3 : the output vector
        """
        if self.is_num_type(factor):
            return Vector3(
                [self.x * factor, self.y * factor, self.z * factor]
            )

        raise TypeError(
            f"Unsupported type for multiplication<__mul__> -> {type(factor)}"
            f"\n Supported Types are:"
            f"\n\t- {NumType}"
        )

    def __truediv__(self, factor: NumType) -> 'Vector3':
        """
            Divide the vector by a scalar

            Args:
                factor: int | float, the scalar to divide the vector by
            Returns:
                Vector3 : the output vector
        """
        if self.is_num_type(factor) and not self.is_equal(factor, 0):
            return Vector3(
                [self.x / factor, self.y / factor, self.z / factor]
            )

        raise TypeError(
            f"Unsupported type for division<__truediv__> -> {type(factor)}"
            f"\n Supported Types are:"
            f"\n\t- {NumType} != 0"
        )

    def add(self, vector: Union[NumList, dict, 'Vector3']) -> None:
        """
        Perform an in place addition (add to self)

        Args:
            vector: tuple | list | dict | Vector3
        """
        xyz = self.get_components(vector)

        if xyz:
            self.x += xyz[0]
            self.y += xyz[1]
            self.z += xyz[2]

        raise TypeError(
            f"Unsupported type for add (in place addition) -> {type(vector)}"
            f"\n Supported Types are:"
            f"\n\t- {self.__class__.__name__}, {NumType}, dict"
        )

    def dot_product(self, vector: Union[NumList, dict, 'Vector3']) -> NumType:
        """
        Gives the result of dot product

        Args:
            vector: tuple | list | dict | Vector3,
                the vector to dot product with
        Return:
            scalar : the dot product of this Vector3 and the given Vector3
        """
        xyz = self.get_components(vector)

        if xyz:
            return self.x * xyz[0] + self.y * xyz[1] + self.z * xyz[2]

        raise TypeError(
            f"Unsupported type for dot_product -> {type(vector)}"
            f"\n Supported Types are:"
            f"\n\t- {self.__class__.__name__}, {NumType}, dict"
        )

    def cross_product(self, vector):
        """
        Gives the result of cross product

        Args:
            vector: tuple | list | dict | Vector3,
                the vector to cross product with
        Return:
            vector : the cross product of this Vector3 and the given Vector3
        """
        xyz = self.get_components(vector)

        x = (self.y * xyz[2]) - (self.z * xyz[1])
        y = (self.z * xyz[0]) - (self.x * xyz[2])
        z = (self.x * xyz[1]) - (self.y * xyz[0])

        return Vector3(x, y, z)

    def angle_between(self, vector, output_type=0):
        """
        Gives the angle between this Vector3 and the input Vector3

        Args:
            vector: tuple | list | dict | Vector3,
                the vector to get the angle with
            output_type: int, the output type (0 - radians or 1 - degrees)
        Return:
            scalar : the angle between this vector and
                the given vector as radians or degrees
        """
        vector3 = vector

        if not self.is_vector3(vector):
            vector3 = self.__class__(vector)

        dot_product = self.dot_product(vector3)
        angle = math.acos(dot_product / (self.norm * vector3.norm))

        if output_type == 0:
            return angle

        elif output_type == 1:
            return angle * 180 / math.pi

        raise TypeError(
            f"Unsupported type for angle_between -> {type(vector)}"
            f"\n Supported Types are:"
            f"\n\t- {self.__class__.__name__}, {NumType}, dict"
        )

    def scale(self, vector: Union[NumList, dict, 'Vector3']) -> None:
        """
        Scale the current vector

        Args:
            vector: tuple | list | dict | Vector3, the vector to scale with
        Return:
            vector3 : a vector scaled by the given factors
        """
        xyz = self.get_components(vector)

        if not all(self.is_num_type(x) for x in xyz):
            raise TypeError(
                f"{self.__class__.__name__}.scale() only accepts {NumType}."
                f"Got [x, y, z] : [{xyz[0]}, {xyz[1]}, {xyz[2]}]"
            )

        self.x *= xyz[0]
        self.y *= xyz[1]
        self.z *= xyz[2]
