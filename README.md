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

## A játék menete

A programunk először megkérdezi, hogy hány paklival szeretnénk játszani, a következő módon. A játékos 1-től 8-ig választhat. 
Majd a választás után a játék kiírja, hogy az adott játékban hány chippel kezdünk. Az első játék elején 100 chippünk van, majd a további játékokban, az adott egyenlegünket írja ki. Ezek mellett elindul a Hi-Lo számláló, kiírja a kezdő értéket, majd minden körben frissíti. 

```
Hány paklival szeretnél játszani? (1-8): 3
3 paklival játszol, összesen 156 kártya.
100 chippel kezdessz.
Hi-Lo kártyaszámolás bekapcsolva. Kezdő érték: 0
```

```
```
Hány paklival szeretnél játszani? (1-8): 3
3 paklival játszol, összesen 156 kártya.
100 chippel kezdessz.
Hi-Lo kártyaszámolás bekapcsolva. Kezdő érték: 0
``````
Hány paklival szeretnél játszani? (1-8): 3
3 paklival játszol, összesen 156 kártya.
100 chippel kezdessz.
Hi-Lo kártyaszámolás bekapcsolva. Kezdő érték: 0
``````Hány paklival szeretnél játszani? (1-8): 33 paklival játszol, összesen 156 kártya.100 chippel kezdessz.Hi-Lo kártyaszámolás bekapcsolva. Kezdő érték: 0```

Miután megkaptad a kezdő lapjaidat, 4 lehetőséged van. Hit, stand, double down vagy split. A hit azt jelenti, hogy kérsz még egy lapot, de ha ezzel túlléped a 21-et, akkor vesztettél automatikusan. A stand azt jelenti, hogy nem kérsz több lapot, ezt akkor érdemes, ha nagy értékű lapjaid vannak. A double down az azt jelenti, hogy megduplázod a tétedet, mielőtt kapsz egy új lapot. A split csak akkor opció, ha két ugyanolyan lapot kaptál kezdésnek, ekkor megduplázod a paklijaidat és ezentúl két "kézzel" játszol, ekkor a tétet is megduplázod.

A "v_8" fáljban lévő program, egy Blackjack szimuláció, amit úgy írtunk meg, hogy közben a Hi-Lo módszerrel számolja a kártyákat. A program a játék elején felajánlja, hogy a játékos válasszon, hány paklival szeretne játszani.



A paklik összekeverve indulnak, és automatikusan újrakeverődnek, ha túl kevés lap marad (15 alatt), pont úgy, mint a valódi kaszinókban, mielőtt visszakevernének. 
A játék közben minden körben a program felajánl 3 (vagy 4, ha kettő ugyanolyat kapsz) lehetőséget: hit, stand, double down(vagy split). Ezek mellett minden kör elején kiírja az aktuális true count-ot is. Ez alapján a játékos könnyebben eldöntheti hogy kér e még lapot vagy sem.

```
Van 100 chipped.
Hi-Lo számláló: 0 (True count: 0)
Mennyit tennél fel? 20
Hi-Lo számláló: 1 (True count: 0.25)
Játékos keze: Káró 6, Kör 5,
Érték: 11
Dealer (látható) keze: Pick Dáma,
Érték: 10
Rendelkezésre álló opciók: [H]it / [S]tand / [D]ouble down
Mit csinálsz?
```
Abban az esetben ha az elején kettő ugyanolyan lapot kapsz, akkor meg van az a lehetőség, hogy szétválaszd a paklidat, és innentől kezdve két paklival játssz tovább:

```
Hány paklival szeretnél játszani? (1-8): 3
3 paklival játszol, összesen 156 kártya.
100 chippel kezdessz.
Hi-Lo kártyaszámolás bekapcsolva. Kezdő érték: 0

Van 100 chipped.
Hi-Lo számláló: 0 (True count: 0)
Mennyit tennél fel? 10
Hi-Lo számláló: 0 (True count: 0.0)
Tét ajánlás: Alap tét rendben van
Játékos keze: Treff 7, Pick 4,
Érték: 11
Dealer (látható) keze: Kör Jumbó,
Érték: 10
Stratégia ajánlás: Double Down (Dupla tét)
Rendelkezésre álló opciók: [H]it / [S]tand / [D]ouble down
Mit csinálsz?
´´´
