from discord import File
from random import randint

class Card:
    def __init__(self,val,suit) -> None:
        self.face = val
        self.suit = suit
        self.int_val = self.value()
        self.img = f"discorddeckpng/{self.face}_{suit}"

    def value(self):
        if self.face == 'ace':
            return 11

        if self.face in ['K','J','Q']:
            return 10
        
        return int(self.face)

class Deck:
    def __init__(self) -> None:
        self.card_values = ['ace','2','3','4','5','6','7','8','9','10','J','K','Q']
        self.card_suits = ['spades','diamonds','clubs','hearts']
        self.cards = []
    
    def create_deck(self):
        for v in self.card_values:
            for s in self.card_suits:
                self.cards.append(Card(v,s))


class bjGame(Deck):
    def __init__(self,channel,author):
        super().__init__()
        self.create_deck()
        self.channel = channel
        self.author = author
        self.hand = []
        self.hand_value = 0
        self.dealer_hand = []
        self.dealer_hand_value = 0

    def STARTGAME(self):
        '''be sure to make this function async and add necessary awaits'''
        self.draw_card(dealer=True); self.draw_card(dealer=True)
        print(f"dealers first card: {self.dealer_hand[0].face}")
        print(self.game_loop())
    
    async def send_card_img(self,val,suit):
        with open(f'discorddeckpng/{val}_{suit}','rb') as fh:
            f = File(fh,filename=f'discorddeckpng/{val}_{suit}')
            await self.channel.send(file=f)

    def get_hand_value(self,hand):
        total_val = 0
        num_of_ace = 0
        for i in hand:
            if i.face == 'ace':
                num_of_ace +=1
                continue
            total_val += i.int_val

        for i in range(num_of_ace):
            total_val += 11
            if total_val > 21:
                total_val-=10

        return total_val
    
    def draw_card(self,dealer=False):
        random_card = randint(0,len(self.cards)-1)
        if not dealer:
            self.hand.append(self.cards.pop(random_card))
        else:
            self.dealer_hand.append(self.cards.pop(random_card))
    
    def check_for_bust(self,hand):
        total_val = 0
        num_of_ace = 0
        for i in hand:
            if i.face == 'ace':
                num_of_ace +=1
                continue
            total_val += i.int_val

        if total_val > 21:
            return 'bust'

        for i in range(num_of_ace):
            total_val += 11
            if total_val > 21 and (total_val-10) > 21:
                return 'bust'
            else:
                total_val-=10
        return total_val
    
    def dealer_phase(self):
        pass

    def game_loop(self):
        self.draw_card()

        print(f"you have: {self.get_hand_value(self.hand)}")

        for i in self.hand:
            print(i.face)

        if self.check_for_bust(self.hand) == 'bust':
            return "game over"
        
        hit = str(input("hit or stand? (h/s)"))

        if hit == 'h':
            self.game_loop()
        
        if hit == 's':
            pass


bj = bjGame('s','s')
bj.STARTGAME()

        

    
    



