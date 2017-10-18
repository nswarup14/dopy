import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import au.com.bytecode.opencsv.CSVReader;
import au.com.bytecode.opencsv.CSVWriter;

class PhotoboothBiller {
	public static void main(String[] args) throws IOException {
		String ssms="/home/yashtib1995/Desktop/Biller/ssms.csv";		//Enter Absolute Path of File ssms
		String csv="/home/yashtib1995/Desktop/Biller/pb3.csv";		//Enter Absolute Path of File csv
		String output="/home/yashtib1995/Desktop/Biller/output.csv";	//Enter Absolute Path of File output
		List<Student> list=new ArrayList<Student>();
		CSVReader in=new CSVReader(new FileReader(new File(ssms)),',');
		Boolean flag=true, flag2=true;
		do {
			try {
				String[] a=in.readNext();
				Student b=new Student(a[2],a[1],a[4],Integer.parseInt(a[5]));
				list.add(b);
			}
			catch(Exception e) {
				flag=false;
			}

		} while(flag);
		in.close();
		Collections.sort(list);
		CSVReader amounts=new CSVReader(new FileReader(new File(csv)),',');
		do {
			try {
				String[] a=amounts.readNext();
				Student t=new Student(a[1]);
				int index=Collections.binarySearch(list , t);
				if(index>=0)
					list.get(index).increaseAmountBilled();
				else
					System.out.println(a[1]);
			}
			catch(Exception e) {
				flag2=false;
			}

		} while(flag2);
		amounts.close();
		int counter=1,sum=0;
		CSVWriter out=new CSVWriter(new FileWriter(output),',');
		for(int i=0;i<list.size();i++) {
			Student st=list.get(i);
			if(!st.getAmountBilled().equals("0"))	{
				String[] toWrite=new String[6];
				toWrite[0]=Integer.toString(counter++); //S. No.
				toWrite[1]=st.getName();
				toWrite[2]=st.getID();
				toWrite[3]=st.getHostel();
				toWrite[4]=st.getRoomno();
				toWrite[5]=st.getAmountBilled();
				sum+=Integer.parseInt(st.getAmountBilled());
				out.writeNext(toWrite);
			}
		}
		out.close();
		System.out.println("Done "+sum);
	}
}
