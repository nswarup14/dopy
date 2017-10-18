
public class ReducedIDed implements Comparable<ReducedIDed>{
	private String reducedID;
	private int amountBilled;
	public ReducedIDed(String id) {
		reducedID=id;
		amountBilled=20;
	}
	public void increaseAmount() {
		amountBilled+=20;
	}
	@Override
	public int compareTo(ReducedIDed r) {
		return this.reducedID.compareTo(r.getReducedID());
	}
	public String getReducedID() {
		return reducedID;
	}
	public int getAmountBilled() {
		return amountBilled;
	}
	@Override
	public boolean equals(Object o) {
		if(o==this)
			return true;
		ReducedIDed r=(ReducedIDed) o;
		return this.reducedID.equals(r.getReducedID());
	}
}

