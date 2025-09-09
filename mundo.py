import random
import math

class Mundo:
    def __init__(self, n=4, qtd_pocos=None):
        self.n = n
        if qtd_pocos is None:
            qtd_pocos = max(1, n-1)
        self.matriz = [["-" for _ in range(n)] for _ in range(n)]
        self.pocos = []

        tentativas = 0
        while len(self.pocos) < qtd_pocos and tentativas < 100:
            x,y = random.randint(0, n-1), random.randint(0, n-1)
            if (self.matriz[x][y] == "-" and (x,y) != (0,0) and
                self._distancia_minima((x,y), 1.5)):
                self.matriz[x][y] = "P"
                self.pocos.append((x,y))
            tentativas += 1

        self.colocar_elemento("O", evitar=self.pocos +[(0,0)])
        self.colocar_elemento("W", evitar=self.pocos +[(0,0)])

    def _distancia_minima(self, posicao, distancia_min):
        for poco in self.pocos:
            if math.dist(posicao, poco) < distancia_min:
                return False
        return True

    def colocar_elemento(self, elemento, evitar=[]):
        while True:
            x = random.randint(0, self.n - 1)
            y = random.randint(0, self.n - 1)
            if self.matriz[x][y] == "-" and (x, y) != (0, 0) and (x, y) not in evitar:
                self.matriz[x][y] = elemento
                break