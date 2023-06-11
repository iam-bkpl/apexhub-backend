from django.core.exceptions import ValidationError


def file_size_validation(file):
  max_size_kb = 500
  
  if file.size > max_size_kb * 1024:
    raise ValidationError(f"file size cannot be larger than {max_size_kb} KB")