from gui import App

def test_check_stability():
    assert App.check_stability(5, 3, 4) == True
    assert App.check_stability(5, 2, 4) == False
    assert App.check_stability(19, 3, 11) == True
    assert App.check_stability(15, 4, 9) == True
    assert App.check_stability(9, 3, 6) == True
    assert App.check_stability(12, 3, 8) == False
    assert App.check_stability(10, 3, 6) == True
