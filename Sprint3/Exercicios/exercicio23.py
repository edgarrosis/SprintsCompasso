class Calculo():
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def soma(self):
        resultado = self._x + self._y
        return print(f"Somando: {self._x}+{self._y} = {resultado}")
    
    def subtrai(self):
        resultado = self._x - self._y
        return print(f"Somando: {self._x}-{self._y} = {resultado}")