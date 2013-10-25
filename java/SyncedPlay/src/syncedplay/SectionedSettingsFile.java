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
import java.util.HashMap;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 *
 * @author kevin
 */
class SectionedSettingsFile {

    HashMap<String, HashMap> dictionary = new HashMap();
    Pattern genericKeyValue = Pattern.compile("(.*)=(.*)");
    Pattern sectionStart = Pattern.compile("\\[(.*)\\]");
    
    public SectionedSettingsFile(String filename) throws FileNotFoundException {
        FileReader fileReader = new FileReader(new File(filename));
        BufferedReader br = new BufferedReader(fileReader);
        ReadData(br);
    }

    private void ReadData(BufferedReader br) {
        String line = null;
        HashMap<String, String> currentsection = null;
        try {
            while ((line = br.readLine()) != null) {

                Matcher startsection = sectionStart.matcher(line);
                Matcher kvmatch = genericKeyValue.matcher(line);

                // Check to see if it matches a start of section
                if (startsection.find()) { //The line is the start of a section
                    currentsection = new HashMap();
                    dictionary.put(startsection.group(1), currentsection);

                } else if (kvmatch.find()) { //The line is a kv pair

                    String key = kvmatch.group(1);
                    String value = kvmatch.group(2);

                    currentsection.put(key, value);
                }
            }
        } catch (IOException ex) {
            Logger.getLogger(SectionedSettingsFile.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
}