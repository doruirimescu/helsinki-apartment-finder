import plotly.graph_objects as go
from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class Parameter:
    value: int
    is_increasing_better: bool = True
    unit: str = ""
    name: str = ""
    range: Tuple[int] = None
    weight: float = 1.0  # From 0 to 1
    normalized_value: int = 0

    def __post_init__(self):
        if self.range is not None and self.range[1] <= self.range[0]:
            raise ValueError("Range is not valid")

        if self.range is not None and (self.value < self.range[0] or self.value > self.range[1]):
            raise ValueError("Parameter {} value is not valid: value {} not in range {}".format(self.name, self.value, self.range) )

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
    def __init__(self, value, is_increasing_better=False, unit="euro", name="price", range=(100*K, 400*K)):
        super().__init__(value, is_increasing_better, unit, name, range)


class Area(Parameter):
    def __init__(self, value, is_increasing_better=True, unit="msq", name="area", range=(50, 150)):
        super().__init__(value, is_increasing_better, unit, name, range)


class Year(Parameter):
    def __init__(self, value, is_increasing_better=True, unit="year", name="year", range=(1950, 2022)):
        super().__init__(value, is_increasing_better, unit, name, range)


class Vastike(Parameter):
    def __init__(self, value, is_increasing_better=False, unit="euro", name="vastike", range=(10, 450)):
        super().__init__(value, is_increasing_better, unit, name, range)


class Floor(Parameter):
    def __init__(self, value, is_increasing_better=True, unit="", name="floor", range=(0, 10)):
        super().__init__(value, is_increasing_better, unit, name, range)


class Rooms(Parameter):
    def __init__(self, value, is_increasing_better=True, unit="", name="rooms", range=(1, 5)):
        super().__init__(value, is_increasing_better, unit, name, range)


class Zone(Parameter):
    def __init__(self, value: str, is_increasing_better=True, unit="", name="zone", range=(0, 1)):
        value = value.lower()
        numerical_value = 0
        if(value == "matinkylä"):
            numerical_value = 1
        elif(value == "leppävaara"):
            numerical_value = 1
        elif(value == "tiistilä"):
            numerical_value = 1
        elif(value == "olari"):
            numerical_value = 0.5

        super().__init__(numerical_value, is_increasing_better, unit, name, range)


@dataclass
class Apartment:
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


def normalizeParameters(parameters: List[Parameter]):
    max_value = max(parameter.value for parameter in parameters)
    min_value = min(parameter.value for parameter in parameters)

    for parameter in parameters:
        parameter.normalize(min_value, max_value)


@dataclass
class Apartments:
    apartments: List[Apartment] = None

    def __post_init__(self):
        self.normalize()

    def normalize(self):
        n_parameters = len(self.apartments[0].parameters)
        for i in range(n_parameters):
            normalizeParameters([apartment.parameters[i] for apartment in self.apartments])

    def plot(self, n = 5):
        self.rank()

        categories = Apartment.categories
        fig = go.Figure()
        for i, a in enumerate(self.apartments):
            if i > n - 1:
                break
            fig.add_trace(go.Scatterpolar(
                r=a.get_values(),
                theta=categories,
                fill='toself',
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

    def rank(self, n=10):
        self.apartments.sort(key=lambda a: a.calculate_weighted_value(), reverse=True)
        for i in range(len(self.apartments)):
            if i > n - 1:
                break
            print(f"{i+1}. Name: {self.apartments[i].name} Url: {self.apartments[i].url}")
            print(f"{self.apartments[i].calculate_weighted_value()}")
            print()
