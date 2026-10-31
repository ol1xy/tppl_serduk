import sys
import math

class StackMachine:

    def __init__(self):
        self.stack = []


    def _add(self, a, b):
        return a + b

    def _sub(self, a, b):
        return a - b

    def _mul(self, a, b):
        return a * b

    def _div(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Деление на 0 невозможно")
        return a / b

    def _til(self, a, b):
        if a and b:
            return abs(a-b)
        
        else:
            total  = sum(self.stack) + a + b
            total **= 2
            self.stack.clear()
            return  total
        


    def evaluate(self, expression: str):

        self.stack = []
        tokens = expression.split()
        if not tokens:                                                                                                       
            raise ValueError("Выражение не должно быть пустым")
    
        operations = {                                                                                                       
            "+": self._add,                                                                                                  
            "-": self._sub,                                                                                                  
            "*": self._mul,                                                                                                  
            "/": self._div,                                                                                                  
            "~": self._til,                                                                                                
        }   

        for item in tokens:
            if item in operations:
                if len(self.stack) < 2:
                    raise ValueError(f"Недостаточно операндов для операции '{item}'")
                b = self.stack.pop()
                a = self.stack.pop()

                result = operations[item](a, b)
                self.stack.append(result)

            else:
                num = float(item)
                if math.isnan(num) or math.isinf(num):
                    raise ValueError("Недопустимое значение")
                
                self.stack.append(num)
            print(f"Стек: {self.stack}")  
                                                                                                                         
        if len(self.stack) != 1:                                                                                             
            raise ValueError("Некорректное выражение: в стеке остались лишние числа")     

        result = self.stack.pop()
        if result.is_integer():
            result = int(result)

        return result
            


def main():

    if len(sys.argv) < 2:
        print("Ошибка: пожалуйста, введите выражение в кавычках")
        sys.exit(1)
    
    string = sys.argv[1]

    machine = StackMachine()

    try:                                                                                                             
        result = machine.evaluate(string)                                                                            
        print(f"{string} = {result}")  

    except (ValueError, ZeroDivisionError) as e:
        print(f"Ошибка в выражении: {e}")
        sys.exit(1)  


if __name__ == "__main__": #pragma: no cover
    main()