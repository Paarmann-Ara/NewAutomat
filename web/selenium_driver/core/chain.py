# ad = ActionChain()
# ad.chains=('txb_suchen', 'click')
# ad.chains=('btn_confirm', 'click')

# ad.pop(1)
# ad.update(0,('txb_suchen', 'click'))
# ad.sort()

class Chain:
    # chains={"id":(element, action)}
    def __init__(self, tuple_action: tuple = None) -> None:
        self._chains = {}
        self.chains = tuple_action

# --
# ... curd
# --

    @property
    def chains(self) -> tuple:
        return self._chains

    @chains.setter
    def chains(self, tuple_action: tuple, id=None):
        if not tuple_action:
            return
        
        if id and id not in self._chains:
            self._chains.update(
                {str(id): tuple_action})

        else:
            self._chains.update(
                {str(len(self._chains)): tuple_action})

    def pop(self, id):
        self._chains.pop(str(id))

    def update(self, id:int, tuple_action: tuple):
        self._chains.pop(str(id))
        self._chains.update({str(id):tuple_action})
        self.sort()
        
    def add_new_chain(self, new_chain):
        self._chains.update(new_chain)
        
# --
# ... utility
# --

    def get_chains_ids_list(self) -> list:
        return list(self._chains.keys())
    
    def sort(self):
        self._chains= dict(sorted(self._chains.items()))
# --
# ... presentation
# --

    def __repr__(self)->str:
        return f"{self.__class__.__name__}({self._chains})"
        
# --
# ... itr
# --

    def __len__(self)->int:
        return len(self.chains)

    def __getitem__(self, id)->tuple:
        
        try:
            return self.chains[str(id)]
        
        except KeyError:
            raise StopIteration
