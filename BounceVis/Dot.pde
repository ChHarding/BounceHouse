class Dot extends Bouncy
{
  boolean isDone = false;
  // Anchor
  Dot anchor;
  PVector clickLoc;
  PVector control1;
  color dotColor;
  
  Dot(int xx, int yy, int ss) {
    super(xx, yy, ss);
    isDone = false;
    dotColor = color(#219ebc);
    control1 = new PVector(width/2, height/2);
  }
  
  void setAnchor(Dot a) {
    anchor = a;
    anchor.dotColor = color(#023047);
  }
  
  void clicked(int x, int y) {
    clickLoc = new PVector(x,y);
  }
  
  void bounce(PVector velo, float ls) {
    super.bounce(velo, ls);
    if (anchor != null)
      anchor.bounce(new PVector(0, random(100, 200)), ls);
  }  
  
  boolean mouseIn() {
    if (mouseX >= position.x - size/2 &&
      mouseX <= position.x + size/2 &&
      mouseY >= position.y - size/2 &&
      mouseY <= position.y + size/2)
      return true;

    return false;
  }
  
  void update() {
    super.update();
    if (anchor != null)
      anchor.update();  
  }
  
  void display() {
    drawAnchor();
    
    noStroke();
    
    if (mouseIn()) {
      strokeWeight(4);
      stroke(255, 255, 0, 100);
    }
    
    fill(dotColor);
    int whatSize = isDone ? size * 2 : size;
    ellipse(position.x, position.y, whatSize, whatSize);
  }
  
  void drawAnchor() {
    if (anchor == null)
      return;
    
    anchor.display();
    
    stroke(dotColor); //#fb8500);
    strokeWeight(1);
    noFill();
    bezier(position.x, position.y,
      control1.x, control1.y,
      height/2, width/2,
      anchor.position.x, anchor.position.y);
    
    noStroke();
    fill(dotColor, map(dist(position.x, position.y, anchor.position.x, anchor.position.y), 0, height, 0, 255));
    int steps = 50;
    for (int i = 0; i <= steps; i++) {
      float t = i / float(steps);
      float x = bezierPoint(position.x, control1.x, control1.y, anchor.position.x, t);
      float y = bezierPoint(position.y, height/2, width/2, anchor.position.y, t);
      ellipse(x, y, 10, 10);
    }
  }
  
  void done() {
    isDone = true;
  }
}
