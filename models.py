"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in TASK-1.
"""
from helpers import cd_to_datetime, datetime_to_str
import math
import datetime


class NearEarthObject:
    """Represents a near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such as:
    - Primary designation (required, unique)
    - IAU name (optional)
    - Diameter in kilometers (optional - sometimes unknown)
    - Potentially hazardous status (boolean)

    Attributes:
        designation (str): The primary designation of the NEO.
        name (str): The IAU name of the NEO (default: None).
        diameter (float): The diameter of the NEO in kilometers (default: float('nan')).
        hazardous (bool): Whether the NEO is potentially hazardous to Earth.
        approaches (list): A collection of close approaches of the NEO (default: empty list).

    Methods:
        __init__(self, designation, name=None, diameter=float('nan'), hazardous=False):
            Initializes a new NearEarthObject with the given attributes.

    A `NearEarthObject` maintains a collection of its close approaches, which is
    initialized to an empty list. The `approaches` attribute can be populated with
    `CloseApproach` objects in the `NEODatabase` constructor or through other means."""

    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self.designation = info.get("designation")
        self.name = info.get("name")
        self.diameter = info.get("diameter")
        if not self.diameter:
            self.diameter = float("nan")
        self.hazardous = info.get("hazardous")

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a full name representation of this NEO."""
        return f"{self.designation} ({self.name})" if self.name else f"{self.designation}"

    def __str__(self):
        """Return `str(self)`."""
        hazardous_status = "is" if self.hazardous else "is not"
        if not math.isnan(self.diameter):
            return (
                f"NEO {self.fullname} has a diameter of {self.diameter:.3f} km "
                f"and {hazardous_status} potentially hazardous."
            )
        return f"NEO {self.fullname} {hazardous_status} potentially hazardous."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
                f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})")

    def serialize(self):
        """Return a dictionary representation of self attributes.
        Returns:
            [dict]: Keys associated with attributes.
        """
        return {
            "designation": self.designation,
            "name": self.name,
            "diameter_km": self.diameter,
            "potentially_hazardous": self.hazardous,
        }


class CloseApproach:
    """
    Represents a close approach to Earth by a near-Earth object (NEO).

    A `CloseApproach` encapsulates information about the NEO's close approach to Earth, such as:
    - Date and time (in UTC) of the closest approach
    - Nominal approach distance in astronomical units
    - Relative approach velocity in kilometers per second

    Attributes:
        _designation (str): The primary designation of the NEO.
        time (datetime): The date and time (in UTC) of the closest approach.
        distance (float): The nominal approach distance in astronomical units.
        velocity (float): The relative approach velocity in kilometers per second.
        neo (NearEarthObject): The `NearEarthObject` making the close approach.

    Methods:
        __init__(self, designation, time, distance, velocity):
            Initializes a new CloseApproach with the given attributes.

        serialize(self):
            Serializes the CloseApproach object to a JSON-compatible dictionary.

    Initially, the `CloseApproach` stores the primary designation of the NEO in a private
    attribute `_designation`. The `neo` attribute is set to None until it is replaced with
    the actual `NearEarthObject` instance in the `NEODatabase` constructor.

    """

    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dict of keyword arguments used to the constructor.
        """
        self._designation = info.get("designation")
        self.time = info.get("time")
        if self.time:
            self.time = cd_to_datetime(self.time)
            assert isinstance(self.time, datetime.datetime), "Date must be a datetime object"
        self.distance = info.get("distance", float("nan"))
        self.velocity = info.get("velocity", float("nan"))

        assert isinstance(self.distance, float), "Distance must be a float object"
        assert isinstance(self.velocity, float), "Velocity must be a float object"

        # Create an attribute for the referenced NEO, originally None.
        self.neo = info.get("neo")

    @property
    def designation(self):
        """Get designation information
        Returns:
            [str]: Returns self._designation
        """
        return self._designation

    @property
    def time_str(self):
        """ Returns a formatted string representation of the approach time.

            The approach time is stored in the `self.time` attribute as a Python `datetime` object.
            However, the default string representation of a `datetime` object includes seconds,
            which are not present in the input data set.

            This method converts the `datetime` object to a formatted string that omits the seconds
            and can be used for human-readable representations and serialization to CSV and JSON files.

            Returns:
                str: A formatted string representation of the approach time, in the format:
                     'YYYY-MM-DD HH:MM'.
        """
        if self.time:
            return datetime_to_str(self.time)
        return "an unknown time"

    def __str__(self):
        """Return `str(self)`."""
        return f"At {self.time_str}, '{self.neo.fullname}' approaches Earth at a distance of {self.distance:.2f} au and a velocity of \
                {self.velocity:.2f} km/s."

    def __repr__(self):
        """Return `repr(self)`, a machine-readable string representation of this object."""
        return (f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")

    def serialize(self):
        """Return a dictionary representation of self attributes.
        Returns:
            [dict]: Keys associated with self attributes.

        """
        return {
            "datetime_utc": datetime_to_str(self.time),
            "distance_au": self.distance,
            "velocity_km_s": self.velocity,
        }
