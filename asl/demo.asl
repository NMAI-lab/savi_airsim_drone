/**
 * Demo BDI program for AirSim car
 * This example BDI program.
 * @author	Patrick Gavigan
 * @date	17 Feb 2020
 */

!fly.

+!fly
	:	angularVelocity(_,_,_,_) &
        linearAcceleration(_,_,_,_) &
		orientation(_,_,_,_,_)
	<-	takeoff(true);
		!fly.
		
+!fly
	<-	!fly.