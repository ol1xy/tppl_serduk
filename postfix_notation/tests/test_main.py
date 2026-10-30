import sys
import pytest 
from src.main import main

def test_main_no_arguments(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["main.py"])

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 1

    captured = capsys.readouterr()
    assert "Ошибка: пожалуйста, введите выражение в скобках" in captured.out


