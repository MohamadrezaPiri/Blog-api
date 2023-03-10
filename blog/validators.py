from django.core.exceptions import ValidationError


def validate_image_size(file):
    max_size_kb = 20
    if file.size > max_size_kb * 1024:
        raise ValidationError(
            f'Image size cannot be greater than {max_size_kb}KB')
