package com.solarlune.bdxhelper.input;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.controllers.Controller;
import com.badlogic.gdx.controllers.PovDirection;
import com.nilunder.bdx.Bdx;

import static com.badlogic.gdx.controllers.Controllers.getControllers;

/**
 * Created by SolarLune on 1/7/2015.
 */

public class InputBase {

    static public final int IS_UP = 0;
    static public final int IS_PRESSED = 1;
    static public final int IS_DOWN = 2;
    static public final int IS_RELEASED = 3;

    public int input_state = IS_UP;

    public float active = 0;
    public float past_active = 0;
    public float scalar = 1;

    public Controller controller;  // Used for joystick input types; doesn't
    public PovDirection povDirection;  // make sense to duplicate this across multiple classes

//    public InputBase(int input_type, int keyname){
//
//        this.input_type = input_type;
//        this.keyname = keyname;
//        this.reassignController(joy_index);
//    }
//
//    public InputBase(int input_type, PovDirection povDirection){
//
//        this.input_type = input_type;
//        this.keyname = 0;  // To expand out to multiple hat numbers
//        this.reassignController(joy_index);
//        this.povDirection = povDirection;
//    }

    public void setGamepadIndex(int index){
        this.controller = getControllers().get(index); // For joysticks
    }

    public void poll(){

        if (active != 0){ // Is active

            if (past_active == active)
                input_state = IS_DOWN;
            else
                input_state = IS_PRESSED;
        }
        else{

            if (past_active == active)
                input_state = IS_UP;
            else
                input_state = IS_RELEASED;
        }

        past_active = active;

    }

}
