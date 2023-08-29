from project import check_stability


def test_check_stability():
    assert check_stability(5, 3, 4) == False
