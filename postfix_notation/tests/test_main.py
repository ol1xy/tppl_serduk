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


def test_operands_leck(monkeypatch, capsys):
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
    
    
def test_simple_addition():
    machine = StackMachine()
    assert machine.evaluate("2 3 +") == 5

def test_simple_division():
    machine = StackMachine()
    assert machine.evaluate("10 2 /") == 5

def test_assignment_examples():                                                                                      
    machine = StackMachine()                                                                                         
    assert machine.evaluate("3 0 4 ~ 2 ~") == 47                                                                     
    assert machine.evaluate("2 2 + 4 - 4 ~ 2 3 * +") == 22