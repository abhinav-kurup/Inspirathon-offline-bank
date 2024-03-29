from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import filesizeformat
from os.path import splitext
from datetime import date
import re

SpecialSym =['$', '@', '#', '%', '!', '&', '^', '-', '_', '=', '+' ]


class FileValidator(object):
    extension_message = _("Extension '%(extension)s' not allowed. Allowed extensions are: '%(allowed_extensions)s.'")
    max_size_message = _('The current file %(size)s, which is too large. The maximum file size is %(allowed_size)s.')

    def __init__(self, *args, **kwargs):
        self.allowed_extensions = kwargs.pop('allowed_extensions', None)
        self.max_size = kwargs.pop('max_size', None)

    def __call__(self, value):
        
        # Check the extension
        ext = splitext(value.name)[1].lower()
        if self.allowed_extensions and not ext in self.allowed_extensions:
            message = self.extension_message % {
                'extension' : ext,
                'allowed_extensions': ', '.join(self.allowed_extensions)
            }

            raise ValidationError(message)

        # Check the file size
        filesize = len(value)
        if self.max_size and filesize > self.max_size:
            message = self.max_size_message % {
                'size': filesizeformat(filesize),
                'allowed_size': filesizeformat(self.max_size)
            }

            raise ValidationError(message)


def validate_pw(pw):
    res = True
    if len(pw) < 8:
        res = False
        raise ValidationError(_("Password length should be at least 8 characters"), code=404)
    if not any(char.isdigit() for char in pw):
        res = False
        raise ValidationError("Password should contain atleast one number", code=404)
    if not any(char.isupper() for char in pw):
        res = False
        raise ValidationError("Password should contain at least one uppercase character", code=404)
    if not any(char.islower() for char in pw):
        print('Password should have at least one lowercase letter')
        res = False
        raise ValidationError("Password should contain at least one lowercase character", code=404)
    if not any(char in SpecialSym for char in pw):
        res = False
        raise ValidationError("Password should contain at least one special character", code=404)
    if res:
        return res


def validate_service_number(value):
    if ' ' in value:
        raise ValidationError("Spaces are not allowed in the string.")
    return value


def validate_dob(value):
    if value > date.today():
        raise ValidationError("Birth date cannot be in the future.")
    return value


def validate_name(pw):
    res = True
    if any(char.isdigit() for char in pw):
        res = False
        raise ValidationError("Name should not contain numbers", code=404)
    if any(char in SpecialSym for char in pw):
        res = False
        raise ValidationError("Name should not contain special characters", code=404)
    if res:
        return res


def validate_phone_no(s):
    Pattern = re.compile(r"^\d{10}$")
    if Pattern.match(s) == None:
        return False
    return True


def validate_email(s):
    pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.match(pat,s):
        return True
    return False
