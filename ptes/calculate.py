from typing import ClassVar, Literal

from pydantic import BaseModel, Field, field_serializer

positive = Field(gt=0.0)
ratio = Field(gt=0.0, le=1.0)


class Material(BaseModel):
    cp: float = positive  # kJ/kg℃
    rho: float = positive  # kg/m³
    porosity: float = ratio
    efficiency: float = ratio  # storage efficiency


class Environment(BaseModel):
    delta_temperature: float = positive  # ℃
    daily_radiation: float = positive  # kWh/m²·day


class Design(BaseModel):
    efficiency: float = ratio
    duration: float = positive  # 일
    area: float = positive  # m²
    material: Literal[0, 1, 2]  # 물, 모래, 물+모래

    MATERIALS: ClassVar[tuple[str, str, str]] = ('물', '모래', '물+모래')

    @field_serializer('efficiency')
    @staticmethod
    def _serialize_efficiency(value):
        return f'{value*100:g}%'

    @field_serializer('material')
    def _serialize_material(self, value):
        return self.MATERIALS[value]


class Capacity(Design):
    heat: float  # kJ
    tank_capacity_mass: float  # kg
    tank_capacity_volume: float  # m³
    capacity: float  # m³

    @field_serializer(
        'duration',
        'area',
        'heat',
        'tank_capacity_mass',
        'tank_capacity_volume',
        'capacity',
    )
    @staticmethod
    def _serialize_numeric(value):
        return f'{value:.4g}'


class DesignCases(BaseModel):
    cases: list[Design]


class CapacityCases(BaseModel):
    cases: list[Capacity]

    COLUMNS: ClassVar[tuple[str, ...]] = (
        '집열 효율',
        '집열 기간 (일)',
        '도로 면적 (m²)',
        '축열재',
        '축열량 (kJ)',
        '축열조 용량 (m³)',
    )
    KEYS: ClassVar[tuple[str, ...]] = (
        'efficiency',
        'duration',
        'area',
        'material',
        'heat',
        'capacity',
    )


def _weighted(m1: Material, m2: Material, field: str) -> float:
    d1 = m1.model_dump()
    d2 = m2.model_dump()
    return d1[field] * m1.porosity + d2[field] * m2.porosity


class PavementTES:
    def __init__(self) -> None:
        self._water = Material(cp=4.2, rho=1000, porosity=0.5, efficiency=0.5)
        self._sand = Material(cp=0.9, rho=2000, porosity=0.5, efficiency=0.5)
        self._env = Environment(delta_temperature=30.0, daily_radiation=4.3)

    @property
    def water(self):
        return self._water

    @water.setter
    def water(self, m: str | Material):
        if isinstance(m, str):
            m = Material.model_validate_json(m)
        self._water = m

    @property
    def sand(self):
        return self._sand

    @sand.setter
    def sand(self, m: str | Material):
        if isinstance(m, str):
            m = Material.model_validate_json(m)
        self._sand = m

    @property
    def env(self):
        return self._env

    @env.setter
    def env(self, e: Environment):
        if isinstance(e, str):
            e = Environment.model_validate_json(e)
        self._env = e

    def calculate(self, data: dict[str, float | int] | Design):
        design = data if isinstance(data, Design) else Design.model_validate(data)

        match design.material:
            case 0:
                cp = self._water.cp
                rho = self._water.rho
                efficiency = self._water.efficiency
            case 1:
                cp = self._sand.cp
                rho = self._sand.rho * self._sand.porosity
                efficiency = self._sand.efficiency
            case 2:
                cp = _weighted(self._water, self._sand, 'cp')
                rho = _weighted(self._water, self._sand, 'rho')
                efficiency = _weighted(self._water, self._sand, 'efficiency')
            case _:
                raise ValueError(design.material)

        heat = (
            3600
            * self._env.daily_radiation
            * design.efficiency
            * design.duration
            * design.area
        )
        try:
            mass = heat / (cp * self._env.delta_temperature)
        except ZeroDivisionError:
            mass = float('inf')

        try:
            volume = mass / rho
        except ZeroDivisionError:
            volume = float('inf')

        capacity = volume * efficiency

        return Capacity(
            efficiency=design.efficiency,
            duration=design.duration,
            area=design.area,
            material=design.material,
            heat=heat / 1000.0,  # kJ
            tank_capacity_mass=mass,
            tank_capacity_volume=volume,
            capacity=capacity,
        )

    def calculate_cases(self, data: str | DesignCases):
        cases = (
            data
            if isinstance(data, DesignCases)
            else DesignCases.model_validate_json(data)
        )

        return CapacityCases(cases=[self.calculate(x) for x in cases.cases])
