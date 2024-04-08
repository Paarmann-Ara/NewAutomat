# import sys

# def te():
#     print("ich bin te")
    
# methode = "MainMenu_Start_" + "BenutzerWechseln" + "_Test"
# val = te
# setattr(sys.modules[__name__], methode,val)

# MainMenu_Start_BenutzerWechseln_Test()

class card:
    def __init__(self, rank, suit) -> None:
        self.rank=rank
        self.suit=suit
        
    def __repr__(self) -> str:
        return f"{__class__.__name__}(rank={self.rank}, suit={self.suit})"
    
class cards:
    def __init__(self) -> None:
        rank=['1','2','3','4','5','6','7','8','9','J','Q','K']
        suit=['clubs', 'speard', 'hart', 'diamond']
        self.cards = [card(r,s) for r in rank for s in suit]
    
    def __len__(self):
        return len(self.cards)
    
    def __getitem__(self, item):
        return self.cards[item]
    
print(cards().cards[0])