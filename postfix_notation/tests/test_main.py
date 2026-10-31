import sys
import pytest 
from src.main import StackMachine, main

def test_main_no_arguments(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["main.py"])

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 1

    captured = capsys.readouterr()
    assert "Ошибка: пожалуйста, введите выражение в кавычках" in captured.out


def test_zero_division(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["main.py", "11 0 /"])
    
    with pytest.raises(SystemExit) as exc_info:
        main()
    
    assert exc_info.value.code == 1
    
    captured = capsys.readouterr()
    assert "Деление на 0 невозможно" in captured.out


def test_operands_lack(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["main.py", "14 +"])
    
    with pytest.raises(SystemExit) as exc_info:
        main()
    
    assert exc_info.value.code == 1
    
    captured = capsys.readouterr()
    assert "Недостаточно операндов" in str(captured.out)                                                           
    assert "'+'" in str(captured.out)  


def test_evaluation_out(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["main.py", "1 2 + 4 3 * +"])
    main()

    captured = capsys.readouterr()
    assert "1 2 + 4 3 * + = 15" in captured.out
    
    

@pytest.mark.parametrize("expression, expected",
                         [("2 3 +", 5),
                          ("10 2 /", 5),
                          ("3 0 4 ~ 2 ~", 47),
                          ("2 2 + 4 - 4 ~ 2 3 * +", 22)
                         ])
def test_math_operations(expression, expected):
    machine = StackMachine()
    assert machine.evaluate(expression) == expected
