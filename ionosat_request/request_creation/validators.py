
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator


request_max_number_validator = MaxValueValidator(9999, message='Request number must be less than 9999')
request_max_latitude_start_validator = MaxValueValidator(82.0, message='Request latitude start must be less then 82.0')
request_min_latitude_start_validator = MinValueValidator(-82.0,
                                                         message='Request latitude start must be greater than -82.0')
request_max_longitude_validator = MaxValueValidator(359.9, message='Request longitude stop must be less then 359.9')
request_min_longitude_validator = MinValueValidator(000.0,
                                                    message='Request longitude start must be greater then 000.0')
device_amount_max_val_validator = MaxValueValidator(8, message='Request device amount must be in range 1-8')
device_amount_min_val_validator = MinValueValidator(0, message='Request device amount must be in range 1-8')
request_file_validator = RegexValidator(r'KNA(0[1-9]|[12][0-9]|3[01])(0[1-9]|1[012])\d\d\d{4}\.zp',
                                        message='Request file name should be KNAddmmyynnnn.zp')






if __name__=="__main__":
    print(request_max_number_validator(99999))