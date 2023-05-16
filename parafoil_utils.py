import math, noise
import numpy as np

def airDensityFromAltitude(z):  #https://en.wikipedia.org/wiki/Density_of_air REDO under troposphere
        p = 0 #air density [kg/m^3]
        StandAtmPres = 101325 #[Pa] at sea lvel
        StandTemp = 288.12 #[K] at sea level
        gravity = 9.80665 #[mn/s^2]
        tempLapseRate = 0.0065 #[K/m]
        gasConstant =  8.31432 #[N*m / mol*k]
        molarMass = 0.0289644 #molar mass of dry air [kg/mol]
        intermediate = StandAtmPres
        intermediate2 = (1-tempLapseRate*z/StandTemp)**(((gravity*molarMass)/(gasConstant*tempLapseRate))-1)
        return (intermediate *intermediate2)
        
        
def convertAirDensitytoImperial(airDensity): #converts airDensity to imperial units in slugs/ft^3 from kg/m^3
    convert = airDensity  #storing airDensity in new variable called convert so the imperial value is not over written when given a new altitude reading
    convert *= 0.00194032 #converting airDensity from metric to imperial unit by conversion factor 0.00194032
    return (convert) 

def rateOfDescent(height): #Parachutes 101 in CRT drive
        # air density
        airDensity = convertAirDensitytoImperial(airDensityFromAltitude(height))

        WeightofLoad= 8.8 #load + parachute, (lbs) 8.8lbs (all according to Luke)
        SurfaceArea =1.9375 #canopy surface area (ft^2) 
        dragCoefficient = 1.6 #related to SA (unitless) ~1.6
        densityO = 0.237689 #Density at sea level
        glide_ratio = 6.5 #glide ratio of parachute (unitless) ~6.5
        C_R = math.sqrt(dragCoefficient**2+(glide_ratio/dragCoefficient)**2 )#combined ratio (unitless) ~6.7
        inter_v_trajectory = WeightofLoad *2/(SurfaceArea*C_R*densityO)
        v_trajectory = math.sqrt(inter_v_trajectory)
        intermediate = 1/(math.sqrt(airDensity/airDensity))
        aoa = math.atan(1/C_R)
        vel_vert = v_trajectory*math.sin(aoa)/3.281
        vel_horiz = v_trajectory*math.cos(aoa)/3.281
        # returns in metric again
        return vel_vert, vel_horiz
        
        

def perlin_noise(seed: int, x: float, y: float, z: float) -> float:
        return noise.pnoise3(x, y, z, octaves=5, persistence=0.5, lacunarity=2.0, repeatx=1, repeaty=1, repeatz=1, base=seed)

def wind(coordinate, max_velocity,seed=1):
        np.random.seed(seed)
        wind = np.random.rand(3)
        wind[2] = 0.0
        return wind * max_velocity
        
        
        """
        x, y, z = coordinate
        noise_scale = 0.001

        # Generate Perlin noise for each direction
        x_noise = perlin_noise(seed, x * noise_scale, y * noise_scale, z * noise_scale)
        y_noise = perlin_noise(seed + 1, x * noise_scale, y * noise_scale, z * noise_scale)
        z_noise = perlin_noise(seed + 2, x * noise_scale, y * noise_scale, z * noise_scale)

        # Convert noise values to velocities
        velocity_x = 2 * x_noise - 1
        velocity_y = 2 * y_noise - 1
        velocity_z = 2 * z_noise - 1

        return np.array([velocity_x, velocity_y, velocity_z]) * max_velocity
        """