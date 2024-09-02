class Ordenadora():
    def __init__(self, listaBaguncada):
        self.listaBaguncada = listaBaguncada
    
    def _bubble_sort(self):
        n = len(self.listaBaguncada)
        for i in range(n):
            for j in range(0, n-i-1):
                if self.listaBaguncada[j] > self.listaBaguncada[j+1]:
                    self.listaBaguncada[j], self.listaBaguncada[j+1] = self.listaBaguncada[j+1], self.listaBaguncada[j]

    def ordenacaoCrescente(self):
        self._bubble_sort()
        return self.listaBaguncada
    
    def ordenacaoDecrescente(self):
        self._bubble_sort()
        return self.listaBaguncada[::-1]