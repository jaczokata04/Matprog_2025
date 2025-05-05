# Matprog_2025
Bringing down the House strategy

# Blackjack vagy más néven 21

A blackjack a kaszinókban egyik legnépszerűbb játék. A játék lényege, hogy van egy osztó, és egy- vagy több játékos. Kezdetben minden játékos kap két lapot, és az osztó (vagy más néven dealer), pedig maga elé is oszt két kapot: egyet fel-, a másikat lefordítva. Ekkor a cél, hogy a játékos keze közelebb legyen a 21-hez, mint az osztóé, de ne haladja meg. A kártyák az értékük szerint: számkártyák annyit érnek, amennyi rájuk van írva, a bubi, dáma, király pedig 10-10-10 pontot érnek, és az ász 1 vagy 11-et, attól függően, hogy melyik az előnyösebb. Az osztó szabályai: 16 pontig kötelező húznia, de 17-nél vagy afelett meg kell állnia. Manapság már minden kör után visszakeverik a lapokat a pakliba, viszont régebben csak 15 lap alatt keverték vissza, és emiatt működött a következő kártyaszámlálási stratégia:

# Hi-Lo stratégia

A játék során minden kijátszott laphoz hozzárendelünk egy értéket a következő módon:

2-6: a lapok értéke legyen +1
7-9: a lapok értéke 0
10, J, Q, K, A: a lapok értéke -1.

Maga a stratégia: ahogy mennek ki a lapok, megyjegyezzük a kiment lapok értékeinek összegét. Ez az összeg a futó számláló (running count). Milyen érték jó nekünk?

A kis lapok (2-6) segítik az osztót, tehát jó, ha elfogynak. A nagy lapok (10-A) viszont a játékost segítik, mivel így nagyobb eséllyel lesz Blackjack-ünk (azaz 21 értékű kezünk), ezért jó ha sok nagy lap van még a pakliban.

Több pakli esetén kicsit változtatni kell. Itt nem a running count kell, hanem az úgynevezett true count, amit úgy kapunk meg, hogy a running count értékét elosztjuk a jelenleg bent maradt paklik számával. Ekkor, ha a játék közben a true count> 1 vagy 2, akkor érdemes nagy tétet tenni, mivel a játékosnak nagy esélye van, ha a true count <= 0, ekkor érdemesebb kis tétet rakni, vagy akár ki is hagyni a kört.

# A játék menete

Miután megkaptad a kezdő lapjaidat, 3 lehetőséged van. Hit, stand vagy split. A hit azt jelenti, hogy kérsz még egy lapot, ha ezzel túlléped a 21-et, akkor vesztettél automatikusan. A stand azt jelenti, hogy nem kérsz több lapot, ezt érdemes akkor, ha nagy értékű lapjaid vannak. A split csak akkor opció, ha két ugyanolyan lapot kaptál kezdésnek, ekkor megduplázod a pakliaidat és ezentúl két "kézzel" játszol, ekkor a tétet is megduplázod.

Ez a projekt egy egyszerű, szöveges alapú Blackjack játék Python nyelven, ahol lehetőség van **hit**, **stand**, **duplázás** (double down) és **split** lépésekre is. A cél: legyőzni a dealt, anélkül hogy besokallnánk (21 pont fölé mennénk).

## 🎯 Funkciók

- Véletlenszerűen kevert pakli generálása
- Játékos és dealer kezek kezelése
- Kártyák értékének helyes számolása, külön kezelve az Ász lapokat
- Duplázás (Double Down) lehetőség
- Osztás (Split) lehetőség, ha az első két lap azonos
- Egyszerű pontszám kezelés (zseton rendszer)

## ▶️ Használat

1. **Python 3** szükséges a futtatáshoz.
2. Futtatás a terminálból:

```bash
python blackjack.py
