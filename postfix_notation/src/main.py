import sys

class StackMachine:

    def __init__(self):
        self.stack = []


    def evaluate(self, expression: str) -> int:

        tokens = expression.split()

        for item in tokens:
            if item in ("+", "-", "*", "/", "~"):
                # функция для операции типа add мб которая опеределяет плюсик ли токен или че  дл
                return 0
            
            num = float(item)
            self.stack.append(num)
            




def main():

    if len(sys.argv) < 2:
        print("Ошибка: пожалуйста, введите выражение в кавычках")
        sys.exit(1)
    
    string = sys.argv[1]

    machine = StackMachine()

    try:                                                                                                             
        result = machine.evaluate(string)                                                                            
        print(f"{string} = {result}")  

    except ValueError as e:
        print(f"Ошибка в выражении: {e}")
        sys.exit(1)  

    


if __name__ == "__main__":
    main()