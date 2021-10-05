"""Vehicle creation module"""

from abc import ABC, abstractmethod


class Transport(ABC):
    """Class template.
    __MAX_PERMISSIBLE_SPEED - class attribute, maximum allowed speed for
    movement of all vehicles, in kilometers per hour."""

    __MAX_PERMISSIBLE_SPEED = 150

    @abstractmethod
    def move(self):
        """Move vehicle."""
        ...

    @classmethod
    def valid_speed(cls, preset_speed: int):
        """Checks compliance with the speed limit for a given class of vehicles,
        and sets the speed of the vehicle not higher than the maximum permissible."""
        if preset_speed > cls.__MAX_PERMISSIBLE_SPEED:
            print(f"Maximum permissible speed for {cls.__name__} is {cls.__MAX_PERMISSIBLE_SPEED}"
                  f" kilometers per hour, so your top speed will be {cls.__MAX_PERMISSIBLE_SPEED}"
                  f" kilometers per hour")
            return cls.__MAX_PERMISSIBLE_SPEED
        return preset_speed


class Coach(Transport):
    """The creation of the Coach object and related functionality"""

    def __init__(self, name: str, max_speed: int):
        """The initializer for the class.

        Arguments:
        name -- the string representing the vehicle's name (what the owner called coach).
        _max_speed -- the integer, the maximum speed of this vehicle,
        indicated in kilometers per hour.
        _speed -- the integer, the vehicle speed, set when calling the 'move' method,
         indicated in kilometers per hour.
        __mileage -- the integer, the vehicle mileage in kilometers, increasing with use.
        _distance -- the integer, the distance to which the vehicle should move in kilometers,
        set when calling the 'move' method."""

        self.name = name
        self._max_speed = self.valid_speed(max_speed)
        self._speed = 0
        self.__mileage = 0
        self._distance = 0

    def move(self):
        """Move the vehicle at a given speed at a given distance.

        The speed and the distance must be positive integer number."""

        if self._speed_setter():
            if self._distance_setter():
                self.__mileage += self._distance
                print(f"You drove {self._distance} kilometers at a speed of {self._speed}"
                      f" kilometers per hour."
                      f"The mileage of {self.name} is {self.__mileage} kilometers")
                self._distance = 0
                self._speed = 0
                return True
            return self.move()
        return self.move()

    def _speed_setter(self):
        """Request, check and set the speed for transport.
        Speed is specified in kilometers per hour and must be a positive integer"""

        speed = input("Please enter the speed with which you are going to drive ")
        if speed.isdigit():
            speed = int(speed)
            if speed == 0:
                print("You cannot move your speed is 0 (need change speed)")
                return self._speed_setter()
            if speed < 0:
                print("The specified speed must be positive")
                return self._speed_setter()
            if speed > self._max_speed:
                self._speed = self._max_speed
                print(f"{self.name} vehicle can travel at a maximum speed of"
                      f" {self._max_speed} kilometers per hour,"
                      f" so this value has been set")
                return True
            self._speed = speed
            print(f"Specified speed for {self.name} is {self._speed} kilometers per hour")
            return True
        print("Speed must be positive integer")
        return self._speed_setter()

    def _distance_setter(self):
        """Request, check and set the distance for travel.
        Distance is specified in kilometers and must be a positive integer"""

        distance = input("Please enter the distance you are going to drive ")
        if distance.isdigit():
            distance = int(distance)
            if distance == 0:
                print("You cannot move your distance is 0")
                return self._distance_setter()
            if distance < 0:
                print("The specified distance must be positive integer")
                return self._distance_setter()
            self._distance = distance
            print(f"Your specified distance is {self._distance} kilometers")
            return True
        print("Distance must be positive integer")
        return self._distance_setter()

    @property
    def mileage(self):
        """Returns vehicle mileage in kilometers."""
        return self.__mileage

    @mileage.setter
    def mileage(self, kilometers):
        """Doesn't allow to change the mileage of the vehicle (this is illegal)"""
        self.__mileage += kilometers

    @mileage.deleter
    def mileage(self):
        """Doesn't allow to change the mileage of the vehicle (this is illegal)"""
        print(f"You can't dropped the mileage, mileage of the {self.name} is "
              f"{self.mileage} kilometers")

    @staticmethod
    def how_long_drive(distance, speed):
        """Allows you to calculate the duration of your trip.
        Returns the expected duration of the trip"""
        if isinstance(distance, int) and distance > 0 and isinstance(speed, int) and speed > 0:
            print(f"The trip will take {distance / speed} hours")
            return int(distance / speed)
        print("Distance and speed specified must be a positive integer.")
        return None

    def __add__(self, other):
        if not isinstance(other, Coach):
            raise ArithmeticError("Other operand is not instance Coach class")
        print(f"The total mileage of two vehicles is {self.mileage + other.mileage} kilometers")
        return self.mileage + other.mileage

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.name
        print(f"{self.name} have  not so attribute with name {name}")
        raise AttributeError

    def __sub__(self, other):
        if not isinstance(other, Coach):
            raise AttributeError
        print(f"The difference in mileage between the {self.name} and"
              f" the {other.name} is {self.mileage - other.mileage} kilometers")
        return self.mileage - other.mileage

    def __eq__(self, other):
        if not isinstance(other, Coach):
            raise AttributeError
        if self.mileage == other.mileage:
            return True
        return False

    def __gt__(self, other):
        if not isinstance(other, Coach):
            raise AttributeError
        if self.mileage > other.mileage:
            return True
        return False


class Engine(ABC):
    """A class for expanding classes of the 'transport' type.
    Increases the speed of vehicles, but periodically repairs are required."""

    def __init__(self, resource):
        """The initializer for the class.

        Arguments:
        _resource -- the integer, the resource is set in kilometers, is consumed during the
        operation of the vehicle and can be restored using the "repair" method."""
        self._resource = resource

    @abstractmethod
    def repair(self):
        """Restores engine life to its starting level."""

    def get_resource(self):
        """Returns the amount of remaining engine life in kilometers."""
        return self._resource


class Car(Coach, Engine):
    """The creation of the Car object and related functionality"""

    def __init__(self, name: str, max_speed: int, resource: int):
        """The initializer for the class.

        Arguments:
        name -- the string representing the vehicle's name (what the owner called coach).
        _max_speed -- the integer, the maximum speed of this vehicle,
        indicated in kilometers per hour.
        _speed -- the integer, the vehicle speed, set when calling the 'move' method,
         indicated in kilometers per hour.
        __mileage -- the integer, the vehicle mileage in kilometers, increasing with use.
        _distance -- the integer, the distance to which the vehicle should move in kilometers,
        set when calling the 'move' method.
        _resource - the integer, the resource is set in kilometers, is consumed during the
        operation of the vehicle and can be restored using the "repair" method.
        _full_resource - the integer, set in kilometers, used to store the initial
        resource of the vehicle."""

        super().__init__(name, max_speed)
        Engine.__init__(self, resource)
        self._full_resource = resource

    def move(self):
        """Move the vehicle"""

        self._speed_setter()
        self._distance_setter()
        if self.check_resource():
            self.mileage = self._distance
            self._resource -= self._distance
            print(f"You drove {self._distance} kilometers at a speed of {self._speed} "
                  f"kilometers per hour. Vehicle mileage is {self.mileage} kilometers")
            self._distance = 0
            self._speed = 0
            return True
        return self.move()

    def check_resource(self):
        """Checks if there is enough engine resource to travel a given path."""

        if self._distance > self._full_resource:
            print(f"You should split your trip into smaller parts with planned repairs,"
                  f" the maximum possible path is {self._full_resource} kilometers")
            return False
        if self._resource < self._distance:
            print(f"Engine needs repairs before drive, engine resource is {self._resource}")
            i = input("For repair engine enter 1, else 2")
            if i.isdigit():
                if int(i) == 1:
                    self.repair()
                    return True
                if int(i) == 2:
                    return False
                print("Please choose 1 or 2")
                return self.check_resource()
        return True

    def repair(self):
        """Restores engine life to its starting level."""

        self._resource = self._full_resource
        print("Engine was repaired")
        return True


class Boat(Coach):
    """The creation of the Boat object and related functionality.
    __MAX_PERMISSIBLE_SPEED_WATER - the integer, class attribute,
    the maximum permissible speed on the water for the movement
    of all surface vehicles, set in kilometers per hour"""

    __MAX_PERMISSIBLE_SPEED_WATER = 80

    def __init__(self, name, max_speed):
        """The initializer for the class.

        Arguments:
        name -- the string representing the vehicle's name (what the owner called coach).
        _max_speed -- the integer, the maximum speed of this vehicle,
        indicated in kilometers per hour.
        _speed -- the integer, the vehicle speed, set when calling the 'move' method,
         indicated in kilometers per hour.
        __mileage -- the integer, the vehicle mileage in kilometers, increasing with use.
        _distance -- the integer, the distance to which the vehicle should move in kilometers,
        set when calling the 'move' method."""

        self._max_speed = self.valid_speed_water(max_speed)
        Coach.__init__(self, name, self._max_speed)

    @classmethod
    def valid_speed_water(cls, preset_speed: int):
        """Checks compliance with the speed limit for a given class of vehicles.
        And sets the speed of the vehicle not higher than the maximum permissible."""
        if preset_speed > cls.__MAX_PERMISSIBLE_SPEED_WATER:
            print(
                f"Maximum permissible speed on water for {cls.__name__}"
                f" is {cls.__MAX_PERMISSIBLE_SPEED_WATER} kilometers per hour,"
                f" so your top speed on water will be "
                f"{cls.__MAX_PERMISSIBLE_SPEED_WATER} kilometers per hour")
            return cls.__MAX_PERMISSIBLE_SPEED_WATER
        return preset_speed


class AmphibiousCar(Boat, Car):
    """The creation of the Boat object and related functionality."""

    def __init__(self, name: str, max_speed: int, resource: int, max_speed_water):
        """The initializer for the class.

        Arguments:
        name -- the string representing the vehicle's name (what the owner called coach).
        _max_speed -- the integer, the maximum speed of this vehicle,
        indicated in kilometers per hour.
        _speed -- the integer, the vehicle speed, set when calling the 'move' method,
         indicated in kilometers per hour.
        __mileage -- the integer, the vehicle mileage in kilometers, increasing with use.
        _distance -- the integer, the distance to which the vehicle should move in kilometers,
        set when calling the 'move' method.
        _full_resource - the integer, set in kilometers, used to store the initial
        resource of the vehicle.
        _max_speed_water - an integer, the maximum speed while driving this vehicle,
        indicated in kilometers per hour.
        _max_speed_ground - the integer, set in kilometers per hour, used to store the initial
        _max_speed of the vehicle."""

        super().__init__(name, max_speed_water)
        self._max_speed_water = self._max_speed
        Car.__init__(self, name, max_speed, resource)
        self._max_speed_ground = self._max_speed

    def move(self):
        answer = input("Will you navigate on water or land? For water enter 1, for land enter 2")
        if answer.isdigit():
            if int(answer) == 1:
                self._max_speed = self._max_speed_water
                Car.move(self)
                self._max_speed = self._max_speed_ground
                return True
            if int(answer) == 2:
                Car.move(self)
                return True
            print("Please enter 1 or 2")
            return self.move()
        print("Please enter 1 or 2")
        return self.move()


if __name__ == '__main__':
    boat5 = Boat("boat5", 200)
    boat5.move()

    amf5 = AmphibiousCar("amf5", 200, 1000, 100)
    amf5.move()

    print(boat5 - amf5)
    print(boat5 == amf5)
    print(boat5 > amf5)
    print(boat5 + amf5)
    print(boat5.rev)
