package com.solarlune.bdxhelper.input;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

/**
 * Created by SolarLune on 1/7/2015.
 */

public class InputMap {

    static public HashMap<String, ArrayList<InputBase>> bindings = new HashMap<String, ArrayList<InputBase>>();
    static public HashMap<String, ArrayList<Float>> results = new HashMap<String, ArrayList<Float>>();

    private InputMap(){
    }

    static public void addBinding(String bindingName, InputBase inputBase){

        if (!bindings.containsKey(bindingName))
            bindings.put(bindingName, new ArrayList<InputBase>());

        ArrayList<InputBase> binding = bindings.get(bindingName);

        binding.add(inputBase);

    }

    static public float bindDown(String bindName){

        if (results.containsKey(bindName)){

            ArrayList<Float> res = results.get(bindName);

            return res.get(0);

        }

        return 0;
    }

    static public boolean bd(String bindName){

        return bindDown(bindName) != 0;

    }

    static public float bindPressed(String bindName){

        if (results.containsKey(bindName)){

            ArrayList<Float> res = results.get(bindName);

            if (res.get(1) == (float) InputBase.IS_PRESSED)

                return res.get(0);
        }

        return 0;
    }

    static public boolean bp(String bindName){

        return bindPressed(bindName) != 0;

    }

    static public float bindReleased(String bindName) {

        if (results.containsKey(bindName)){

            ArrayList<Float> res = results.get(bindName);

            if (res.get(1) == (float) InputBase.IS_RELEASED)

                return res.get(0);

        }

        return 0;
    }

    static public boolean br(String bindName){

        return bindReleased(bindName) != 0;

    }

    static public void poll(){

        for (Map.Entry<String, ArrayList<InputBase>> entry : bindings.entrySet() ) {

            ArrayList<Float> ar = new ArrayList<Float>();
            ar.add(0.0f);  // Active value
            ar.add(0.0f);  // State
            results.put(entry.getKey(), ar);

            for (InputBase ik : bindings.get(entry.getKey())) {

                ik.poll();

                ArrayList<Float> res = results.get(entry.getKey());

                if ((ik.active != 0) || (ik.input_state != ik.IS_UP)) {

                    res.clear();
                    res.add(ik.active);
                    res.add((float) ik.input_state);
                }
            }
        }

    }

}
