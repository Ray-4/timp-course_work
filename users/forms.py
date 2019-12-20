from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.forms import AuthenticationForm, UsernameField, PasswordResetForm, SetPasswordForm
from django.utils.translation import gettext, gettext_lazy as _
from django.core import validators
from photo_forum.settings import AUTH_PASSWORD_VALIDATORS



from django.contrib.auth import authenticate
from django.utils.translation import gettext as _, ngettext




class RegistrForm(UserCreationForm):

    email = forms.EmailField(label="Электронная почта")

    username_validator = UnicodeUsernameValidator()
    username_validator.message =  _(
        'Введите правильное имя пользователя. Это значение может содержать только английские буквы '
        'цифры и символы @ /. / + / - / '
    )

    username = forms.CharField(
        label = ('Логин'),
        max_length = 50,
        help_text = ('Только буквы, цифры и @ /. / + / - / _.'),
        validators = [username_validator],
    )

    password1 = forms.CharField(
        label = ("Пароль"),
        strip = False,
        widget = forms.PasswordInput,
        help_text = ("Ваш пароль не может быть слишком похож на другую вашу личную информацию. "
                   " Ваш пароль должен содержать не менее 8 символов."
                  " Ваш пароль не может быть часто используемым паролем."
                 " Ваш пароль не может быть полностью цифровым."),

    )
    password2 = forms.CharField(
        label = ("Подтверждение пароля"),
        widget = forms.PasswordInput,
        strip = False,
        help_text = ("Введите тот же пароль, что и раньше, для проверки."),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # проверяет есть ли этот email уже в базе данных
    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        # __iexaxt - фильтр для регистро-независимого точного совпадения
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Данный email уже используется')
        return email

    # проверяет если данный user в базе данных
    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        # __exaxt - фильтр для регистро-зависимого точного совпадения
        # exists() - возвращает True если QuerySet содержит какой-либо результат,
        # и False, если не содержит.
        if User.objects.filter(username__exact=username).exists():
            raise forms.ValidationError('Пользователь с таким именем уже существует.')
        return username

    # проверка совпадения паролей
    def clean_password2(self):

        cd_1 = self.cleaned_data['password1']
        cd_2 = self.cleaned_data['password2']

        if cd_1 != cd_2:
            raise forms.ValidationError('Вы ввели разные пароли')
        return cd_2


class EditUserForm(forms.ModelForm):

    email = forms.EmailField(label="Электронная почта")

    username_validator = UnicodeUsernameValidator()

    username = forms.CharField(
        label = 'Логин',
        max_length = 50,
        help_text = ('Только буквы, цифры и @ /. / + / - / _.'),
        validators = [username_validator],
        error_messages = {
            'unique': ("Пользователь с таким именем уже существует."),
        }
    )

    """
    # проверяет есть ли этот email уже в базе данных
    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        # __iexaxt - фильтр для регистро-независимого точного совпадения
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Данный email уже используется')
        return email
    """

    class Meta:
        model = User
        fields = ['username', 'email']




class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['website', 'image']





class AuthorizationForm (AuthenticationForm):
    username = UsernameField(label="Логин", widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label=_("Пароль"),
        strip=False,
        widget=forms.PasswordInput,
    )

    error_messages = {
        'invalid_login': _(
            "Пожалуйста, введите правильный логин и пароль. Учтите что оба поля "
            "могут быть чувствительны к регистру."
        ),
        'inactive': _("Этот аккаунт неактивирован"),
        'required':_("Это поле обязательно к заполнению."),
    }

    default_error_messages = {
        'required': _('Это поле обязательно к заполнению!!.'),
    }

    empty_values = list(validators.EMPTY_VALUES) # список пустых значений передает

    def validate(self, value):
        if value is None:
            raise forms.ValidationError("Это поле обязательно к заполнению!")




class PassResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Электронная почта"), max_length=254)


class ResetPassForm (SetPasswordForm):
    """
        Форма, позволяющая пользователю изменять свой пароль,
        не вводя свой старый пароль
    """

    error_messages = {
        'password_mismatch': _("Пароли не совпадают."),
    }
    new_password1 = forms.CharField(
        label=_("Новый пароль"),
        widget = forms.PasswordInput,
        strip = False,
        help_text = ("Ваш пароль не может быть слишком похож на другую вашу личную информацию. "
                   " Ваш пароль должен содержать не менее 8 символов."
                  " Ваш пароль не может быть часто используемым паролем."
                 " Ваш пароль не может быть полностью цифровым."),
    )
    new_password2 = forms.CharField(
        label = _("Подтверждение нового пароля"),
        strip = False,
        widget = forms.PasswordInput,
    )


































