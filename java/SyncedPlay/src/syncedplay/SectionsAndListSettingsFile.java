/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package syncedplay;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 *
 * @author kevin
 */
class Cue {

    String name;
    ArrayList<String> commands = new ArrayList();
    
    public Cue(String name) {
        this.name = name;
    }
    
    void addCommand(String command) {
        this.commands.add(command);
    }
    
    @Override
    public String toString() {
        StringBuilder s = new StringBuilder("Cue " + this.name + ":" + this.commands.toString());
        return s.toString();
    }
}

class SectionsAndListSettingsFile {
    
    ArrayList<Cue> dictionary = new ArrayList();
    Pattern genericKeyValue = Pattern.compile("(.*)=(.*)");
    Pattern sectionStart = Pattern.compile("\\[(.*)\\]");
    
    public SectionsAndListSettingsFile(String filename) throws FileNotFoundException {
        FileReader fileReader = new FileReader(new File(filename));
        BufferedReader br = new BufferedReader(fileReader);
        ReadData(br);
    }
    
    private void ReadData(BufferedReader br) {
        String line = null;
        Cue currentCue = null;
        try {
            while ((line = br.readLine()) != null) {
                Matcher startsection = sectionStart.matcher(line);
                // Check to see if it matches a start of section
                if (startsection.find()) { //The line is the start of a section
                    currentCue = new Cue(startsection.group(1));
                    dictionary.add(currentCue);
                } else { //The line is a command
                    currentCue.addCommand(line);
                }
            }
        } catch (IOException ex) {
            Logger.getLogger(SectionsAndListSettingsFile.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
}
