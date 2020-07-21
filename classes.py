class vetor():
    def __init__(self, coords):
        self.coords = coords[:]
        self.dimensao = len(self.coords)

    def __getitem__(self, val):
        if isinstance(val, int):
            return self.coords[val]
        else:
            return vetor(self.coords[val])
    
    def __setitem__(self, ind, val):
        self.coords[ind] = val
    
    def __add__(self, vet):
        novas_coords = self.coords[:]
        for i in range(len(vet)):
            novas_coords[i] += vet[i]
        return vetor(novas_coords)

    def __mul__(self, val):
        novas_coords = self.coords[:]
        for i in range(len(novas_coords)):
            novas_coords[i] *= val
        return vetor(novas_coords)
    
    def __rmul__(self, val):
        novas_coords = self.coords[:]
        for i in range(len(novas_coords)):
            novas_coords[i] *= val
        return vetor(novas_coords)

    def __sub__(self, vet):
        novas_coords = self.coords[:]
        for i in range(len(vet)):
            novas_coords[i] -= vet[i]
        return vetor(novas_coords)
    
    def __len__(self):
        return self.dimensao

    def __str__(self):
        return str(tuple(self.coords))
    
    def modulo(self):
        mod = 0
        for c in self.coords:
            mod += c * c
        return mod ** (1/2)
    
    def versor(self):
        vers = self[:]
        return vers * (1 / self.modulo())
