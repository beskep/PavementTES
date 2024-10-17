from __future__ import annotations

import pytest
from hypothesis import given
from hypothesis import strategies as st

from ptes import calculate as cal

positive = st.floats(min_value=0, exclude_min=True)
ratio = st.floats(min_value=0, max_value=1, exclude_min=True)


@given(
    st.from_type(cal.Material),
    st.from_type(cal.Material),
    st.from_type(cal.Environment),
    st.from_type(cal.Design),
)
def random_calculate(
    water: cal.Material,
    sand: cal.Material,
    environment: cal.Environment,
    design: cal.Design,
):
    # https://docs.pydantic.dev/latest/integrations/hypothesis/
    # We are temporarily removing the Hypothesis plugin in favor of studying
    # a different mechanism. For more information, see the issue
    # annotated-types/annotated-types#37.
    pt = cal.PavementTES()
    pt.water = water
    pt.sand = sand
    pt.env = environment

    pt.calculate(design.model_dump())


@given(
    st.tuples(positive, positive, ratio, ratio),
    st.tuples(positive, positive, ratio, ratio),
    st.tuples(positive, positive),
    st.tuples(ratio, positive, positive, st.integers(min_value=0, max_value=2)),
)
def test_random_calculation(water, sand, env, design):
    pt = cal.PavementTES()
    pt.water = cal.Material(
        cp=water[0],
        rho=water[1],
        porosity=water[2],
        efficiency=water[3],
    )
    pt.sand = cal.Material(
        cp=sand[0],
        rho=sand[1],
        porosity=sand[2],
        efficiency=sand[3],
    )
    pt.env = cal.Environment(delta_temperature=env[0], daily_radiation=env[1])
    pt.calculate(
        dict(zip(['efficiency', 'duration', 'area', 'material'], design, strict=True))
    )


@pytest.mark.parametrize(
    ('efficiency', 'duration', 'area', 'capacity'),
    [
        (35, 60, 40, 51.6),
        (35, 90, 40, 77.4),
        (35, 120, 40, 103.2),
        (25, 60, 30, 27.64285714),
        (25, 90, 30, 41.46428571),
        (25, 120, 30, 55.28571429),
        (15, 60, 20, 11.05714286),
        (15, 90, 20, 16.58571429),
        (15, 120, 20, 22.11428571),
    ],
)
def test_water(efficiency, duration, area, capacity):
    pt = cal.PavementTES()
    pt.water = pt.water.model_validate({
        'cp': 4.2,
        'rho': 1000,
        'porosity': 0.5,
        'efficiency': 0.5,
    })
    pt.env = pt.env.model_validate({'delta_temperature': 30, 'daily_radiation': 4.3})

    a = pt.calculate({
        'efficiency': efficiency / 100.0,
        'duration': duration,
        'area': area,
        'material': 0,
    })

    assert a.capacity == pytest.approx(capacity)


@pytest.mark.parametrize(
    ('efficiency', 'duration', 'area', 'capacity'),
    [
        (35, 60, 40, 240.8),
        (35, 90, 40, 361.2),
        (35, 120, 40, 481.6),
        (25, 60, 30, 129),
        (25, 90, 30, 193.5),
        (25, 120, 30, 258),
        (15, 60, 20, 51.6),
        (15, 90, 20, 77.4),
        (15, 120, 20, 103.2),
    ],
)
def test_sand(efficiency, duration, area, capacity):
    pt = cal.PavementTES()
    pt.sand = pt.sand.model_validate({
        'cp': 0.9,
        'rho': 2000,
        'porosity': 0.5,
        'efficiency': 0.5,
    })
    pt.env = pt.env.model_validate({'delta_temperature': 30, 'daily_radiation': 4.3})

    a = pt.calculate({
        'efficiency': efficiency / 100.0,
        'duration': duration,
        'area': area,
        'material': 1,
    })

    assert a.capacity == pytest.approx(capacity)


@pytest.mark.parametrize(
    ('efficiency', 'duration', 'area', 'capacity'),
    [
        (35, 60, 40, 46.60645161),
        (35, 90, 40, 69.90967742),
        (35, 120, 40, 93.21290323),
        (25, 60, 30, 24.96774194),
        (25, 90, 30, 37.4516129),
        (25, 120, 30, 49.93548387),
        (15, 60, 20, 9.987096774),
        (15, 90, 20, 14.98064516),
        (15, 120, 20, 19.97419355),
    ],
)
def test_water_and_sand(efficiency, duration, area, capacity):
    pt = cal.PavementTES()
    pt.water = pt.water.model_validate({
        'cp': 4.2,
        'rho': 1000,
        'porosity': 0.5,
        'efficiency': 0.5,
    })
    pt.sand = pt.sand.model_validate({
        'cp': 0.9,
        'rho': 2000,
        'porosity': 0.5,
        'efficiency': 0.5,
    })
    pt.env = pt.env.model_validate({'delta_temperature': 30, 'daily_radiation': 4.3})

    a = pt.calculate({
        'efficiency': efficiency / 100.0,
        'duration': duration,
        'area': area,
        'material': 2,
    })

    assert a.capacity == pytest.approx(capacity)
