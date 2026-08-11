from django.core.exceptions import ValidationError
def validate_file_size(file):
    size_kb = 50
    if file.size  >size_kb*1028 :
        raise ValidationError(f'Fille cannot be larger than {size_kb} KB')