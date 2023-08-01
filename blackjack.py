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
    def __init__(self,channel,author,client, bet_amnt):
        super().__init__()
        self.create_deck()
        self.channel = channel
        self.author = author
        self.client = client
        self.hand = []
        self.hand_value = 0
        self.dealer_hand = []
        self.dealer_hand_value = 0

        self.bet_amnt = bet_amnt
        self.trash_talk = ['you suck LOLOLOL','gg','goodgame well played you suck','try not to lose next time','yup keep losing','wow you suck','play another youll win','most gamblers quit before their big win so keep playing','i dont think this game is for you','did momma give birth so you could lose in blackjack?','cmon you cant lose like that','i am disappointed','do better i know you can']

    async def STARTGAME(self):
        '''be sure to make this function async and add necessary awaits'''
        self.draw_card(dealer=True); self.draw_card(dealer=True)
        await self.channel.send(f"**dealers first card ({self.dealer_hand[0].int_val})**")
        await self.send_card_img([self.dealer_hand[0]])
        await self.channel.send("==================================================================================\n")
        await self.game_loop()
        return self.bet_amnt
    async def send_card_img(self,cards):
        files = [File(open(f"discorddeckpng/{x.face}_{x.suit}.png",'rb'),f"discorddeckpng/{x.face}_{x.suit}.png") for x in cards]
        await self.channel.send(files=files)

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

    def check_user_response(self,msg):
        return (msg.content.startswith('h') or msg.content.startswith('s')) and msg.channel == self.channel
    
    async def bust_phase(self):
        await self.channel.send(self.trash_talk[randint(0,len(self.trash_talk)-1)])
        self.bet_amnt = 0
        return 0
    
    async def winner_phase(self):
        if self.hand_value == 21:
            self.bet_amnt *= 3
        else:
            self.bet_amnt *= 2
        await self.channel.send(f"woo you won {self.bet_amnt} dollars!")
        
    async def dealer_phase(self):
        self.dealer_hand_value = self.get_hand_value(self.dealer_hand)

        await self.channel.send(f"dealer has: {self.dealer_hand_value}")
        await self.send_card_img(self.dealer_hand)

        if self.check_for_bust(self.dealer_hand) == 'bust':
            await self.channel.send(f"dealer busted")
            await self.winner_phase()
            return 0

        if self.dealer_hand_value == self.hand_value and self.dealer_hand_value >= 17:
            await self.channel.send("push")
            return 0

        if self.dealer_hand_value > self.hand_value and self.dealer_hand_value >= 17:
            await self.channel.send(f"you had: {self.hand_value}. dealer had a stronger hand")
            await self.bust_phase()
            return 0
    
        if self.dealer_hand_value >= 17 and self.hand_value > self.dealer_hand_value:
            await self.channel.send(f"dealer must stand, he has {self.dealer_hand_value}")
            await self.winner_phase()
            return 0

        self.draw_card(dealer=True)
        await self.dealer_phase()

    async def game_loop(self):
        self.draw_card()
        self.hand_value = self.get_hand_value(self.hand)

        await self.channel.send(f"you have: {self.hand_value}")
        await self.send_card_img(self.hand)

        if self.check_for_bust(self.hand) == 'bust':
            await self.channel.send('busted')
            await self.bust_phase()
            return 0
        
        await self.channel.send("hit or stand")
        user = await self.client.wait_for('message',timeout=20)

        if user.content.startswith('s'):
            await self.channel.send("**DEALERS TURN**")
            await self.channel.send("==================================================================================\n")
            await self.dealer_phase()

        if user.content.startswith('h'):
            await self.game_loop()
    