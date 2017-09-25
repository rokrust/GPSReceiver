#http://www.navipedia.net/index.php/Coordinates_Computation_from_Almanac_Data

from abc import ABC, abstractmethod

word_length = 30

#Helper functions
def extract_parameter(word, param_position, param_length):
    return (word << (word_length - param_position - param_length)) >> (word_length - param_length)

#Abstract class used for ephemeris and almanac
class GPS_data:
    ##Standard parameters
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

#Filled by subframe 4 and 5
class Almanac(GPS_data):
    ##Standard parameters
    #Time
    t_oa = 0.0

    #Orbital
    i_0 = 53
    delta_i = 0.0

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

class Subframe(ABC):
    word = []

    def __init__(self, GPS_data):
        self.store_subframe_in_GPS_data(GPS_data)

    @classmethod
    @abstractmethod
    def store_subframe_in_GPS_data(self, GPS_data): pass

    @staticmethod
    def identify_subframe(subframe):
        subframe_id =     extract_parameter(word[2], 8, 3)
        if subframe_id == 1:
            subframe = Subframe_1
        
        elif subframe_id == 2:
            subframe = Subframe_2
        
        elif subframe_id == 3:
            subframe = Subframe_3
        
        elif subframe_id == 4 or sub_frame_id == 5:
            subframe_page = extract_parameter(word[2], 22, 6)
            
            if subframe <= 32:
                subframe = Almanac_page
            
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



#
class Subframe_4(Subframe): pass
class Subframe_5(Subframe): pass
