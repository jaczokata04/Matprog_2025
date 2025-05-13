import random
import matplotlib.pyplot as plt

# Kártyák és értékek definiálása
suits = ['Kör', 'Káró', 'Pick', 'Treff']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jumbó', 'Dáma', 'Király', 'Ász']
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jumbó': 10, 'Dáma': 10, 'Király': 10, 'Ász': 11}

# Hi-Lo kártyaszámolás értékei
card_counting_values = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,  # Alacsony lapok: +1
    '7': 0, '8': 0, '9': 0,                   # Közepes lapok: 0
    '10': -1, 'Jumbó': -1, 'Dáma': -1, 'Király': -1, 'Ász': -1  # Magas lapok: -1
}

def create_deck(num_decks=1):
    """Több pakli létrehozása"""
    deck = []
    for _ in range(num_decks):
        for suit in suits:
            for rank in ranks:
                deck.append((rank, suit))
    random.shuffle(deck)
    return deck

def calculate_hand_value(hand):
    """Kézérték számítása"""
    value = 0
    aces = 0
    
    for card in hand:
        value += values[card[0]]
        if card[0] == 'Ász':
            aces += 1
    
    # Ász kezelés, 11 vagy 1 értékkel
    while value > 21 and aces:
        value -= 10
        aces -= 1
    
    return value

def blackjack_strategy(player_hand, dealer_upcard, true_count=0):
    """Stratégia meghatározása"""
    # Kiszámoljuk a játékos kezének értékét
    player_value = calculate_hand_value(player_hand)
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
    
    original_value = sum(values[card[0]] for card in player_hand)
    is_soft = has_ace and (original_value <= 21) and (calculate_hand_value(player_hand) == original_value)
    
    if is_soft:  # Soft handünk van
        # Soft hand (A2-A9)
        non_ace_value = player_value - 11
        soft_key = f"A{non_ace_value}"  # pl A5
        
        basic_strategy = get_strategy_from_table(soft_key, dealer_value)  # táblából kikeresés
        
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
    """Stratégia tábla"""
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

def simulate_game(true_count=0):
    """Egy teljes játék szimulálása"""
    # Pakli létrehozása - szimuláció miatt csak 1 pakli
    deck = create_deck()
    random.shuffle(deck)
    
    # Kezdő lapok
    player = [deck.pop(), deck.pop()]
    dealer = [deck.pop(), deck.pop()]
    
    # Játékos stratégiája
    while True:
        move = blackjack_strategy(player, dealer[0], true_count)
        
        # Hit - Húzzunk lapot
        if move == "H" or (move == "H/P" and random.random() < 0.5):  # H/P esetén 50% eséllyel hit
            player.append(deck.pop())
            if calculate_hand_value(player) > 21:
                return -1  # Besokallás
        
        # Stand - Megállunk
        elif move == "S":
            break
        
        # Double Down - Dupla tét + még egy lap
        elif move == "DD":
            player.append(deck.pop())
            if calculate_hand_value(player) > 21:
                return -2  # Besokallás dupla veszteséggel
            else:
                break  # Megállunk a dupla után
        
        # Split - megosztás (egyszerűsítve)
        elif move == "P":
            # Szimuláció egyszerűsítés: split esetén két új játékot játszunk
            result1 = simulate_split_hand(deck, player[0], dealer[0], true_count)
            result2 = simulate_split_hand(deck, player[1], dealer[0], true_count)
            return result1 + result2
    
    # Dealer húzása (Dealer szabály: 17-nél megáll)
    while calculate_hand_value(dealer) < 17:
        dealer.append(deck.pop())
    
    # Eredmények kiértékelése
    player_value = calculate_hand_value(player)
    dealer_value = calculate_hand_value(dealer)
    
    # Dupla tét esetén
    multiplier = 2 if move == "DD" else 1
    
    if player_value > 21:
        return -1 * multiplier  # Játékos besokallás
    elif dealer_value > 21:
        return 1 * multiplier   # Dealer besokallás
    elif player_value > dealer_value:
        return 1 * multiplier   # Játékos nyer
    elif player_value < dealer_value:
        return -1 * multiplier  # Dealer nyer
    else:
        return 0                # Döntetlen

def simulate_split_hand(deck, card, dealer_card, true_count=0):
    """Split kéz szimulálása"""
    # Új kéz létrehozása az eredeti lapból és egy újból
    hand = [(card[0], card[1]), deck.pop()]
    
    # Játék szimulálása
    while True:
        move = blackjack_strategy(hand, dealer_card, true_count)
        
        if move == "H" or (move == "H/P" and random.random() < 0.5):
            hand.append(deck.pop())
            if calculate_hand_value(hand) > 21:
                return -1  # Besokallás
        elif move == "S":
            break
        elif move == "DD":
            hand.append(deck.pop())
            if calculate_hand_value(hand) > 21:
                return -2  # Besokallás dupla veszteséggel
            else:
                break
        else:  # P, H/P esetén
            hand.append(deck.pop())
            if calculate_hand_value(hand) > 21:
                return -1
    
    # Dealer kéz szimulálása
    dealer = [dealer_card, deck.pop()]
    while calculate_hand_value(dealer) < 17:
        dealer.append(deck.pop())
    
    # Eredmények kiértékelése
    player_value = calculate_hand_value(hand)
    dealer_value = calculate_hand_value(dealer)
    
    # Dupla tét esetén
    multiplier = 2 if move == "DD" else 1
    
    if player_value > 21:
        return -1 * multiplier
    elif dealer_value > 21:
        return 1 * multiplier
    elif player_value > dealer_value:
        return 1 * multiplier
    elif player_value < dealer_value:
        return -1 * multiplier
    else:
        return 0

def run_simulation(num_games=10000):
    """Megadott számú játék szimulálása fix 0-s true count értékkel"""
    true_count = 0  # Fix 0-s true count érték
    print(f"Blackjack szimuláció indítása {num_games} játékkal, True Count = {true_count}")
    
    # Eredmények gyűjtése
    wins = 0
    losses = 0
    draws = 0
    
    # Pénznyeremény követése
    total_profit = 0
    
    for i in range(num_games):
        result = simulate_game(true_count)
        
        if result > 0:
            wins += 1
            total_profit += result
        elif result < 0:
            losses += 1
            total_profit += result
        else:
            draws += 1
    
    # Eredmények kijelzése
    win_rate = wins / num_games
    loss_rate = losses / num_games
    draw_rate = draws / num_games
    print(f"Nyerési arány: {win_rate:.2%}")
    print(f"Veszteségi arány: {loss_rate:.2%}")
    print(f"Döntetlen arány: {draw_rate:.2%}")
    print(f"Profit/veszteség: {total_profit}")
    print(f"Átlagos profit/játék: {total_profit/num_games:.4f}")
    
    # Grafikus megjelenítés - csak egy ábra az arányokról
    plt.figure(figsize=(10, 8))
    
    # Oszlopdiagram a nyerési/veszteségi/döntetlen arányokról
    labels = ['Nyerés', 'Veszteség', 'Döntetlen']
    values = [wins, losses, draws]
    colors = ['green', 'red', 'gray']
    
    bars = plt.bar(labels, values, color=colors)
    
    # Hozzáadjuk a százalékokat az oszlopok tetejére
    for bar in bars:
        height = bar.get_height()
        percentage = height / num_games * 100
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.05 * max(values),
                f'{percentage:.1f}%', ha='center', va='bottom')
    
    plt.title('Blackjack eredmények (alapstratégia szerint, True Count = 0)')
    plt.ylabel('Játékok száma')
    plt.grid(True, axis='y', linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# Fő program - automatikusan elindítja 10000 játék szimulálását
if __name__ == "__main__":
    # Alapértelmezetten 10000 játék szimulálása, de változtatható itt
    num_games = 10000
    run_simulation(num_games)