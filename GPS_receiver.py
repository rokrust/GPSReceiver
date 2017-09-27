#http://www.navipedia.net/index.php/Coordinates_Computation_from_Almanac_Data

from abc import ABCMeta, abstractmethod
import math

word_length = 30

#Helper functions
def extract_parameter(word, param_position, param_length):
    return (word << (word_length - param_position - param_length)) >> (word_length - param_length)

##Data structures
#Abstract class used for ephemeris and almanac
class GPS_data:
    ##Standard parameters
    # Constants
    F = -4.442807633 * 10**-10
    c = 2.99792458 * 10**8
    mu = 3.986005 * 10**14
    w_ie = 7.2921151467 * 10**-5
    a = 6378137.0
    b = 6356752.3
    f_1 = 1575.42
    f_2 = 1227.60
    omega_e_dot = 0
    lambda_1 = c/f_1
    lambda_2 = c/f_2
    lambda_w = c/(f_1 - f_2)
    lambda_n = c/(f_1 + f_2)

    # Time
    w_n = 0

    # Orbital
    M_0 = 0.0
    i_0 = 0.0
    omega_0 = 0.0
    omega = 0.0
    e = 0.0
    sqrt_a = 0.0
    omega_dot = 0.0

    ##Corrections
    # Clock correction parameters
    a_f0 = 0.0
    a_f1 = 0.0

    ##Functions
    @abstractmethod
    def calculate_satellite_positon(self): pass


#Filled by subframe 4 and 5
class Almanac(GPS_data):
    ##Standard parameters
    #Time
    t_oa = 0.0

    #Orbital
    i_0 = 53
    delta_i = 0.0

    ##Functions
    def calculate_satellite_positon(self):
        #delta_tr = self.F*self.e*self.sqrt_a*sin(self.E_k)

        #Satellite clock correction
        delta_t_sv = self.a_f0 + self.a_f1*(self.t_sv - self.t_oc) + self.a_f2*(self.t_sv - self.t_oc)**2
        t = self.t_sv - delta_t_sv

        A = self.sqrt_a**2                      #orbit semi-major axis
        n_0 = sqrt(self.mu)/(A*self.sqrt_a)     #mean motion

        t_k = t - self.t_oe                     #time from reference epoch
        n = n_0 + self.delta_n                  #Corrected mean motion

        M_k = self.M_0 + t_k*n                  #Mean anomaly

        #recursive computation
        for i in range(22): #Magic number required for millimeter precision
            E_k = M_k + self.e*sin(E_k)

        #True anomaly
        cos_E_k = cos(E_k)
        v_k = atan2(sqrt(1-self.e**2)*sin(E_k)/(1-self.e*cos_E_k), (cos_E_k - self.e)/(1 - self.e*cos_E_k))

        phi_k = v_k + self.omega                #argument of latitude

        sin_2_phi_k = sin(2 * phi_k)
        cos_2_phi_k = cos(2 * phi_k)
        delta_u_k = self.C_us * sin_2_phi_k + self.C_uc * cos_2_phi_k
        delta_r_k = self.C_rs * sin_2_phi_k + self.C_rc * cos_2_phi_k
        delta_i_k = self.C_is * sin_2_phi_k + self.C_ic * cos_2_phi_k

        u_k = phi_k + delta_u_k
        r_k = A*(1 - self.e*cos_E_k) + delta_r_k
        i_k = self.i_0 + delta_i_k + self.i_dot * t_k

        #Coordinates in orbital plane
        X_k = r_k * cos(u_k)
        Y_k = r_k * sin(u_k)
        Omega_k = self.omega_0 + (self.omega_dot - self.omega_e_dot)*t_k - self.omega_e_dot*self.t_oe

        #Coordinates in ECEF
        cos_omega_k = cos(Omega_k)
        sin_omega_k = sin(Omega_k)
        cos_i_k = cos(i_k)
        x_k = X_k*cos_omega_k - Y_k*cos_i_k*sin_omega_k
        y_k = X_k*sin_omega_k + Y_k*cos_i_k*cos_omega_k
        z_k = Y_k*sin(i_k)




#Filled by subframe 1, 2 and 3
class Ephemeris(GPS_data):
    ##Standard parameters
    # Time
    t_sv = 0.0
    t_ow = 0.0
    t_gd = 0.0
    t_oc = 0.0
    t_oe = 0.0

    # Orbital
    i_dot = 0.0

    ##Corrections
    # Clock correction parameters
    a_f2 = 0.0

    # Orbital correction parameters
    C_us = 0.0
    C_uc = 0.0
    C_rc = 0.0
    C_rs = 0.0
    C_is = 0.0
    C_ic = 0.0
    delta_n = 0.0

    ##Validity
    aodc = 0
    AODE = 0
    IODC = 0
    IODE = 0

    ##function definitions

##Frame structures
#Abstract super class
class Subframe:
    word = []
    id = 0
    __metaclass__ = ABCMeta

    def __init__(self, GPS_data):
        self.store_subframe_in_GPS_data(GPS_data)

    @classmethod
    @abstractmethod
    def store_subframe_in_GPS_data(self, GPS_data): pass

    @staticmethod
    def identify_subframe(subframe, GPS_data):
        if subframe.id == 1:
            subframe = Subframe_1(GPS_data)
        
        elif subframe.id == 2:
            subframe = Subframe_2(GPS_data)
        
        elif subframe.id == 3:
            subframe = Subframe_3(GPS_data)
        
        elif subframe.id == 4 or subframe.id == 5:
            subframe_page = extract_parameter(subframe.word[2], 22, 6)
            
            if subframe <= 32:
                subframe = Almanac_page(GPS_data)
            
            else:
                print "Ugh too complicated"

#Fills ephemeris
class Subframe_1(Subframe):
    def __init__(self, GPS_data):
        super(Subframe_1, self).__init__(self, GPS_data)

    def store_subframe_in_GPS_data(self, GPS_data):
        #### MISSING IODC #####
        GPS_data.w_n =      extract_parameter(self.word[2], 20, 10)
        GPS_data.t_gd =     extract_parameter(self.word[6], 6, 8)
        GPS_data.t_oc =     extract_parameter(self.word[7], 6, 16)
        GPS_data.a_f2 =     extract_parameter(self.word[8], 22, 8)
        GPS_data.a_f1 =     extract_parameter(self.word[8], 6, 16)
        GPS_data.a_f0 =     extract_parameter(self.word[9], 8, 22)

#Fills ephemeris
class Subframe_2(Subframe):
    def __init__(self, GPS_data):
        super(Subframe_2, self).__init__(self, GPS_data)

    def store_subframe_in_GPS_data(self, GPS_data):
        GPS_data.IODE =     extract_parameter(self.word[2], 22, 8)
        GPS_data.C_rs =     extract_parameter(self.word[2], 6, 16)
        GPS_data.delta_n =  extract_parameter(self.word[3], 14, 16)
        GPS_data.C_uc =     extract_parameter(self.word[5], 14, 16)
        GPS_data.C_us =     extract_parameter(self.word[7], 14, 16)
        GPS_data.t_oe =     extract_parameter(self.word[9], 14, 16)

        #parameters longer than word length
        M_0_LSBs =          extract_parameter(self.word[4], 6, 24)
        M_0_MSBs =          extract_parameter(self.word[3], 6, 8)
        e_LSBs =            extract_parameter(self.word[6], 6, 24)
        e_MSBs =            extract_parameter(self.word[5], 6, 8)
        sqrt_A_LSBs =       extract_parameter(self.word[8], 6, 24)
        sqrt_A_MSBs =       extract_parameter(self.word[8], 6, 8)

        #gather bytes
        GPS_data.M_0 =      (M_0_MSBs << 24) | M_0_LSBs
        GPS_data.e =        (e_MSBs << 24) | e_LSBs
        GPS_data.sqrt_a =   (sqrt_A_MSBs << 24) | sqrt_A_LSBs

#Fills ephemeris
class Subframe_3(Subframe):
    def __init__(self, GPS_data):
        super(Subframe_3, self).__init__(self, GPS_data)

    def store_subframe_in_GPS_data(self, GPS_data):
        GPS_data.C_ic =     extract_parameter(self.word[2], 14, 16)
        GPS_data.C_is =     extract_parameter(self.word[4], 14, 16)
        GPS_data.C_rc =     extract_parameter(self.word[6], 14, 16)
        GPS_data.omega_dot = extract_parameter(self.word[8], 6, 24)
        GPS_data.i_dot =    extract_parameter(self.word[9], 8, 14)
        GPS_data.IODE =     extract_parameter(self.word[9], 22, 8)

        #parameters longer than word length
        omega_0_LSBs =      extract_parameter(self.word[3], 6, 24)
        omega_0_MSBs =      extract_parameter(self.word[2], 6, 8)
        i_0_LSBs =          extract_parameter(self.word[5], 6, 24)
        i_0_MSBs =          extract_parameter(self.word[4], 6, 8)
        omega_LSBs =        extract_parameter(self.word[7], 6, 24)
        omega_MSBs =        extract_parameter(self.word[6], 6, 8)

        #gather bytes
        GPS_data.omega_0 =  (omega_0_MSBs << 24) | omega_0_LSBs
        GPS_data.i_0 =      (i_0_MSBs << 24) | i_0_LSBs
        GPS_data.omega =    (omega_MSBs << 24) | omega_LSBs

#Fills the almanac
class Almanac_page(Subframe):
    def __init__(self, GPS_data):
        super(Almanac_page, self).__init__(self, GPS_data)

    def store_subframe_in_GPS_data(self, GPS_data):
        GPS_data.e = extract_parameter(self.word[2], 6, 16)
        GPS_data.t_oa = extract_parameter(self.word[3], 22, 8)
        GPS_data.delta_i = extract_parameter(self.word[3], 6, 16)
        GPS_data.omega_dot = extract_parameter(self.word[4], 14, 16)
        GPS_data.sqrt_a = extract_parameter(self.word[5], 6, 24)
        GPS_data.omega_0 = extract_parameter(self.word[6], 6, 24)
        GPS_data.omega = extract_parameter(self.word[7], 6, 24)
        GPS_data.M_0 = extract_parameter(self.word[8], 6, 24)
        GPS_data.a_f1 = extract_parameter(self.word[9], 11, 11)

        # split parameter
        a_f0_LSBs = extract_parameter(self.word[9], 8, 3)
        a_f0_MSBs = extract_parameter(self.word[9], 22, 8)

        # gather bytes
        GPS_data.a_f0 = (a_f0_MSBs << 3) | a_f0_LSBs

#Not yet used
class Subframe_4(Subframe): pass
class Subframe_5(Subframe): pass

