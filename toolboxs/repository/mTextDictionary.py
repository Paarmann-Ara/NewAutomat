class cTextDictionary:
    def __call__(self) -> dict:
        self.dictionary = {
            'Number4Character': '9999',
            'Number9Character': '123456789',
            'TextTest': 'Simple Data 512',
            'TextJustSondernChar': '!"°!"§$%&/}{³²~µ|>,;:_-.</*-+"y!"#$%&''()*+-./0=?[\]^',
            'Text10Character': '10%!"°!"§$',
            'Text14Character': '14"%r!"§$&/?}ue',
            'Text30Character': '30 !"°!"§$%&/?`´ß^\}{³²~µ|>,;:',
            'Text62Character': '62 !"°!"§$%&/?`´ß^\}{³²~µ|>,;:_-.</*-+"y!"#$%&''()*+-./0=?[]',
            'Text64Character': '64 !"°!"§$%&/?`´ß^\}{³²~µ|>,;:_-.</*-+"y!"#$%&''()*+-./0=?[\]^',
            'Text255Character': 'Simple Data 255 Character Simple Data Simple Data Simple Data Simple Simple D ° ! " ° !"§$%&/()=?`´ß0987654321^\}][{³²~µ|>YXCVBNM;:_-.,mnbvcxy<123/*-+"y!"#$%&''()*+,-./01:;<=>?PZ[\]^p@Ayz{|}~._qwertzuiopüasdfghjklöä#y,.12300,789/*-+üöä-|<<>',
            'Text512Character': 'Simple Data 255 Character Simple Data Simple Data Simple Data Simple Simple D ° ! " ° !"§$%&/()=?`´ß0987654321^\}][{³²~µ|>YXCVBNM;:_-.,mnbvcxy<123/*-+"y!"#$%&''()*+,-./01:;<=>?PZ[\]^p@Ayz{|}~._qwertzuiopüasdfghjklöä#y,.12300,789/*-+üöä-|<<>' * 2,
            'Text1024Character': 'Simple Data 255 Character Simple Data Simple Data Simple Data Simple Simple D ° ! " ° !"§$%&/()=?`´ß0987654321^\}][{³²~µ|>YXCVBNM;:_-.,mnbvcxy<123/*-+"y!"#$%&''()*+,-./01:;<=>?PZ[\]^p@Ayz{|}~._qwertzuiopüasdfghjklöä#y,.12300,789/*-+üöä-|<<>' * 4,
            'Text10000Character': 'Simple Data 255 Character Simple Data Simple Data Simple Data Simple Simple D ° ! " ° !"§$%&/()=?`´ß0987654321^\}][{³²~µ|>YXCVBNM;:_-.,mnbvcxy<123/*-+"y!"#$%&''()*+,-./01:;<=>?PZ[\]^p@Ayz{|}~._qwertzuiopüasdfghjklöä#y,.12300,789/*-+üöä-|<<>' * 40,
        }
        
        return self.dictionary