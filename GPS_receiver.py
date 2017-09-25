from abc import ABC, abstractmethod

word_length = 30

#Helper functions
def extract_parameter(word, param_position, param_length):
    return (word << (word_length - param_position - param_length)) >> (word_length - param_length)

class Almanac
    t_sv = 0.0
    t_ow = 0.0
    t_gd = 0.0
    t_oc = 0.0
    t_oe = 0.0
    w_n = 0;

    # Orbital
    M_0 = 0.0
    i_0 = 0.0
    omega_0 = 0.0
    omega = 0.0
    e = 0.0
    sqrt_a = 0.0
    omega_dot = 0.0
    i_dot = 0.0

    ##Corrections
    # Clock correction parameters
    a_f0 = 0.0
    a_f1 = 0.0
    a_f2 = 0.0

    # Orbital correction parameters
    C_us = 0.0
    C_uc = 0.0
    C_rc = 0.0
    C_rs = 0.0
    C_is = 0.0
    C_ic = 0.0
    delta_n = 0.0;

    ##Validity
    aodc = 0
    AODE = 0
    IODE = 0


class Ephemeris(Almanac):
    ##Standard parameters
    #Time
    t_sv = 0.0
    t_ow = 0.0
    t_gd = 0.0
    t_oc = 0.0
    t_oe = 0.0
    w_n = 0;

    #Orbital
    M_0 = 0.0
    i_0 = 0.0
    omega_0 = 0.0
    omega = 0.0
    e = 0.0
    sqrt_a = 0.0
    omega_dot = 0.0
    i_dot = 0.0

    ##Corrections
    #Clock correction parameters
    a_f0 = 0.0
    a_f1 = 0.0
    a_f2 = 0.0

    #Orbital correction parameters
    C_us = 0.0
    C_uc = 0.0
    C_rc = 0.0
    C_rs = 0.0
    C_is = 0.0
    C_ic = 0.0
    delta_n = 0.0;

    ##Validity
    aodc = 0
    AODE = 0
    IODE = 0

    ##function definitions

class Subframe(ABC):
    word = []

    @abstractmethod
    def store_subframe_in_ephemeris(self, ephemeris): pass


class Subframe_1(Subframe):
    def store_subframe_in_ephemeris(self, ephemeris):
        #### MISSING IODC #####
        ephemeris.w_n =     extract_parameter(self.word[2], 20, 10)
        ephemeris.t_gd =    extract_parameter(self.word[6], 6, 8)
        ephemeris.t_oc =    extract_parameter(self.word[7], 6, 16)
        ephemeris.a_f2 =    extract_parameter(self.word[8], 22, 8)
        ephemeris.a_f1 =    extract_parameter(self.word[8], 6, 16)
        ephemeris.a_f0 =    extract_parameter(self.word[9], 8, 22)


class Subframe_2(Subframe):
    def store_subframe_in_ephemeris(self, ephemeris):
        ephemeris.IODE =    extract_parameter(self.word[2], 22, 8)
        ephemeris.C_rs =    extract_parameter(self.word[2], 6, 16)
        ephemeris.delta_n = extract_parameter(self.word[3], 14, 16)
        ephemeris.C_uc =    extract_parameter(self.word[5], 14, 16)
        ephemeris.C_us =    extract_parameter(self.word[7], 14, 16)
        ephemeris.t_oe =    extract_parameter(self.word[9], 14, 16)

        #parameters longer than word length
        M_0_LSBs =          extract_parameter(self.word[4], 6, 24)
        M_0_MSBs =          extract_parameter(self.word[3], 6, 8)
        e_LSBs =            extract_parameter(self.word[6], 6, 24)
        e_MSBs =            extract_parameter(self.word[5], 6, 8)
        sqrt_A_LSBs =       extract_parameter(self.word[8], 6, 24)
        sqrt_A_MSBs =       extract_parameter(self.word[8], 6, 8)

        #gather bytes
        ephemeris.M_0 =     (M_0_MSBs << 8) | M_0_LSBs
        ephemeris.e =       (e_MSBs << 8) | e_LSBs
        ephemeris.sqrt_a =  (sqrt_A_MSBs << 8) | sqrt_A_LSBs

class Subframe_3(Subframe):
    def store_subframe_in_ephemeris(self, ephemeris):
        ephemeris.C_ic =    extract_parameter(self.word[2], 14, 16)
        ephemeris.C_is =    extract_parameter(self.word[4], 14, 16)
        ephemeris.C_rc =    extract_parameter(self.word[6], 14, 16)
        ephemeris.omega_dot = extract_parameter(self.word[8], 6, 24)
        ephemeris.i_dot =   extract_parameter(self.word[9], 8, 14)
        ephemeris.IODE =    extract_parameter(self.word[9], 22, 8)

        #parameters longer than word length
        omega_0_LSBs =      extract_parameter(self.word[3], 6, 24)
        omega_0_MSBs =      extract_parameter(self.word[2], 6, 8)
        i_0_LSBs =          extract_parameter(self.word[5], 6, 24)
        i_0_MSBs =          extract_parameter(self.word[4], 6, 8)
        omega_LSBs =        extract_parameter(self.word[7], 6, 24)
        omega_MSBs =        extract_parameter(self.word[6], 6, 8)

        #gather bytes
        ephemeris.omega_0 = (omega_0_MSBs << 8) | omega_0_LSBs
        ephemeris.i_0 =     (i_0_MSBs << 8) | i_0_LSBs
        ephemeris.omega =   (omega_MSBs << 8) | omega_LSBs


class Subframe_4(Subframe):
    def store_subframe_in_ephemeris(self, ephemeris):


class Subframe_5(Subframe):
    def store_subframe_in_ephemeris(self, ephemeris):
        ephemeris.e =       extract_parameter(self.word[2])


def store_gps_subframe_data(subframe):




