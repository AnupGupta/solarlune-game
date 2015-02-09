package com.solarlune.bdxhelper.choice;

import java.util.ArrayList;

/**
 * Created by SolarLune on 1/28/2015.
 */
public class Screen {

    String name;
    ArrayList<Choice> choices;
    public boolean active = true;
    int currentChoiceIndex = 0;

    public Screen(String name){
        choices = new ArrayList<Choice>();
    }
    public Screen(){
        this("default");
    }

    public void add(Choice c){
        choices.add(c);
    }

    public void remove(Choice c){
        choices.remove(c);
    }

    public void nextChoice(){
		if (active) {
			currentChoiceIndex += 1;
			enforceBounds();
		}
    }

    public void prevChoice(){
		if (active) {
			currentChoiceIndex -= 1;
			enforceBounds();
		}
    }

    public void setChoice(int index){
		if (active) {
			currentChoiceIndex = index;
			enforceBounds();
		}
    }

    public void enforceBounds(){

        if (currentChoiceIndex >= choices.size()){
            currentChoiceIndex -= choices.size();
        }
        if (currentChoiceIndex < 0){
            currentChoiceIndex += choices.size();
        }

    }

    public Choice currentChoice(){
        enforceBounds();
        if (currentChoiceIndex >= 0 && currentChoiceIndex < choices.size())
            return choices.get(currentChoiceIndex);

        return null;
    }

}
