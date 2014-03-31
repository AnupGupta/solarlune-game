from bge import logic

def addLight(light_type = 'Point', time = 0, priority = 0):
    
    """
    Spawns a light that was pre-placed in a hidden layer. Note that the light must have a property present
    in it named, "DynPoint", "DynSun", "DynHemi", or "DynSpot" for it to spawn in correctly.
    
    time = how long the light should stick around in frames
    priority = what priority the light should spawn with. Higher priorities will delete and re-create
    (overwrite, if you will) existing lights if not enough pre-made lights are present.
    
    Basically, priority allows you to spawn lights with low
    priority at non important places, like spawn 10 torches with lights at priority 0, and then spawn a light
    for the player with a priority of 1. Since it has a higher priority, the player's light will spawn, and one
    of the torches' lights will be deleted.
    """
    
    sce = logic.getCurrentScene()
        
    obj = logic.getCurrentController().owner
      
    if not hasattr(logic, 'lights_used'):
       
        logic.lights_used = {
        #'Point':{}, 
        #'Sun':{},
        #'Hemi':{},
        #'Spot':{},
        } # Create a mapping of lamps with their types to spawners
            
        #for lt in logic.lights_used:
            
        for l in [l for l in sce.objectsInactive if "DynLight" in l]: # Loop through the lamps that have the string "Dyn" + the type in their name (i.e. Point lamps named "Point", "Point.001", etc.)
            
            if not l['DynLight'] in logic.lights_used:
                
                logic.lights_used[l['DynLight']] = {}
            
            logic.lights_used[l['DynLight']][l.name] = {'reference':None, 'priority':0} # And set their "used" status to 0
              
    for l in logic.lights_used[light_type]: # Then loop through all of the lamps
        
        light_dict = logic.lights_used[light_type][l]
        
        if light_dict['reference'] == None: # And when you find a lamp that hasn't been used
            
            light = sce.addObject(l, obj, time) # Create that lamp,
            
            light_dict['priority'] = priority
            
            light_dict['reference'] = light # And set it to be used (mitts off to all other spawners until it's destroyed)
            
            return light # And then break out of the loop, returning the spawned light
          
        else:
            
            if light_dict['reference'].invalid:
                
                # If the lamp you've "found" is used, but doesn't exist or has been deleted, or has a lower priority
                # than intended,
                
                light = sce.addObject(l, obj, time)
                                                        
                light_dict['reference'] = light # Then re-use that one, rather than looking for another lamp
                
                light_dict['priority'] = priority
                
                return light # And then break out of the loop, returning the spawned light
    
    light_keys = list(logic.lights_used[light_type].keys())

    lights_pri = sorted(light_keys, key = lambda light_in_use: logic.lights_used[light_type][light_in_use]['priority'])
 
    for l in lights_pri:
        
        light_dict = logic.lights_used[light_type][l]
        
        if light_dict['priority'] < priority:
            
            light_dict['reference'].endObject()
            
            light = sce.addObject(l, obj, time)
            
            light_dict['reference'] = light
            
            light_dict['priority'] = priority
            
            return light
       
    return None