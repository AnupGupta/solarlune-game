from bge import logic

class Scenes:
    
    def __str__(self):
        return str(logic.getSceneList())
    
    def __len__(self):
        return len(logic.getSceneList())




    def __iter__(self):
        return iter(logic.getSceneList())
    
    def __contains__(self, key):
        if isinstance(key, str):
            return True if key in {s.name for s in logic.getSceneList()} else False
        raise TypeError('must be str, not ' + type(key).__name__)
    
    def __getitem__(self, key):
        scenes = logic.getSceneList()
        if isinstance(key, str):
            return {s.name: s for s in scenes}[key]
        return scenes[key]




    def set(self, key):
        logic.getCurrentScene().replace(key)
        
    def add(self, key, overlay=True):
        logic.addScene(key, overlay)
        
    def remove(self, key):
        self.__getitem__(key).end()
        
    def leave(self, *args):
        
        """
        Ends all scenes except the ones you specify.
        arguments = the names of the scenes you want to leave
        """           
        for scene in logic.getSceneList():
            if not scene.name in args:
                scene.end()
            
logic.scenes = Scenes()