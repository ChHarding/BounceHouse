import processing.serial.*;

Serial sPort;
ArrayList<Marble> delays = new ArrayList<Marble>();

int screenX = 1200;
int screenY = 800;

int numDots = 20;
int currDot = 0;
int currFrame = 0;

color backColor = color(#8ecae6);

boolean auto = true;

int holdCount = 0;

ArrayList<Dot> dots = new ArrayList<Dot>();
Dot mouseDot;

void setup() {
  size(1200, 800);
  fullScreen();

  hint(ENABLE_STROKE_PURE);
  frameRate(30);
  background(backColor);
  initDots();

  printArray(Serial.list());
  sPort = new Serial(this, Serial.list()[2], 9600);
}

void draw() {
  background(backColor);
  
  if (mouseDot != null) {
    holdCount++;
  
    if (holdCount > 1) {
      //PVector v = new PVector(random(3) * random(-1,1), random(50) * random(-5,5));
      PVector v = new PVector(mouseX - mouseDot.clickLoc.x, mouseY - mouseDot.clickLoc.y);
      if (mouseX > mouseDot.clickLoc.x)
        v = new PVector(-v.x, v.y);
      if (mouseY > mouseDot.clickLoc.y)
        v = new PVector(v.x, -v.y);

      v.normalize().mult(random(15,80));
      v = PVector.random2D();
      v.mult(20);
      println(v);
      mouseDot.bounce(v, 300);
      mouseDot = null;
    }
  }

  for (int i = 0; i < dots.size(); i++) {
    Dot dot = dots.get(i);
    dot.update();
  }

  for (int i = 0; i < dots.size(); i++) {
    dots.get(i).display();
  }
  
  for (int i = delays.size() - 1; i >= 0; i--) {
    Marble s = delays.get(i);
    s.update();
    s.display();
    
    if (s.diameter <= 5)
      delays.remove(i);
  }
}

void initDots() {
  for (int i = 0; i < numDots; i++) {
    int x = (int)map(i, 0, numDots, 0, width);
    Dot dot = new Dot(x + 40, 10, 40);
    Dot anchor = new Dot(x + 40, height - 40, 40);
    dot.setAnchor(anchor);
    dots.add(dot);
    //dots.add(anchor);
  }
}

void mousePressed() {
  if (mouseButton == LEFT) {
    if (mouseDot != null) {
      mouseDot = null;
    }
  
    holdCount = 0;
    
    for (int i = 0; i < dots.size(); i++) {
      Dot dot = dots.get(i);
      dot.control1 = new PVector(mouseX, mouseY);
      dot.bounce(PVector.random2D(),5);
      if (dot.mouseIn()) {
        mouseDot = dot;
        mouseDot.clicked(mouseX, mouseY);
        break;
      }
    }
  }
  else if (mouseButton == RIGHT) {
  }
}

void keyPressed() {
}

void mouseMoved() {
  if (mouseDot != null) {
    holdCount = 0;
    mouseDot.position = new PVector(mouseX, mouseY);
  }
}

void serialEvent(Serial port) {
  //Read from port
  String inString = port.readStringUntil('\n');
  if (inString != null) {
    //Trim
    inString = inString.trim();
    //println(inString);
    String[] command = inString.split(":");
    switch(command[0]) {
      case "KNOCK":
        onKnockCommand(float(command[1]));
        break;
      case "CC":
        onControlChange(int(command[1]), int(command[2]), float(command[3]));
    }
  }
}

void onKnockCommand(float k) {
  float t = 1000;
  if (k < t)
    return;
  
  if (currDot == dots.size())
    currDot = 0;
  
  Dot dot = dots.get(currDot);
  if (!dot.animating()) {
    PVector v = PVector.random2D();
    v.normalize();
    //v.mult(k);
    dot.bounce(v, 300);
  }
  
  dot.dotColor = color(map(k, t, 3000, 0, 255), random(255), blue(dot.dotColor));
  currDot++;
}

void onControlChange(int cc, int channel, float value) {
  if (value > 0) {
    Marble m = new Marble((int)random(width), (int)random(height), (int)value * 5, StripeOrientaion.Horizontal);
    m.bounce(PVector.random2D(), value);
    delays.add(m);
  }
}
