from project import check_stability
import pytest


def test_check_stability():
    assert check_stability(5, 3, 4) == True
    assert check_stability(5, 2, 4) == False
    assert check_stability(19, 3, 11) == True
    assert check_stability(15, 4, 9) == True
    assert check_stability(9, 3, 6) == True
    assert check_stability(12, 3, 8) == False
