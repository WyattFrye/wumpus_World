import pytest
import wumpus_Final as wf

def setup_module(module):
    """Setup map and entities before tests."""
    wf.generate_base_map()
    wf.place_wumpus()

def test_base_map_dimensions():
    assert wf.base_map is not None
    assert len(wf.base_map) == wf.size
    assert all(len(row) == wf.size for row in wf.base_map)

def test_wumpus_placement():
    assert wf.wumpus_x is not None and wf.wumpus_y is not None
    assert wf.base_map[wf.wumpus_y][wf.wumpus_x] == 1

def test_is_near_pit():
    assert callable(wf.is_near_pit)

def test_is_near_bats():
    assert callable(wf.is_near_bats)

def test_valid_base_map_structure():
    assert all(isinstance(row, list) for row in wf.base_map)

def test_map_cell_values():
    assert all(all(isinstance(cell, int) for cell in row) for row in wf.base_map)
