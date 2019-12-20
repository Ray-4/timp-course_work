from django.utils.module_loading import import_string
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.password_validation import (MinimumLengthValidator, UserAttributeSimilarityValidator,
    CommonPasswordValidator, NumericPasswordValidator)
from django.core.exceptions import (
    FieldDoesNotExist, ImproperlyConfigured, ValidationError,
)
from django.utils.translation import gettext as _, ngettext

import re
from difflib import SequenceMatcher




class minimumLengthValidation (MinimumLengthValidator):

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ngettext(
                    "Введённый пароль слишком короткий. Он должен содержать как минимум "
                        "%(min_length)d символ. ",
                    "Введённый пароль слишком короткий. Он должен содержать как минимум "
                        "%(min_length)d символов. ",
                    self.min_length
                ),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return ngettext(
            "Ваш пароль должен содержать как минимум %(min_length)d символ. ",
            "Ваш пароль должен содержать как минимум %(min_length)d символов. ",
            self.min_length
        ) % {'min_length': self.min_length}




class userAttribSimilarityValidation (UserAttributeSimilarityValidator):
    def validate(self, password, user=None):
        if not user:
            return

        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, str):
                continue
            value_parts = re.split(r'\W+', value) + [value]
            for value_part in value_parts:
                if SequenceMatcher(a=password.lower(), b=value_part.lower()).quick_ratio() >= self.max_similarity:
                    try:
                        verbose_name = str(user._meta.get_field(attribute_name).verbose_name)
                    except FieldDoesNotExist:
                        verbose_name = attribute_name
                    raise ValidationError(
                        _("Введённый пароль слишком похож на %(verbose_name)s. "),
                        code='password_too_similar',
                        params={'verbose_name': verbose_name},
                    )

    def get_help_text(self):
        return _("Ваш пароль не должен совпадать с вашим именем или другой персональной "
                    "информацией или быть слишком похожим на неё. ")


class commonPassValidation (CommonPasswordValidator):

    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise ValidationError(
                _("Введённый пароль слишком широко распространён. "),
                code='password_too_common',
            )

    def get_help_text(self):
        return _("Ваш пароль не может быть одним из широко распространённых паролей. ")


class numericPasswordValidation (NumericPasswordValidator):

    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                _("Введённый пароль состоит только из цифр. "),
                code='password_entirely_numeric',
            )

    def get_help_text(self):
        return _("Ваш пароль не может состоять только из цифр. ")















