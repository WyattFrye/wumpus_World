
from wumpus_Final import (
    generate_base_map,
    is_near_pit,
    is_near_wumpus,
    is_near_bats,
    pits,
    bats,
    player_x,
    player_y,
)

def setup_module(module):
    """Setup map and entities once before tests."""
    generate_base_map()

def test_pits_not_on_player():
    assert all((x, y) != (player_x, player_y) for (x, y) in pits)

def test_bats_not_on_player():
    assert all((x, y) != (player_x, player_y) for (x, y) in bats)

def test_is_near_pit_returns_bool():
    assert isinstance(is_near_pit(player_x, player_y), bool)

def test_is_near_wumpus_returns_bool():
    assert isinstance(is_near_wumpus(player_x, player_y), bool)

def test_is_near_bats_returns_bool():
    assert isinstance(is_near_bats(player_x, player_y), bool)
