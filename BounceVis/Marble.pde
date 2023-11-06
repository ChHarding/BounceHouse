enum StripeOrientaion {
  Horizontal,
  Vertical
};

class Marble extends Dot
{
  float diameter;
  int dir = 1;
  int dirDur = 0;
  int dirDurMax = (int)frameRate;
  int step = 10;
  StripeOrientaion stripe;
  
  Marble(int x, int y, int d, StripeOrientaion s) {
    super(x, y, d / 2);
    diameter = d;
    stripe = s;
  }
  
  void display() {
    super.display();
    noFill();
    //shapeColor = color(random(255), random(255), random(255));
    //stroke(shapeColor);
    //noStroke();
    ellipse(position.x, position.y, diameter, diameter);
    
    stripe = position.x % 2 == 0 ? StripeOrientaion.Horizontal : StripeOrientaion.Vertical;
    
    float stripeDiameter = diameter;
    while (stripeDiameter > 5)
    {
      stroke(random(255), random(255), random(255));
      switch(stripe) {
        case Horizontal:
          ellipse(position.x, position.y, diameter,stripeDiameter);
          break;
        case Vertical:
          ellipse(position.x, position.y, stripeDiameter,diameter);
          break;
      };
      stripeDiameter -= 5;
    }
  }  
}
