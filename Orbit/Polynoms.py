from scipy import poly1d

p = []
p.append(poly1d([1]))
p.append(poly1d([1, 0]))

i = 2
while i < 5:
    Pol = (2 * i + 1)/(i + 1) * p[i-1] * poly1d([1, 0]) + i / (i + 1) * p[i-2]
    p.append(Pol)
    i += 1

print(p)
p[2] = p[2].deriv(2)
print(p[2])
print(poly1d([1, 0])**2**2)
