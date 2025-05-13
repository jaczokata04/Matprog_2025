# Bringing down the House strategy
A Blackjack szimulátor



## Blackjack vagy más néven 21

A blackjack a kaszinókban egyik legnépszerűbb játék. A játék lényege, hogy van egy osztó, és egy- vagy több játékos. Kezdetben minden játékos kap két lapot, és az osztó (vagy más néven dealer), pedig maga elé is oszt két kapot: egyet fel-, a másikat lefordítva. Ekkor a cél, hogy a játékos keze közelebb legyen a 21-hez, mint az osztóé, de ne haladja meg. A kártyák az értékük szerint: számkártyák annyit érnek, amennyi rájuk van írva, a bubi, dáma, király pedig 10-10-10 pontot érnek, és az ász 1 vagy 11-et, attól függően, hogy melyik az előnyösebb. Az osztó szabályai: 16 pontig kötelező húznia, de 17-nél vagy afelett meg kell állnia. Manapság már minden kör után visszakeverik a lapokat a pakliba, viszont régebben csak 15 lap alatt keverték vissza, és emiatt működött a következő kártyaszámlálási stratégia:

## Hi-Lo stratégia

A játék során minden kijátszott laphoz hozzárendelünk egy értéket a következő módon:

2-6: a lapok értéke legyen +1
7-9: a lapok értéke 0
10, J, Q, K, A: a lapok értéke -1.

Maga a stratégia: ahogy mennek ki a lapok, megyjegyezzük a kiment lapok értékeinek összegét. Ez az összeg a futó számláló (running count). Milyen érték jó nekünk?

A kis lapok (2-6) segítik az osztót, tehát jó, ha elfogynak. A nagy lapok (10-A) viszont a játékost segítik, mivel így nagyobb eséllyel lesz Blackjack-ünk (azaz 21 értékű kezünk), ezért jó ha sok nagy lap van még a pakliban.

Több pakli esetén kicsit változtatni kell. Itt nem a running count kell, hanem az úgynevezett true count, amit úgy kapunk meg, hogy a running count értékét elosztjuk a jelenleg bent maradt paklik számával. Ekkor, ha a játék közben a true count> 1 vagy 2, akkor érdemes nagy tétet tenni, mivel a játékosnak nagy esélye van, ha a true count <= 0, ekkor érdemesebb kis tétet rakni, vagy akár ki is hagyni a kört.

## Basic strategy
![image](https://github.com/user-attachments/assets/eac6811f-8c02-466e-9031-85312f6c3108)



## A játék menete-példa futtatás

A programunk először megkérdezi, hogy hány paklival szeretnénk játszani, a következő módon. A játékos 1-től 8-ig választhat. 
Majd a választás után a játék kiírja, hogy az adott játékban hány chippel kezdünk. Az első játék elején 100 chippünk van, majd a további játékokban, az adott egyenlegünket írja ki. Ezek mellett elindul a Hi-Lo számláló, kiírja a kezdő értéket, majd minden körben frissíti. 

```
Hány paklival szeretnél játszani? (1-8): 6
3 paklival játszol, összesen 156 kártya.
100 chippel kezdessz.
Hi-Lo kártyaszámolás bekapcsolva. Kezdő érték: 0
```
Majd miután kiválasztottad, hogy hány paklival játszanál, a program megkérdezi, hogy a pénzedből mennyit tennél fel.
```
Mennyit tennél fel? 20
```
A program a következő lépésben kiosztja a lapokat, és kiírja a játékos majd a dealer kezét, és azok értékét.
Ezután a program ajánl egy stratégiát a lapjaink, a basic strategy és a Hi-Lo számláló alapján. 
```
Hi-Lo számláló: 0 (True count: 0.0)
Tét ajánlás: Alap tét rendben van
Játékos keze: Kör Jumbó, Treff 8,
Érték: 18
Dealer (látható) keze: Kör 4,
Érték: 4
Stratégia ajánlás: Stand (Maradj)
Rendelkezésre álló opciók: [H]it / [S]tand / [D]ouble down
Mit csinálsz? s
```
Miután megkaptad a kezdő lapjaidat, 4 lehetőséged van. Hit, stand, double down vagy split. A hit azt jelenti, hogy kérsz még egy lapot, de ha ezzel túlléped a 21-et, akkor vesztettél automatikusan. A stand azt jelenti, hogy nem kérsz több lapot, ezt akkor érdemes, ha nagy értékű lapjaid vannak. A double down az azt jelenti, hogy megduplázod a tétedet, mielőtt kapsz egy új lapot. A split csak akkor opció, ha két ugyanolyan lapot kaptál kezdésnek, ekkor megduplázod a paklijaidat és ezentúl két "kézzel" játszol, ekkor a tétet is megduplázod.
Minden esetben az a végcél hogy a lapjaid értéke nagyobb legyen mint a dealer.

Mivel itt a kezünk értéke 18 és a Hi-Lo számláló 0, ezért látszik, hogy ha kérnénk lapot, akkor nagyobb valószínűséggel veszítenénk, mint nyernénk. (A program is ezt ajánlja). Ez egy példa futtatás a standre.

```
Dealer jön:
Dealer keze: Kör 4, Treff 9,
Érték: 13
Dealer húzott: Káró 8
Hi-Lo számláló: 0 (True count: 0.0)
Dealer keze: Kör 4, Treff 9, Káró 8, 
Érték: 21
Dealer nyert!
```
Ezután a dealer is megkapja a lapjait és lejátsza a körét, aminek a végén a program kiírja, hogy ki nyert.
Végül dönthetünk, hogy szeretnénk-e folytatni.
```
Akarsz játszani megint? (igen/nem) igen
```
Abban az esetben ha az elején kettő ugyanolyan lapot kapsz, akkor meg van az a lehetőség, hogy szétválaszd a paklidat, és innentől kezdve két paklival játssz tovább, erre a következő játék egy jó példa:
```Van 40 chipped.
Hi-Lo számláló: 3 (True count: 0.69)
Mennyit tennél fel? 20
Hi-Lo számláló: 4 (True count: 0.94)
Tét ajánlás: Alap tét rendben van
Játékos keze: Pick 7, Pick 7,
Érték: 14
Dealer (látható) keze: Treff 2,
Érték: 2
Stratégia ajánlás: Split (Oszd ketté)
Rendelkezésre álló opciók: [H]it / [S]tand / [D]ouble down / S[P]lit
Mit csinálsz? P
```
Innentől kezdve két kézzel játszunk:
```
Hi-Lo számláló: 5 (True count: 1.19)
2 kézbe osztva:
```
Először lejátszuk az első kézzel:
```
Első kéz:
Játékos keze: Pick 7, Treff 9,
Érték: 16
Stratégia ajánlás: Stand (Maradj)
Rendelkezésre álló opciók: [H]it / [S]tand / [D]ouble down
Mit csinálsz?s
```
Második kéz:
```
Második kéz:
Játékos keze: Pick 7, Káró 6,
Érték: 13
Stratégia ajánlás: Stand (Maradj)
Rendelkezésre álló opciók: [H]it / [S]tand / [D]ouble down
Mit csinálsz? h
```
