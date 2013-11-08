from bge import logic

def addLight(light_type = 'Point'):
    
    sce = logic.getCurrentScene()
        
    obj = logic.getCurrentController().owner
      
    if not hasattr(logic, 'lights_used'):
       
        logic.lights_used = {
        'Point':{}, 
        'Sun':{},
        'Hemi':{},
        'Spot':{},
        } # Create a mapping of lamps with their types to spawners
            
        for lt in logic.lights_used:
            
            for l in [l for l in sce.objectsInactive if "Dyn" + lt in l]: # Loop through the lamps that have the type in their name (i.e. Point lamps named "Point", "Point.001", etc.)
                
                logic.lights_used[lt][l.name] = 0 # And set their "used" status to 0
                
    for l in logic.lights_used[light_type]: # Then loop through all of the lamps
        
        if logic.lights_used[light_type][l] == 0: # And when you find a lamp that hasn't been used
            
            light = sce.addObject(l, obj) # Create that lamp,
            
            logic.lights_used[light_type][l] = 1 # And set it to be used (mitts off to all other spawners until it's destroyed)

            return light # And then break out of the loop, returning the spawned light
          
        else:
            
            if l not in sce.objects or sce.objects[l].invalid: # If the lamp you've "found" is used, but doesn't exist or has been deleted,
                
                light = sce.addObject(l, obj)
                            
                logic.lights_used[light_type][l] = 1 # Then re-use that one, rather than looking for another lamp
                
                return light # And then break out of the loop, returning the spawned light
          
    return None