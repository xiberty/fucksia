# Project imports
from fucksia.maker.models import Estudiante


def get_user_avatar(backend, details, response, social_user, uid, user, *args, **kwargs):
    url = None

    if backend.name == 'facebook':
        url = "http://graph.facebook.com/%s/picture?type=large" % response['id']

    elif backend.name == 'twitter':
        url = response.get('profile_image_url', '').replace('_normal', '')

    if url:
        est, created = Estudiante.objects.get_or_create(uid=user.id)
        if created:
            est.nombre=details['fullname']
            est.avatar=url
            est.social_network=backend.name
            est.email=details['email']
            est.save()

