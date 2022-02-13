import plotly.graph_objects as go
from dataclasses import dataclass, field
from typing import List, Tuple
from parameters import *


@dataclass
class Parameter:
    """Parameter used for decision making

    Args:
        value (float):                  Value of the parameter
        is_increasing_better (bool):    True if the parameter is better if its value is increasing
        unit(str):                      Unit of the parameter
        name (str):                     Name of the parameter
        range (Tuple[int]):             Range of the parameter
        weight (float):                 Weight of the parameter (0, 1)
        normalized_value (float):       Normalized value of the parameter

    Raises:
        ValueError: range is not valid
        ValueError: value is not valid
        ValueError: weight is not valid
    """
    value: int
    is_increasing_better: bool = True
    unit: str = ""
    name: str = ""
    range: Tuple[int] = None
    weight: float = 1.0  # From 0 to 1
    normalized_value: int = 0

    def __post_init__(self):
        if self.range is not None and self.range[1] <= self.range[0]:
            raise ValueError("Parameter {} range {} is not valid".format(self.name, self.range))

        if self.range is not None and (self.value < self.range[0] or self.value > self.range[1]):
            raise ValueError("Parameter {} value is not valid: value {} not in range {}".format(
                self.name, self.value, self.range))

        if self.weight > 1.0:
            raise ValueError("Parameter {} weight is not valid: weight {} is not in range 0 to 1".format(
                self.name, self.weight))

    def normalize(self, min_value, max_value):
        if self.range is not None:
            min_value = self.range[0]
            max_value = self.range[1]
        denominator = max_value - min_value
        if denominator == 0:
            self.normalized_value = 0
            return
        self.normalized_value = (self.value - min_value) / (max_value - min_value)
        if not self.is_increasing_better:
            self.normalized_value = 1 - self.normalized_value

    def calculate_weighted_value(self):
        return round(self.normalized_value * self.weight, 2)


K = 1000


class Price(Parameter):
    """Parameter which reflects a price

    Args:
        value (float):                  Value of the parameter
        weight (float):                 Weight of the parameter (0, 1)
    """

    def __init__(self, value, weight=1.0):
        super().__init__(value, is_increasing_better=False, unit="euro", name="price", range=price_range, weight=weight)


class Area(Parameter):
    def __init__(self, value, weight=1.0):
        super().__init__(value, is_increasing_better=True, unit="sqm", name="area", range=area_range, weight=weight)


class Year(Parameter):
    def __init__(self, value, weight=1.0):
        super().__init__(value, is_increasing_better=True, unit="year", name="year", range=year_range, weight=weight)


class Vastike(Parameter):
    def __init__(self, value, weight=1.0):
        super().__init__(value, is_increasing_better=False, unit="euro", name="vastike", range=vastike_range, weight=weight)


class Floor(Parameter):
    def __init__(self, value, weight=1.0):
        super().__init__(value, is_increasing_better=True, unit="", name="floor", range=floor_range, weight=weight)


class Rooms(Parameter):
    def __init__(self, value, weight=1.0):
        super().__init__(value, is_increasing_better=True, unit="", name="rooms", range=rooms_range, weight=weight)


class Zone(Parameter):
    def __init__(self, value: str):
        value = value.lower()
        numerical_value = 0
        if(zone_weights.get(value) is not None):
            numerical_value = zone_weights[value]

        super().__init__(numerical_value, is_increasing_better=True, unit="", name="zone", range=zone_range)


@dataclass
class Apartment:
    """Apartment class which stores all relevant parameters for an apartment
    """
    categories = ["price", "area", "year", "vastike", "floor", "rooms", "zone"]

    name: str

    price: Price
    area: Area
    year: Year
    vastike: Vastike
    floor: Floor
    rooms: Rooms
    zone: Zone

    url: str = ""

    parameters: List[Parameter] = None

    def __post_init__(self):
        self.update_parameters()

    def update_parameters(self):
        self.parameters = [self.price, self.area, self.year, self.vastike, self.floor, self.rooms, self.zone]

    def get_values(self):
        return [p.normalized_value for p in self.parameters]

    def calculate_weighted_value(self):
        return sum([p.calculate_weighted_value() for p in self.parameters])

    def __str__(self) -> str:
        return "Apartment: {} Price: {} Area: {} Year: {} Vastike: {} Floor: {} Rooms: {} Zone: {}".format(self.name,
                                                                                                           self.price.value,
                                                                                                           self.area.value,
                                                                                                           self.year.value,
                                                                                                           self.vastike.value,
                                                                                                           self.floor.value,
                                                                                                           self.rooms.value,
                                                                                                           self.zone.value)


@dataclass
class Apartments:
    apartments: List[Apartment] = None

    def __post_init__(self):
        self.normalize()

    def normalize(self):
        n_parameters = len(self.apartments[0].parameters)
        for i in range(n_parameters):
            self.__normalizeParameters([apartment.parameters[i] for apartment in self.apartments])

    def __normalizeParameters(self, parameters: List[Parameter]):
        max_value = max(parameter.value for parameter in parameters)
        min_value = min(parameter.value for parameter in parameters)

        for parameter in parameters:
            parameter.normalize(min_value, max_value)

    def plot(self):
        self.apartments.sort(key=lambda a: a.calculate_weighted_value(), reverse=True)

        categories = Apartment.categories
        fig = go.Figure()
        for i, a in enumerate(self.apartments):
            if i > number_of_apartments_to_plot - 1:
                break
            fig.add_trace(go.Scatterpolar(
                r=a.get_values(),
                theta=categories,
                fill='toself',
                hoveron='points+fills',
                name=a.name
            ))

        fig.update_layout(polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
            showlegend=False
        )

        fig.show()

    def rank(self):
        self.apartments.sort(key=lambda a: a.calculate_weighted_value(), reverse=True)
        for i in range(len(self.apartments)):
            if i > number_of_apartments_to_rank - 1:
                break
            ranking = i + 1
            score = self.apartments[i].calculate_weighted_value()
            name = self.apartments[i].name
            url = self.apartments[i].url
            print("{}. Name: {}, Score: {:0.2f}, Url: {}".format(
                ranking, name, score, url))
