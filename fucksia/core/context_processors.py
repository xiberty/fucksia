from django.conf import settings

def website(request):
    """
    Returns common info about the website
    """
    return {
        'website_name': settings.WEBSITE_NAME,
        'website_description': settings.WEBSITE_DESCRIPTION,
        'website_author': settings.WEBSITE_AUTHOR
    }


def debug(context):
    return {'DEBUG': settings.DEBUG}