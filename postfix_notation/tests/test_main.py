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


def test_StackMachine_simple_addition():
    machine = StackMachine()
    assert machine.evaluate("2 3 +") == 5

def test_assignment_examples():                                                                                      
    machine = StackMachine()                                                                                         
    assert machine.evaluate("3 0 4 ~ 2 ~") == 47                                                                     
    assert machine.evaluate("2 2 + 4 - 4 ~ 2 3 * +") == 22