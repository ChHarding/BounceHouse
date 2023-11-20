import processing.serial.*;

Serial sPort;
float knock = 0;
String message;

int currS = 0;
int currY = 0;
int gridX = 0;
int gridY = 0;

int x;
int y;

int ss = 50;

float factor = 1;

void setup()
{
  size(1200, 800);
  fullScreen();
  gridX = width / ss;
  gridY = height / ss;
  frameRate(10);
  
  x = width/2;
  y = height/2;
  

  printArray(Serial.list());
  sPort = new Serial(this, Serial.list()[2], 9600);
  background(0);
}

void draw() {
  if (knock < 50)
    background(0);
        
  draw1();
  
  if (knock > 300)
    draw2();
  
  if (frameCount % 50 == 0) {
    x = (int)random(0, width);
    y = (int)random(0, height);
    //factor = random(1, 4);
    saveFrame("frames/image######.png");
  }
  
  if (knock > 100)
    knock -= 25;
}

void draw1() {
  if (knock > 0) {
    ellipseMode(CORNER);
    float f = map(knock, 100, 600, 5, 200);
    stroke(f, abs(255 - f), random(255));
    fill(f, abs(255 - f), random(255));
    if (knock % 10 == 0)
      noStroke();
    else
      noFill();
    //rect(currS * ss, currY, ss, ss);
    ellipse(currS * ss, currY, f, f);
  }
  
  currS++;
  if (currS > gridX)  {
    currS = 0;
    currY += ss;
  }
  
  if (currY > height) currY = 0;
}


void draw2() {  
  ellipseMode(CENTER);
  rectMode(CENTER);
  float f = map(knock, 100, 600, 0, 255) * factor;
  //float s = map(angleY, 0, 1000, 20, 0);
  noFill();
  strokeWeight(5 * factor);
  stroke(f, abs(255 - f), random(255));
  
  if (knock % 10 == 0)
  {
    fill(f, abs(255 - f), random(255));
    rect(x, y, floor(knock) * factor, floor(knock) * factor, f);
  }
  else
    ellipse(x, y, floor(knock) * factor, floor(knock) * factor);
}

void mousePressed() {
  if (mouseButton == LEFT) {
    int r = (int)map(mouseX, 0, width, 0, 127);
    sPort.write("CC:" + "111:15:" + r + "\n");
  }
  else if (mouseButton == RIGHT) { 
  }
}

void mouseWheel(MouseEvent event) {
  // Adjust the scale factor based on the mouse wheel movement
  float delta = event.getCount();
  if (delta > 0) factor += .1;
  else factor -= .1;
  println("D", factor);
}

void serialEvent(Serial port) {
  //Read from port
  String inString = port.readStringUntil('\n');
  if (inString != null) {
    //Trim
    inString = inString.trim();
    String[] command = inString.split(":");
    switch(command[0]) {
      case "KNOCK":
        //println(inString);
        onKnockCommand(float(command[1]));
        break;
      case "EXTCMD":
        println(inString);
        break;
      case "CC":
        println(inString);
        onControlChange(int(command[1]), int(command[2]), float(command[3]));
    }
  }
}

void onKnockCommand(float k) {
  println("KNOCK:", k);
  knock = k;
}

void onControlChange(int cc, int channel, float value) {
  if (value > 0) {
    if (cc == 111) {
    }
  }
}
