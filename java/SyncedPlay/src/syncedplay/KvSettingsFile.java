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

//TODO Work was pasued on this. Fix this file.

/*
 * 
 * 
re_startsection = re.compile(r"\[(.*)\]")
re_data = re.compile(r"\_(.*)=(.*)")
re_generickeyvalue = re.compile(r"(.*)=(.*)")
re_command = re.compile(r"\^(.*)=(.*)")
re_comment = re.compile(r"#.*$")

 */
 abstract class KvSectionsFile extends SettingsFile {

    Pattern genericKeyValue = Pattern.compile("(.*)=(.*)");
    HashMap<String, String> dictionary = new HashMap();
    /** This initializer will read the file and generate the keyvalue dictionary based upon what it reads */
    public KvSectionsFile(String filename) throws FileNotFoundException, IOException {
        /*get a handle on the file */
        
        /* Read each line */
    }
    
    private ReadData(BufferedReader br){
        String line = null;
        while ((line = br.readLine()) != null) {
            /*For each line, read a key-value pair and store it*/
            Matcher matches = genericKeyValue.matcher(line);
            String key = matches.group(1);
            String value = matches.group(2);
            dictionary.put(key, value);
        }
    }
}
