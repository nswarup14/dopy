class Student implements Comparable<Student> {
	private String name;
	private String ID;
	private String hostel;
	private int roomno;
	private int amountBilled;
	private String reducedID;

	public Student (String name, String ID, String hostel, int roomno) {
		this.name=name;
		this.ID=ID;
		this.hostel=hostel;
		this.roomno=roomno;
		setReducedID();
		amountBilled=0;
	}
	public Student(String reducedID) {
		this.reducedID=reducedID;
		name=new String();
		ID=new String();
		hostel=new String();
		roomno=0;
		amountBilled=0;
	}
	public int compareTo(Student other) {
		return this.reducedID.compareToIgnoreCase(other.getReducedID());
	}
	public String getReducedID() {
		return reducedID;
	}
	public String getName() {
		return name;
	}
	public String getID() {
		return ID;
	}
	public String getHostel() {
		return hostel;
	}
	public String getRoomno() {
		return Integer.toString(roomno);
	}
	public String getAmountBilled() {
		return Integer.toString(amountBilled);
	}
	private void setReducedID() {
		try {
			if(ID.charAt(4)=='H'||ID.charAt(4)=='h')
				reducedID="m"+ID.substring(2,4)+ID.substring(8,11);
			else if(ID.charAt(4)=='P'||ID.charAt(4)=='p')
				reducedID="p"+ID.substring(2,4)+ID.substring(8,11);
			else
				reducedID=ID.substring(2,4)+ID.substring(8,11);

		}
		catch (Exception e) {
			e.printStackTrace();
		}
	}
	public void increaseAmountBilled() {
		amountBilled+=25;
	}
	@Override
	public boolean equals(Object o) {
		if(o==this)
			return true;
		Student t=(Student) o;
		return this.reducedID.equalsIgnoreCase(t.getReducedID());
	}
}
