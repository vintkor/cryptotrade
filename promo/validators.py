from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


def youtube_validator(value):

    youtube_re = '^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+'
    is_youtube = re.match(youtube_re, value)

    if not is_youtube:
        raise ValidationError(
            _('{} - is not valid youtube link'.format(value))
        )