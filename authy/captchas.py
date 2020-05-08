from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible


class CustomCaptchaV2Invisible(ReCaptchaField):
    widget = ReCaptchaV2Invisible