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
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/** This class stores data about settings files.
 *
 * @author kevin
 */
abstract class SettingsFile {

    Pattern genericKeyValue = Pattern.compile("(.*)=(.*)");
    HashMap<String, Object> dictionary = new HashMap();

    /** This initializer will read the file and generate the keyvalue dictionary based upon what it reads */
    public SettingsFile(String filename) throws FileNotFoundException {
        /*get a handle on the file */

        FileReader fileReader = new FileReader(new File(filename));
        BufferedReader br = new BufferedReader(fileReader);
        ReadData(br);
        /* Read each line */
    }

    abstract void ReadData(BufferedReader br);

    Object GetSetting(String key) {
        return dictionary.get(key);
    }
}