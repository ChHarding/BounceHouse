# BounceHouse
A bouncy ball MIDI controller art installation designed, fabricated, and programmed for HCI 584 Python Implementation Fall 2023.
![image](https://github.com/dandegeest/BounceHouse/assets/73483425/ee5f4afd-551b-46ac-a2f8-306eee6b8dd5)
![image](https://github.com/dandegeest/BounceHouse/assets/73483425/86ae4651-b598-4382-84b6-660a2462e244)

An interactive and self-contained art installation using bouncing balls to interact with a custom floor orientated MIDI pad controller consisting of custom fabricated “pads” that will detect ball impact, generate a MIDI note, and send the note to a MIDI compatible sequencer.

## Concept Sketch
![image](https://github.com/dandegeest/BounceHouse/assets/73483425/91c6d74d-1e08-4705-a544-f923754ef3e4)

## Background

I recently started a job at Ames Resource Recovery plant and have been collecting a large assortment of bouncy balls (200) from the plant while I perform my duties as a clean-up laborer.  The balls are prevalent in the plant because their diameter is smaller than the primary shredder teeth and after dropping through they bounce or roll out of the various sorting, sifting, secondary shredding machines, and inclined conveyor belts used to turn garbage into refuse derived fuel that is burned in the natural gas boiler at the Ames Power Plant.

![image](https://github.com/dandegeest/BounceHouse/assets/73483425/2562f369-ee3b-4a7f-be43-fd3c80162b73)

I would like to build an installation that contains sensor pads positioned on the ground that will produce a MIDI note when they are hit by a bouncing ball thrown by the user.  The MIDI will be routed to a synthesizer/sequencer that will play a note/fx based on the current settings of the current sequence and MIDI device.  As the ball bounces it can interact with other pads until coming to rest.  I will experiment with different solutions for how the “spent” balls will be returned to the user.

The pads will also be positioned in a room to allow bouncing interaction with at least two walls (ie: in a corner).  The hope is that one throw of a ball will result in several pad interactions as the ball bounces off walls and the floor/pads.  Meanwhile the user is free to continue to bounce more balls and perhaps even multiple users will be allowed.

## Components:

*Bounce Pads:* I will fabricate custom pads that can be laid out on the ground in various patterns but initially I will just be using a basic grid like current table top MIDI pad controllers. 
![image](https://github.com/dandegeest/BounceHouse/assets/73483425/ca2a90d4-2250-4907-b02b-e40e369c0430)

For the purpose of this class I will build two prototypes to test which thickness of plywood (1/4'' and 1/2'') gives the best bounce/resoance combination.  I want the balls to not have their bounce significantly impacted by hitting the pad but also want to get a good signal from the knock sensor.

![PXL_20231007_224350869](https://github.com/dandegeest/BounceHouse/assets/73483425/2d103c03-17d4-4e05-9da7-1a8d283265b5)
![PXL_20231006_213939401](https://github.com/dandegeest/BounceHouse/assets/73483425/e76db093-e991-4efa-96aa-e4832206df87)
![PXL_20231006_210759816](https://github.com/dandegeest/BounceHouse/assets/73483425/4ee70728-01d4-4032-998f-3f5478f38418)
![PXL_20231006_210600428](https://github.com/dandegeest/BounceHouse/assets/73483425/8742fafb-20fd-4113-9b3e-a3656b1494f5)

For the final installation I would like to use 8 or more pads arranged in various configurations in a dedicated room or installation space.

*Controller:*  [SparkFun Thing Plus - RP2040](https://www.sparkfun.com/products/17745) running https://micropython.org/ will be used to process the pad inputs and translate to MIDI data that will then be sent to the Novation Tracks sequencer using a normal MIDI cable connection.

*Initial Knock Sensor and Board Configuration:*
![PXL_20231019_210658576](https://github.com/dandegeest/BounceHouse/assets/73483425/88e446c6-d64b-4aab-95cd-0bb5dbc97130)
![PXL_20231019_211426438](https://github.com/dandegeest/BounceHouse/assets/73483425/413cd556-6492-40db-96ff-b00248924164)

*Addition of Midi 5PIN output*
![PXL_20231112_233003857](https://github.com/dandegeest/BounceHouse/assets/73483425/73090531-a391-4c40-9bf2-5d68d2e89c59)
Add Midi output connector and updated code to send Midi Note or CC values.

*Synthesizer(s):* The MIDI input will be connected to a [Novation Tracks](https://us.novationmusic.com/products/circuit-tracks) Groovebox.  This is a device I already own and am experienced using it to create music.  There may be an opportunity to also control this device directly from python over usb from a custom desktop application.

I also have a [MicroFreak Synthesizer](https://www.arturia.com/products/hardware-synths/microfreak/overview) that could be controlled by MIDI and I will experiment with this varied gear to determine the best output solution. It also has a control app that could possibly be presented to the user to allow real time adjustments to synth engines, etc.

*Sound:* ROKIT-5-G4 monitor speakers for playback that will be integrated into the installation.

**Programming:**

Python and MicroPython will be used to complete the needed interface(s) and hardware programming respectively.  

Python 3 and the various tools we have been learning in class will be used for testing and other applications as needed.

http://projecessing.org was used to create simple visualizations that can read and write on the serial port to control values on the board and render graphics in conjuction with the midi output.
![bounceHouse0255](https://github.com/dandegeest/BounceHouse/assets/73483425/4e987689-446e-4d29-8e59-6040fcbf6169)

![imageV4002100](https://github.com/dandegeest/BounceHouse/assets/73483425/9e8b76c5-24f1-46db-8a41-d98663cc307a)









