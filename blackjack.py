import random
import time


# Hi-Lo kártyaszámolás értékei
card_counting_values = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,  # Alacsony lapok: +1
    '7': 0, '8': 0, '9': 0,                   # Közepes lapok: 0
    '10': -1, 'Jumbó': -1, 'Dáma': -1, 'Király': -1, 'Ász': -1  # Magas lapok: -1
}

# Egy pakli kártyát így definiálunk
suits = ['Kör', 'Káró', 'Pick', 'Treff']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jumbó', 'Dáma', 'Király', 'Ász']
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jumbó': 10, 'Dáma': 10, 'Király': 10, 'Ász': 11}

# Globális változó a Hi-Lo kártyaszámoláshoz
count = 0
true_count = 0

def create_deck(num_decks=1):
    """Több pakli létrehozása és megkeverése"""
    deck = []
    for _ in range(num_decks):
        for suit in suits:
            for rank in ranks:
                deck.append((rank, suit))
    random.shuffle(deck)
    return deck


# Így számoljuk ki, hogy mennyi egy kéz értéke
def calculate_hand_value(hand):
    real_value = 0
    value = 0
    aces = 0
    
    for card in hand:
        real_value += values[card[0]]
        value += values[card[0]]
        if card[0] == 'Ász':
            aces += 1
            real_value -= 10
    
    while value > 21 and aces:
        value -= 10
        aces -= 1
    
    return value, real_value



# Így írjuk ki a konzolba a kezeket
def display_hand(hand, name):
    print(f"{name} keze: ", end='')
    for card in hand:
        print(f"{card[1]} {card[0]}", end=', ')
    print()
    #ászokat rendesen írja ki
    aces = 0
    for card in hand:
        if card[0] == 'Ász':
            if calculate_hand_value(hand)[1] < 12:
                print(f"Érték: {calculate_hand_value(hand)[1]}/{calculate_hand_value(hand)[0]}") #pl 4/14
            else:
                print(f"Érték: {calculate_hand_value(hand)[0]}")  # pl 15/25 nincs csak 15
            aces += 1
            break
    if aces == 0:
        print(f"Érték: {calculate_hand_value(hand)[0]}")   # csak siman 14 pl

# Tudunk-e splitelni?
def can_split(hand):
    return len(hand) == 2 and hand[0][0] == hand[1][0]

# Tudunk e double down-olni?
def can_double_down(hand):
    return len(hand) == 2


def blackjack_strategy(player_hand, dealer_upcard, true_count=0):
    #PLAYER HAND= A JÁTÉKOSNÁL LÉVŐ LAPOK
    #DEALER UPCARD= A DEALER LÁTHATÓ LAPJA
    #TRUE COUNT= A KÁRTYASZÁMOLÁS EREDMÉNYE

    # Kiszámoljuk a játékos kezének értékét
    player_value, real_value = calculate_hand_value(player_hand) #real value= ha van ászod akkor a kisebbik érték
    dealer_rank = dealer_upcard[0]
    
    # Dealer értékének konvertálása számra a stratégiához
    dealer_value = ""
    if dealer_rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10']:
        dealer_value = dealer_rank
    elif dealer_rank in ['Jumbó', 'Dáma', 'Király']:
        dealer_value = '10'
    elif dealer_rank == 'Ász':
        dealer_value = 'A'
    


    # Ellenőrizzük, hogy PÁRt kapott-e a játékos
    if len(player_hand) == 2 and player_hand[0][0] == player_hand[1][0]:
        card_rank = player_hand[0][0]
        pair_key = ""
        
        # Párok átalakítása a stratégia táblához
        if card_rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10']:
            pair_key = f"{card_rank},{card_rank}"
        elif card_rank in ['Jumbó', 'Dáma', 'Király']:
            pair_key = "10,10"
        elif card_rank == 'Ász':
            pair_key = "A,A"
        
        basic_strategy = get_strategy_from_table(pair_key, dealer_value)
        
        # True count alapján módosítás
        if true_count >= 3:
            # Magas true count esetén érdemes lehet inkább splitelni
            if pair_key == "10,10" and dealer_value in ['5', '6']:
                return "P"  # 10-es pár split magasabb true count esetén 5,6 ellen
            elif pair_key == "9,9" and dealer_value == '7':
                return "P"  # 9-es pár split magasabb true count esetén 7-es ellen
        
        return basic_strategy
    


    # Ellenőrizzük, hogy SOFT handünk van-e
    has_ace = False
    for card in player_hand:
        if card[0] == 'Ász':
            has_ace = True
            break
    
    if has_ace and player_value != real_value and player_value <= 21:  #Soft handünk van
        # Soft hand (A2-A9)
        non_ace_value = player_value - 11
        soft_key = f"A{non_ace_value}"  #pl A5
        
        basic_strategy = get_strategy_from_table(soft_key, dealer_value)  #táblából kikeresés
        
        # True count alapján módosítás soft handekre
        if true_count >= 4:
            if soft_key == "A6" and dealer_value in ['2']:
                return "DD"  # A6 vs 2: magas true count esetén Double Down
        
        return basic_strategy
    
    # Hard hand (8-17)
    basic_strategy = get_strategy_from_table(str(player_value), dealer_value)
    
    # True count alapján stratégia módosítás
    if true_count >= 3:
        # Magasabb true count előnyös a játékosnak
        if player_value == 12 and dealer_value == '2':
            return "S"  # 12 vs 2: true count >= 3 esetén Stand
        elif player_value == 12 and dealer_value == '3':
            return "S"  # 12 vs 3: true count >= 3 esetén Stand
        elif player_value == 16 and dealer_value == '10':
            return "S"  # 16 vs 10: true count >= 3 esetén Stand a surrender helyett
    
    if true_count >= 4:
        if player_value == 10 and dealer_value == 'A':
            return "DD"  # 10 vs A: igazi magas true count esetén Double Down  
        elif player_value == 9 and dealer_value == '2':
            return "DD"  # 9 vs 2: true count >= 4 esetén Double Down
    
    if true_count <= -2:
        # Alacsony true count nem előnyös a játékosnak, óvatosabb stratégia
        if player_value == 16 and dealer_value in ['9', '10']:
            return "H"  # 16 vs 9/10: alacsony true count esetén inkább surrender
    
    return basic_strategy

def get_strategy_from_table(player_key, dealer_value):
    # A stratégia tábla adatszerkezete
    strategy_map = {
        # Hard táblázat (8-21)
        "8":  {"2":"H", "3":"H", "4":"H", "5":"H", "6":"H", "7":"H", "8":"H", "9":"H", "10":"H", "A":"H"},
        "9":  {"2":"H", "3":"DD", "4":"DD", "5":"DD", "6":"DD", "7":"H", "8":"H", "9":"H", "10":"H", "A":"H"},
        "10": {"2":"DD", "3":"DD", "4":"DD", "5":"DD", "6":"DD", "7":"DD", "8":"DD", "9":"DD", "10":"H", "A":"H"},
        "11": {"2":"DD", "3":"DD", "4":"DD", "5":"DD", "6":"DD", "7":"DD", "8":"DD", "9":"DD", "10":"DD", "A":"H"},
        "12": {"2":"H", "3":"H", "4":"S", "5":"S", "6":"S", "7":"H", "8":"H", "9":"H", "10":"H", "A":"H"},
        "13": {"2":"S", "3":"S", "4":"S", "5":"S", "6":"S", "7":"H", "8":"H", "9":"H", "10":"H", "A":"H"},
        "14": {"2":"S", "3":"S", "4":"S", "5":"S", "6":"S", "7":"H", "8":"H", "9":"H", "10":"H", "A":"H"},
        "15": {"2":"S", "3":"S", "4":"S", "5":"S", "6":"S", "7":"H", "8":"H", "9":"H", "10":"H", "A":"H"},
        "16": {"2":"S", "3":"S", "4":"S", "5":"S", "6":"S", "7":"H", "8":"H", "9":"H", "10":"H", "A":"H"},
        "17": {"2":"S", "3":"S", "4":"S", "5":"S", "6":"S", "7":"S", "8":"S", "9":"S", "10":"S", "A":"S"},
        "18": {"2":"S", "3":"S", "4":"S", "5":"S", "6":"S", "7":"S", "8":"S", "9":"S", "10":"S", "A":"S"},
        "19": {"2":"S", "3":"S", "4":"S", "5":"S", "6":"S", "7":"S", "8":"S", "9":"S", "10":"S", "A":"S"},
        "20": {"2":"S", "3":"S", "4":"S", "5":"S", "6":"S", "7":"S", "8":"S", "9":"S", "10":"S", "A":"S"},
        "21": {"2":"S", "3":"S", "4":"S", "5":"S", "6":"S", "7":"S", "8":"S", "9":"S", "10":"S", "A":"S"},
        
        # Soft táblázat (A2-AA)
        "A2": {"2":"H", "3":"H", "4":"H", "5":"DD", "6":"DD", "7":"H", "8":"H", "9":"H", "10":"H", "A":"H"},
        "A3": {"2":"H", "3":"H", "4":"H", "5":"DD", "6":"DD", "7":"H", "8":"H", "9":"H", "10":"H", "A":"H"},
        "A4": {"2":"H", "3":"H", "4":"DD", "5":"DD", "6":"DD", "7":"H", "8":"H", "9":"H", "10":"H", "A":"H"},
        "A5": {"2":"H", "3":"H", "4":"DD", "5":"DD", "6":"DD", "7":"H", "8":"H", "9":"H", "10":"H", "A":"H"},
        "A6": {"2":"H", "3":"DD", "4":"DD", "5":"DD", "6":"DD", "7":"H", "8":"H", "9":"H", "10":"H", "A":"H"},
        "A7": {"2":"S", "3":"DD", "4":"DD", "5":"DD", "6":"DD", "7":"S", "8":"S", "9":"H", "10":"H", "A":"H"},
        "A8": {"2":"S", "3":"S", "4":"S", "5":"S", "6":"S", "7":"S", "8":"S", "9":"S", "10":"S", "A":"S"},
        "A9": {"2":"S", "3":"S", "4":"S", "5":"S", "6":"S", "7":"S", "8":"S", "9":"S", "10":"S", "A":"S"},
        
        # Párok (2,2-A,A)
        "2,2": {"2":"P", "3":"P", "4":"P", "5":"P", "6":"P", "7":"P", "8":"H", "9":"H", "10":"H", "A":"H"},
        "3,3": {"2":"H/P", "3":"H/P", "4":"P", "5":"P", "6":"P", "7":"P", "8":"H", "9":"H", "10":"H", "A":"H"},
        "4,4": {"2":"H", "3":"H", "4":"H", "5":"H/P", "6":"H/P", "7":"H", "8":"H", "9":"H", "10":"H", "A":"H"},
        "5,5": {"2":"DD", "3":"DD", "4":"DD", "5":"DD", "6":"DD", "7":"DD", "8":"DD", "9":"DD", "10":"H", "A":"H"},
        "6,6": {"2":"H/P", "3":"P", "4":"P", "5":"P", "6":"P", "7":"H", "8":"H", "9":"H", "10":"H", "A":"H"},
        "7,7": {"2":"P", "3":"P", "4":"P", "5":"P", "6":"P", "7":"P", "8":"H", "9":"H", "10":"H", "A":"H"},
        "8,8": {"2":"P", "3":"P", "4":"P", "5":"P", "6":"P", "7":"P", "8":"P", "9":"P", "10":"P", "A":"P"},
        "9,9": {"2":"P", "3":"P", "4":"P", "5":"P", "6":"P", "7":"S", "8":"P", "9":"P", "10":"S", "A":"S"},
        "10,10": {"2":"S", "3":"S", "4":"S", "5":"S", "6":"S", "7":"S", "8":"S", "9":"S", "10":"S", "A":"S"},
        "A,A": {"2":"P", "3":"P", "4":"P", "5":"P", "6":"P", "7":"P", "8":"P", "9":"P", "10":"P", "A":"P"}
    }
    
    # Ellenőrizzük, hogy a játékos keze szerepel-e a stratégia táblában
    if player_key in strategy_map and dealer_value in strategy_map[player_key]:
        return strategy_map[player_key][dealer_value]
    else:
        # Ha nincs explicit stratégia (például 8 alatti kemény összeg)
        if player_key.isdigit() and int(player_key) < 8:
            return "H"  # 8 alatti kemény totálnál mindig hit
        
        # Alapértelmezett eset, ha nem tudjuk meghatározni a stratégiát
        return "H"  # Alapértelmezett: hit

# Ajánlások szöveges értelmezése
def interpret_strategy(strategy_code):
    """Az ajánlott stratégia kódjának szöveges értelmezése"""
    interpretations = {
        "H": "Hit (Húzz lapot)",
        "S": "Stand (Maradj)",
        "DD": "Double Down (Dupla tét)",
        "P": "Split (Oszd ketté)",
    }
    return interpretations.get(strategy_code, strategy_code)

def get_true_count_recommendation(true_count):
    """True count ajánlások a játékhoz"""
    if true_count >= 5:
        return "Emelj sokat!"
    elif true_count >= 3:
        return "Emelhetsz többet is!"
    elif true_count >= 1:
        return "Kicsit emeld a tétet."
    elif true_count <= -3:
        return "Keveset rakj fel nagyon!"
    elif true_count <= -1:
        return "Rakj kevesebb tétet."
    else:
        return "Rakj egy normál tétet."

# Egy játék játszása
def play_hand(deck, player_hand, dealer_hand, bet, is_split_hand=False):
    global count  # Hozzáférés a globális számlálóhoz
    global true_count  # Hozzáférés a globális true_count-hoz
    current_bet = bet
    
    while True:
        display_hand(player_hand, 'Játékos')
        if not is_split_hand:
            display_hand([dealer_hand[0]], 'Dealer (látható)')
        
        # Blackjack-e?
        if calculate_hand_value(player_hand)[0] == 21 and len(player_hand) == 2:
            if not is_split_hand:
                print("Blackjack!")
                return bet * 1.5  # Blackjacknél 1.5-szer annyit kapsz
            else:
                print("21! Nyertél!")
                return bet * 1   #Splitelt kéznél nincs blackjack
        
        # STRATÉGIA AJÁNLÁS KÉRÉSE
        strategy_result = blackjack_strategy(player_hand, dealer_hand[0], true_count)
        print(f"Stratégia ajánlás: {interpret_strategy(strategy_result)}")
        
        # Amit tudunk csinálni
        actions = ['[H]it', '[S]tand']
        if can_double_down(player_hand):
            actions.append('[D]ouble down')
        if can_split(player_hand) and not is_split_hand:
            actions.append('S[P]lit')
        
        print(f"Rendelkezésre álló opciók: {' / '.join(actions)}")
        action = input("Mit csinálsz? ").lower()
        print("\n")


        #Ha Hit-elünk
        if action == 'h':
            new_card = deck.pop() #húzunk egy lapot
            player_hand.append(new_card) #kibővítjük a kezet
            
            # Kártyaszámolás frissítése
            count += card_counting_values[new_card[0]]
            true_count = round(count / (len(deck) / 52), 2)
            print(f"Hi-Lo számláló: {count} (True count: {true_count})")
            
            if calculate_hand_value(player_hand)[0] > 21:
                display_hand(player_hand, 'Játékos')
                print("Besokaltál, vesztettél!")
                return -current_bet
            

        #Ha Double Down-olunk        
        elif action == 'd' and can_double_down(player_hand):
            current_bet *= 2
            print(f"Tét emelése {current_bet}-re")
            new_card = deck.pop()
            player_hand.append(new_card)
            
            # Kártyaszámolás frissítése
            count += card_counting_values[new_card[0]]
            true_count = round(count / (len(deck) / 52), 2)
            print(f"Hi-Lo számláló: {count} (True count: {true_count})")
            
            display_hand(player_hand, 'Játékos')
            
            if calculate_hand_value(player_hand)[0] > 21:
                print("Besokaltál, vesztettél!")
                return -current_bet
            else:
                # Egy lapot húzunk double után vagyis itt vége van a húzásnak
                break



        #Ha Splitelünk        
        elif action == 'p' and can_split(player_hand) and not is_split_hand:
            # 2 kezünk lesz
            new_card1 = deck.pop()
            new_card2 = deck.pop()
            
            # Kártyaszámolás frissítése
            count += card_counting_values[new_card1[0]] + card_counting_values[new_card2[0]]
            true_count = round(count / (len(deck) / 52), 2)
            print(f"Hi-Lo számláló: {count} (True count: {true_count})")
            
            hand1 = [player_hand[0], new_card1]
            hand2 = [player_hand[1], new_card2]
            
            print("2 kézbe osztva:")
            
            print("\nElső kéz:")
            result1 = play_hand(deck, hand1, dealer_hand, bet, is_split_hand=True)
            
            print("\nMásodik kéz:")
            result2 = play_hand(deck, hand2, dealer_hand, bet, is_split_hand=True)
            
            # Dealer játéka a split kezek ellen
            split_hands = []
            split_bets = []
            
            # Első kéz feldolgozása
            if isinstance(result1, tuple):
                split_hands.append(result1[0])  # Kéz
                split_bets.append(result1[1])   # Tét
            else:
                # Ha már szám, akkor már vége a játéknak ennél a kéznél (pl. besokallás)
                total_result = result1
                
                if isinstance(result2, tuple):
                    split_hands.append(result2[0])
                    split_bets.append(result2[1])
                    # Csak a második kezet játsszuk le
                else:
                    # Mindkét eredmény szám, visszaadjuk az összeget
                    return result1 + result2
            
            # Második kéz feldolgozása, ha még nem volt feldolgozva
            if isinstance(result2, tuple) and not split_hands:
                split_hands.append(result2[0])
                split_bets.append(result2[1])
                total_result = 0
            elif isinstance(result2, tuple):
                split_hands.append(result2[0])
                split_bets.append(result2[1])
            elif not 'total_result' in locals():
                total_result = result2
            
            # Ha van olyan kéz, amit le kell játszani
            if split_hands:
                # Dealer játéka
                print("\nDealer játéka a splitelt kezek ellen:")
                display_hand(dealer_hand, 'Dealer')
                
                # Dealer húzása
                while calculate_hand_value(dealer_hand)[0] < 17:  # Hivatalosan 17-nél megállnak
                    new_card = deck.pop()
                    dealer_hand.append(new_card)
                    print(f"Dealer húzott: {new_card[1]} {new_card[0]}")
                    
                    # Kártyaszámolás frissítése
                    count += card_counting_values[new_card[0]]
                    true_count = round(count / (len(deck) / 52), 2)
                    print(f"Hi-Lo számláló: {count} (True count: {true_count})")
                    
                    time.sleep(1)  # Egy kis delay
                    display_hand(dealer_hand, 'Dealer')
                
                dealer_value = calculate_hand_value(dealer_hand)[0]
                
                # Kiértékeljük az összes megmaradt kezet
                if not 'total_result' in locals():
                    total_result = 0
                    
                for i in range(len(split_hands)):
                    hand = split_hands[i]
                    bet_amount = split_bets[i]
                    player_value = calculate_hand_value(hand)[0]
                    
                    print(f"\nKéz #{i+1} kiértékelése:")
                    display_hand(hand, 'Játékos')
                    print(f"Játékos érték: {player_value}, Dealer érték: {dealer_value}")
                    
                    if player_value > 21:
                        print("Ez a kéz besokallott!")
                        total_result -= bet_amount
                    elif dealer_value > 21:
                        print("Dealer besokallt! Ez a kéz nyert!")
                        total_result += bet_amount
                    elif player_value > dealer_value:
                        print("Ez a kéz nyert!")
                        total_result += bet_amount
                    elif player_value == dealer_value:
                        print("Döntetlen ennél a kéznél.")
                        # Döntetlennél nincs változás
                    else:
                        print("Dealer nyert ennél a kéznél!")
                        total_result -= bet_amount
            
            return total_result
            
        elif action == 's':
            break
        else:
            print("Nem helyes input, csinálj mást!")
    
    # Splitelt esetben
    if is_split_hand:
        return player_hand, current_bet
    
    # Dealer része
    print("\nDealer jön:")
    display_hand(dealer_hand, 'Dealer')
    

    #Dealer húzása
    while calculate_hand_value(dealer_hand)[0] < 17:  #Hivatalosan 17-nél megállnak
        new_card = deck.pop()
        dealer_hand.append(new_card)
        print(f"Dealer húzott: {new_card[1]} {new_card[0]}")
        
        # Kártyaszámolás frissítése
        count += card_counting_values[new_card[0]]
        true_count = round(count / (len(deck) / 52), 2)
        print(f"Hi-Lo számláló: {count} (True count: {true_count})")
        
        time.sleep(1)  # Egy kis delay
        display_hand(dealer_hand, 'Dealer')
    
    # Győztes hirdetése
    player_value = calculate_hand_value(player_hand)[0]
    dealer_value = calculate_hand_value(dealer_hand)[0]
    
    if dealer_value > 21:
        print("Dealer besokallt! Nyertél!")
        return current_bet
    elif player_value > dealer_value:
        print("Nyertél!")
        return current_bet
    elif player_value == dealer_value:
        print("Döntetlen")
        return 0
    else:
        print("Dealer nyert!")
        return -current_bet

# Fő függvényünk
def play_blackjack():
    global count  # Használjuk a globális számlálót
    global true_count  # Használjuk a globális true_count-ot
    
    # Paklik számának bekérése
    while True:
        try:
            num_decks = int(input("Hány paklival szeretnél játszani? (1-8): "))
            if 1 <= num_decks <= 8:
                break
            else:
                print("Kérlek 1 és 8 közötti számot adj meg!")
        except ValueError:
            print("Kérlek egy egész számot adj meg!")
    
    # Több pakli létrehozása
    deck = create_deck(num_decks)
    print(f"{num_decks} paklival játszol, összesen {len(deck)} kártya.")
    
    chips = 100  # Kezdő chipek
    count = 0    # Hi-Lo kártyaszámolás kezdeti értéke reseteléése
    true_count = 0  # True count kezdeti értéke
    
    print(f"{chips} chippel kezdessz.")
    print("Hi-Lo kártyaszámolás bekapcsolva. Kezdő érték: 0")
    
    # Az újrakeverés küszöbértéke a paklik számától függ, 15 kártya paklinként
    reshuffle_threshold = num_decks * 15
    
    while chips > 0:
        print(f"\nVan {chips} chipped.")
        print(f"Hi-Lo számláló: {count} (True count: {true_count})")
        print(f"Tét ajánlás: {get_true_count_recommendation(true_count)}")
        
        try:
            bet = int(input("Mennyit tennél fel? "))
            if bet <= 0 or bet > chips:
                print(f"Egy egész számot adj meg 1 és {chips} között.")
                continue
        except ValueError:
            print("Egy egész számot adj meg.")
            continue
        
        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]
        
        # Hi-Lo kártyaszámolás frissítése a kezdeti lapokra
        for card in player_hand + [dealer_hand[0]]:  # Csak a dealer látható lapját számoljuk
            count += card_counting_values[card[0]]
        
        # Számláló megjelenítése
        true_count = round(count / (len(deck) / 52), 2)  # True count = count / remaining decks
        print('\n')
        print(f"Hi-Lo számláló: {count} (True count: {true_count})")

        # Ha kevés kártya maradt, újrakeverünk
        if len(deck) < reshuffle_threshold:
            deck = create_deck(num_decks)
            count = 0  # Számláló nullázása keverésnél
            true_count = 0  # True count nullázása
            print(f"Új {num_decks} pakli keverése. Összesen {len(deck)} kártya.")
            print("Hi-Lo számláló újraindítva: 0")
        

        # Mi lett a végkimenetel
        result = play_hand(deck, player_hand, dealer_hand, bet)
        
        # A result lehet egy lista is, ha spliteltünk, ezt így intézzük.
        if isinstance(result, tuple):
            split_hand, split_bet = result
            
            # Jön a dealer a splitelt kézhez
            print("\nDealer jön:(splitelt kéz)")
            display_hand(dealer_hand, 'Dealer')
            
            while calculate_hand_value(dealer_hand)[0] < 17:
                new_card = deck.pop()
                dealer_hand.append(new_card)
                print(f"Dealer húzott: {new_card[1]} {new_card[0]}")
                
                # Kártyaszámolás frissítése
                count += card_counting_values[new_card[0]]
                true_count = round(count / (len(deck) / 52), 2)
                print(f"Hi-Lo számláló: {count} (True count: {true_count})")
                
                time.sleep(1)
                display_hand(dealer_hand, 'Dealer')
            
            # Nyertes eldöntése
            player_value = calculate_hand_value(split_hand)[0]
            dealer_value = calculate_hand_value(dealer_hand)[0]
            
            if dealer_value > 21:
                print("Dealer besokallt! Nyertél!")
                result = split_bet
            elif player_value > dealer_value:
                print("Nyertél!")
                result = split_bet
            elif player_value == dealer_value:
                print("Döntetlen.")
                result = 0
            else:
                print("Dealer nyert!")
                result = -split_bet
        
        # Chippek frissitése
        chips += result
        
        if chips <= 0:
            print("Nincs több chipped. Vége a játéknak!")
            break
            
        if input("Akarsz játszani megint? (igen/nem) ").lower() != 'igen':
            print(f"Köszi a játékot! {chips} chippel fejezted be a játékot.")
            break

# Játék futtatása
if __name__ == "__main__":
    play_blackjack()