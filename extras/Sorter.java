import java.io.*;
import java.nio.file.Files;
import java.nio.file.StandardCopyOption;
public class Sorter {

	public static void main(String[] args) throws IOException, NullPointerException {
		int count=0;
		
		String input="/media/yashtib1995/Windows8_OS/Users/Yash/Downloads/DoPy Backup/Oasis 114/4. Billed/Final Billed"; //Enter Input Folder
		String output="/media/yashtib1995/Windows8_OS/Users/Yash/Downloads/DoPy Backup/Oasis 114/5. Sorted"; //Enter Output Folder
		
		File in=new File(input);
		File out=new File(output);
		if(!in.isDirectory()||!out.isDirectory()) {
			System.out.println("Error! Enter a valid input, output directory!");
			System.exit(0);
		}
		for(File rolls: in.listFiles()) {
			if(rolls.isDirectory()) {
				for (File img: rolls.listFiles()) {
					String bhawan=img.getName().substring(0,2);
					File a=new File(output+"/"+bhawan);
					if(!a.exists())
						a.mkdir();
					Files.copy(img.toPath(), (new File(a+"/"+img.getName())).toPath(), StandardCopyOption.REPLACE_EXISTING);
					count++;
				}
				System.out.println(rolls.getName());
			}
		}
		System.out.printf("Total snaps = %d",count);
	}

}

