import processing.serial.*;
import garciadelcastillo.dashedlines.*;

String[] columns = {"Timestamp", "Command"}; // Modify this array to match your data
String filename = "data/data.csv"; // Name of the CSV file to save
DataManager data;
String version = "V4";

DashedLines dash;
float dashDist = 0;
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
float delay = 0;
int octave = 0;

void setup()
{
  size(1200, 800);
  //fullScreen();
  gridX = width / ss;
  gridY = height / ss;
  frameRate(30);
  
  x = width/2;
  y = height/2;
  
  dash = new DashedLines(this);
  dash.pattern(30, 10);
  
  data = new DataManager();
  data.createCsvFile(columns);

  printArray(Serial.list());
  int comPort = -1;
  String[] ports = Serial.list();
  for (int i = 0; i < ports.length; i++) {
    if (ports[i].equals("COM6")) {
      comPort = i;
      break; // If found, exit the loop
    }
  }
  
  if (comPort > 0) {
    println("OPENPORT:", Serial.list()[comPort]);
    sPort = new Serial(this, Serial.list()[comPort], 9600);
  }
  
  background(0);
}

void exit() {
  data.saveFile(filename);
  sPort.stop();
  sPort.dispose();
}

void draw() {
  if (knock < 50)
    background(0);
     
  if (knock > 0)
    draw1();
  
  if (knock > 1000)
    draw2();
  
  if (delay > 5)
    draw3();
  
  if (frameCount % 300 == 0) {
    x = (int)random(0, width);
    y = (int)random(0, height);
    //factor = random(1, 4);
    print("Saving");
    saveFrame("frames/image" + version + "######.png");
  }
  
  currS++;
  if (currS > gridX)  {
    currS = 0;
    currY += ss;
  }
  
  if (currY > height) {
    currY = 0;
    background(0);
  }

  if (knock > 100)
    knock -= 25;
}

void draw1() {
  ellipseMode(CENTER);
  float f = map(knock, 0, 5000, 0, 255);
  stroke(f, abs(255 - f), random(255));
  fill(f, abs(255 - f), random(255));
  if (knock > 1000)
  {
    noFill();
    rect(currS * ss, currY, f, f);
  }
  else
    ellipse(currS * ss, currY, f, f);
}

void draw2() {  
  ellipseMode(CENTER);
  rectMode(CENTER);
  float c = map(knock, 0, 5000, 0, 255) * factor;
  float s = map(knock, 0, 5000, 0, 500);
  //float s = map(angleY, 0, 1000, 20, 0);
  noFill();
  strokeWeight(1 * factor);
  stroke(c, abs(255 - c), random(255));
  
  if (knock % 2 == 0)
  {
    //fill(f, abs(255 - f), random(255));
    rect(x, y, s, s, c);
  }
  else
    ellipse(x, y, s, s/2);
}

void draw3() {
   noFill();
   stroke(delay, 255-delay, 255 % delay);
   strokeCap(SQUARE);
   dash.pattern(delay, 10);
   strokeWeight(1);
   //dash.line(currS * ss, currY, mouseX, mouseY);
   if (knock > 1500) {    
     //background(#FF9001);
     dash.bezier(0, 0, random(width), random(height), currS * ss, currY, width, 0);
   }
   else
     dash.bezier(0, height, random(width), random(height), currS * ss, currY, width, height);
   
   dash.offset(dashDist);
   dashDist += 1;
}

void mousePressed() {
  if (mouseButton == LEFT) {
    int r = (int)map(mouseX, 0, width, 0, 127);
    sPort.write("CC:" + "111:15:" + r + "\n");
  }
  else if (mouseButton == RIGHT) { 
  }
}

void keyPressed() {
  if (keyCode == LEFT) {
    octave += 10;
    sPort.write("OCTAVE:" + octave + "\n");
  }
  
  if (keyCode == RIGHT) {
    octave -= 10;
    sPort.write("OCTAVE:" + octave + "\n");
  }
  
  if (keyCode == ENTER) {
    saveFrame("screens\\photoTile####.png");
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
    //Record it
    String[] values = new String[2];
    values[0] = Long.toString(System.currentTimeMillis());
    values[1] = inString;
    data.addRow(values);
    // Process the command
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
  knock = k; //map(k, 0, 65536, 0, 5000);
}

void onControlChange(int cc, int channel, float value) {
  if (value > 0) {
    if (cc == 111) {
      delay = value;
    }
  }
}
