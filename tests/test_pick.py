from rich._pick import pick_bool


def test_pick_bool():
    assert pick_bool(False) == False
    assert pick_bool(True) == True
    assert pick_bool(None) == False
    assert pick_bool(False, True) == False
    assert pick_bool(None, True) == True
    assert pick_bool(True, None) == True
    assert pick_bool(False, None) == False
    assert pick_bool(None, None) == False
    assert pick_bool(None, None, False, True) == False
    assert pick_bool(None, None, True, False) == True
