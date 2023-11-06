class Bouncy extends Sprite {
  float animateLifeSpan;
  
  Bouncy(float x, float y, int s) {
    super(x, y, s);
  }
  
  void bounce(PVector velo, float ls) {
    velocity = velo;
    animateLifeSpan = ls;
  }
   
  boolean doneBouncing() { return onGround(); }
  boolean onGround()
  {
    return position.y + size > height;
  }
  
  boolean animating() {
    return animateLifeSpan > 0;
  }
  
  void update() {
    if (animateLifeSpan > 0) {
      // Update the bounce animation
      velocity.add(gGravity);
      position.add(velocity);
      if (onGround())
        animateLifeSpan -= 1;
      
      if (animateLifeSpan > 0) {
        //Contrain to canvas edges
        if (position.x > width - size || position.x < size) {
          velocity.x *= -1; // Reverse horizontal velocity on wall collision
        }
        if (position.y > height - size) {
          position.y = height - size;
          velocity.y *= -0.8; // Reverse and dampen vertical velocity on ground collision
        }
      }
    }
  }
}
