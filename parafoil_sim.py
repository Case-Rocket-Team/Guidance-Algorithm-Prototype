import numpy as np
import math
import parafoil_utils as utils

class State:
    def __init__(self,max_wind=0):
        self.pos = np.array((0,0,0),dtype='float64')
        self.vel = np.array((0,0,0),dtype='float64')
        self.dThetaDs = 1 + 0j
        self.heading = 1 + 0j
        self.turningRadius = 0
        
        self.dt = 0.5
        self.glideRatio = 6.5 * 2
        self._zVelLast = 0
        self.max_wind = max_wind

    def update(self):
        dz = self._zVelLast * self.dt
        dx = dz * self.glideRatio

        # Update velocity and position, apply wind
        #vert, horiz = 
        self.vel[0] = np.real(self.heading) * dx
        self.vel[1] = np.imag(self.heading) * dx
        self.vel[2] = -utils.rateOfDescent(self.pos[2])[0]
        self.pos += self.getGroundVel() * self.dt
        self._zVelLast = self.vel[2]

        speed = math.sqrt(self.vel[0] ** 2 + self.vel[1] ** 2)
        #speed = math.sqrt(self.getGroundVel()[0] ** 2 + self.getGroundVel()[1] ** 2)

        # Apply rotations
        if self.turningRadius == 0:
            self._setDThetaDtRad(0)
        else:
            self._setDThetaDtRad(speed / self.turningRadius)
        self.heading = self.heading * self._dThetaDs
        #self.heading /= abs(self.heading)
        #print(self.getHeadingRad(), self._getDThetaDtRad())
        
        
    
    def setHeadingRad(self, heading):
        self.heading = -np.exp(1j * heading)

    def getHeadingRad(self):
        return np.angle(self.heading)

    def _setDThetaDtRad(self, dThetaDt):
        self._dThetaDs = np.exp(1j * (self.dt * dThetaDt))

    def _getDThetaDtRad(self):
        return np.angle(self._dThetaDs) / self.dt
    
    
    def getGroundVel(self):
        return self.vel + utils.wind(self.pos,max_velocity=self.max_wind,seed=1) #TODO: seed should be a parameter