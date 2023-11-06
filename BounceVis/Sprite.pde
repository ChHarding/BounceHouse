PVector gGravity = new PVector(0, 0.2);

class Sprite
{
  PVector position;
  PVector offset;
  PVector velocity;
  PVector gravity;
  int size;
  
  Sprite(float x, float y, int s) {
    position = new PVector(x, y);
    offset = new PVector(0, 0);
    gravity = gGravity;
    size = s;
  }

  boolean mouseIn() {
    if (mouseX >= position.x &&
        mouseX <= position.x + size &&
        mouseY >= position.y &&
        mouseY <= position.y + size)
      return true;

    return false;
  }

  void update() {}
  void display() {}
  
  float mouseProximity() {
    float distance = dist(position.x + size/2, position.y + size/2, mouseX, mouseY);
    return distance;
  }
}
