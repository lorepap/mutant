class ConfigModel(object):

    def __init__(self, obj: dict) -> None:
        super().__init__()
        
        self.obj = obj


    
    @property
    def models(self) -> list:
        return self.obj['models'] if self.obj != None else []