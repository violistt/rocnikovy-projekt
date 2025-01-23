# Ročníkový projekt
## Celočíselné bázy tokového priestoru

Cieľom ročníkového projektu je pripraviť program, ktorý vypočíta
celočiselnu bázu tokového priestoru grafu nad $\mathbb{Q}$.

V zimnom semestri je cieľom implementovať greedy algoritmus, ktorý postupne
prechádza kružnice od najkratších a snaží sa ich vloziť do bázy.
Vyhodnotíme úspešnosť algoritmu.

## Externé knižnice
Program využíva externú knižnicu `numpy` na algebraické výpočty.

Inštalácia:

`pip3 install numpy`

## Unit testy
`python3 -m unittest discover -s tests -p "test.py"`
