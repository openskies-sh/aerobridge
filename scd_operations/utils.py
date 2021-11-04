from itertools import cycle

class UAVSerialNumberValidator():
    ''' A class to validate the Serial number of a UAV per the ANSI/CTA-2063-A standard '''

    def code_contains_O_or_I(manufacturer_code):
        if 

    def __init__(self, serial_number):
        self.serial_number = serial_number
        self.serial_number_length_code_points = {'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'A':10,'B':11,'C':12,'D':13,'E':14,'F':15}
        self.serial_number_code_points = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','J','K','L','M','N','P','Q','R','S','T','U','V','W','X','Y','Z']


    def is_valid(self):
        
        manufacturer_code = self.serial_number[:4]
        # Check if the string is four characters
        if not len(manufacturer_code):
            return False

        character_length_code = self.serial_number[4:5]
        # Length code can only be 1-9, A-F
        if character_length_code not in self.serial_number_code_points.keys():
            return False
        #Get the rest of the string 
        manufacturers_code = self.serial_number[5:]
        if (len(manufacturers_code) != self.serial_number_length_code_points[character_length_code]):
            return False

        return True

        
class OperatorRegistrationNumberValidator():
    ''' A class to validate a Operator Registration provided number per the EN4709-02 standard'''

    def __init__(self, operator_registration_number):
        self.operator_registration_number = operator_registration_number
        self.registration_number_code_points = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

    def gen_checksum(self, raw_id):
        assert raw_id.isalnum()
        assert len(raw_id) == 15
        d = {v: k for k, v in enumerate(self.registration_number_code_points)}
        numeric_base_id = list(map(d.__getitem__, list(raw_id)))
        # Multiplication factors for each digit depending on its position
        mult_factors = cycle([2, 1])
        def partial_sum(number, mult_factor):
            """Calculate partial sum ofr a single digit."""
            quotient, remainder = divmod(number * mult_factor, 36)
            return quotient + remainder
        final_sum = sum(partial_sum(int(character), mult_factor) for character, mult_factor in zip(numeric_base_id, mult_factors))

        # Calculate control number based on partial sums
        control_number = -final_sum % 36
        return self.registration_number_code_points[control_number]

    def is_valid(self):
        # Get the prefix 
        oprn, secure_characters = self.operator_registration_number.split('-')

        if len(oprn) != 16:
            return False
        if len(secure_characters) != 3:
            return False
        base_id = oprn[3:-1]
        if not base_id.isalnum():
            return False
        country_code = self.operator_registration_number[:3]
        checksum = self.operator_registration_number[-5] # checksum 
        # op_registration_suffix = self.operator_registration_number[3:]
        random_three_alnum_string = self.operator_registration_number[-3:]
        
        
        computed_checksum = self.gen_checksum(base_id + random_three_alnum_string)

        if computed_checksum != checksum:
            return False


        
        return True