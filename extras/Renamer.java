package renamer;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.StandardCopyOption;
/* REnamer :
 * Assumes no fuck ups with numbering of snaps ie all snaps must be of format DSC_xxx.jpg
 * All rolls must start with 001/041/081...
 * Renames the snaps in its destination hence, make a backup in case of fuckups
 */
public class Renamer {

	public static void main(String[] args) throws IOException {
		String input="/home/yashtib1995/Desktop/2. Autoed"; //Enter Input Folder

		File in=new File(input);
		if(!in.isDirectory()) {
			System.out.println("Error! Enter a valid input, output directory!");
			System.exit(0);
		}
		for(File rolls: in.listFiles()) {
			if(rolls.isDirectory()) {
				for (File img: rolls.listFiles()) {
					int count=Integer.parseInt(img.getName().replaceAll("[^0-9]",""))%40;
					if(count==0)
						count=40;
					String roll=rolls.getName().substring(0,rolls.getName().indexOf('R')+1);
					String count1;
					if(count/10==0)
						count1="0"+Integer.toString(count);
					else
						count1=Integer.toString(count);
					File dest=new File(img.getParentFile().getPath()+"/"+roll+count1);	
					img.renameTo(dest);
				}
				System.out.println(rolls.getName());
			}
		}

	}
}
