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
                print(f"Érték: {calculate_hand_value(hand)[1]}/{calculate_hand_value(hand)[0]}")
            else:
                print(f"Érték: {calculate_hand_value(hand)[0]}")
            aces += 1
            break
    if aces == 0:
        print(f"Érték: {calculate_hand_value(hand)[0]}")

# Tudunk-e splitelni?
def can_split(hand):
    return len(hand) == 2 and hand[0][0] == hand[1][0]

# Tudunk e double down-olni?
def can_double_down(hand):
    return len(hand) == 2

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
            new_card = deck.pop()
            player_hand.append(new_card)
            
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
            
            return result1 + result2
            
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
    
    print(f"{chips} chippel kezdessz.")
    print("Hi-Lo kártyaszámolás bekapcsolva. Kezdő érték: 0")
    
    # Az újrakeverés küszöbértéke a paklik számától függ
    reshuffle_threshold = num_decks * 15
    
    while chips > 0:
        print(f"\nVan {chips} chipped.")
        print(f"Hi-Lo számláló: {count} (True count: {true_count})")

        
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
        print(f"Hi-Lo számláló: {count} (True count: {true_count})")
        
        # Ha kevés kártya maradt, újrakeverünk
        if len(deck) < reshuffle_threshold:
            deck = create_deck(num_decks)
            count = 0  # Számláló nullázása keverésnél
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