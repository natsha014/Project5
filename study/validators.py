import re

from rest_framework.exceptions import ValidationError


class VideoLinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        video_url = dict(value).get(self.field)
        if not video_url:
            return

        youtube_reg = re.compile(r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/')
        if not youtube_reg.match(video_url):
            raise ValidationError('Разрешены только ссылки на YouTube.')
