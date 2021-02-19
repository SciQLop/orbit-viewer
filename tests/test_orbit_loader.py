#!/usr/bin/env python3

import datetime as dt

from orbit_viewer.orbit_loader import OrbitLoader

import spwc


def test_get_orbit_mms1_1_hours_sanity_check(qtbot):
    s = OrbitLoader('mms1')

    def __slot(var: spwc.SpwcVariable):
        assert len(var.time) == 60
        assert var.data.shape == (60, 6)

    def __error():
        assert 0

    s.done.connect(__slot)
    s.error.connect(__error)

    with qtbot.waitSignal(s.done, timeout=5000):
        r = (dt.datetime.now() - dt.timedelta(hours=1), dt.datetime.now())
        s.get_orbit(r[0], r[1])

    with qtbot.waitSignal(s.finished):
        s.quit()


def test_error_unknown_product(qtbot):
    s = OrbitLoader('surely_not_existing')

    with qtbot.waitSignal(s.error, timeout=5000):
        r = (dt.datetime.now() - dt.timedelta(hours=1), dt.datetime.now())
        s.get_orbit(r[0], r[1])

    with qtbot.waitSignal(s.finished):
        s.quit()


def test_invalid_time_range_empty_orbit(qtbot):
    s = OrbitLoader('mms1')

    def __slot(var: spwc.SpwcVariable):
        assert len(var.time) == 0

    def __error():
        assert 0

    s.done.connect(__slot)
    s.error.connect(__error)

    with qtbot.waitSignal(s.done, timeout=5000):
        r = (dt.datetime.now() + dt.timedelta(hours=1), dt.datetime.now())
        s.get_orbit(r[0], r[1])

    with qtbot.waitSignal(s.finished):
        s.quit()
