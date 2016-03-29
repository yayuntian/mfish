import java.io.*;
import java.util.Map.Entry;
import java.util.Set;

import org.ini4j.InvalidFileFormatException;
import org.ini4j.Profile.Section;
import org.ini4j.Wini;
public class ReadSectionIni {
  public static void main(String[] agrs) {
    try {
      Wini ini = new Wini(new File("config/properties.ini"));
      Set<Entry<String, Section>> sections = ini.entrySet(); /* !!! */

            for (Entry<String, Section> e : sections) {
                Section section = e.getValue();
                System.out.println("[" + section.getName() + "]");

                Set<Entry<String, String>> values = section.entrySet(); /* !!! */
                for (Entry<String, String> e2 : values) {
                    System.out.println(e2.getKey() + " = " + e2.getValue());
                }
            }
            
        } catch (InvalidFileFormatException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
  }
}
