/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package syncedplay;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.regex.Matcher;

/**
 *
 * @author kevin
 */
public class SectionedSettingsFile extends SettingsFile {
    public SectionedSettingsFile(String filename) throws FileNotFoundException {
      super(filename);
    }
              
    @Override
    void ReadData(BufferedReader br){
        String line = null;
        try {
            while ((line = br.readLine()) != null) {
                /*For each line, read a key-value pair and store it*/
                Matcher matches = genericKeyValue.matcher(line);
                String key = matches.group(1);
                String value = matches.group(2);
                dictionary.put(key, value);
            }
        } catch (IOException e){}
    }
}