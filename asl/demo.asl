/**
 * Demo BDI program for AirSim car
 * This example BDI program performs the action
 * 'throttle(5)' whenever it receives a perception 
 * of the format 'speed(1234)'.
 * @author	Patrick Gavigan
 * @date	17 Feb 2020
 */

!fly.

+!fly
	:	angularVelocity(_,_,_,_) &
        linearAcceleration(_,_,_,_) &
		orientation(_,_,_,_,_) &
	<-	takeoff();
		!fly.
		
+!fly
	<-	!fly.