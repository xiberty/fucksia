import os
import html2text
from premailer import Premailer
from django.conf import settings
from django.template import Context, loader
from django.core.mail.message import EmailMultiAlternatives



def send_mail(subject, body_text, addr_from, addr_to, fail_silently=False,
              attachments=None, body_html=None, connection=None):
    """
    Sends a multipart email containing text and html versions which
    are encrypted for each recipient that has a valid gpg key
    installed.
    """

    # Allow for a single address to be passed in.
    if not hasattr(addr_to, "__iter__"):
        addr_to = [addr_to]

    # Obtain a list of the recipients that have gpg keys installed.
    key_addresses = {}

    # Load attachments and create name/data tuples.
    attachments_parts = []
    if attachments is not None:
        for attachment in attachments:
            # Attachments can be pairs of name/data, or filesystem paths.
            if not hasattr(attachment, "__iter__"):
                with open(attachment, "rb") as f:
                    attachments_parts.append(
                        (os.path.basename(attachment), f.read()))
            else:
                attachments_parts.append(attachment)

    # Send emails.
    for addr in addr_to:
        msg = EmailMultiAlternatives(subject, body_text, addr,
                                     addr_from, [addr], connection=connection)
        if body_html is not None:
            msg.attach_alternative(body_html, "text/html")
        for parts in attachments_parts:
            name = parts[0]
            if key_addresses.get(addr):
                name += ".asc"
            msg.attach(name, parts[1])
        msg.send(fail_silently=fail_silently)


def send_mail_template(subject, addr_to, addr_from, template_name,
                       fail_silently=False, attachments=None, context=None,
                       connection=None):
    """
    Send email rendering text and html template for the specified
    template name using the context dictionary passed in.
    """
    context = context if context else {}

    content_html = loader.get_template(template_name).render(Context(context))

    bname, ext = os.path.splitext(template_name)
    template_name_text = '.'.join([bname, ext])

    if os.path.exists(template_name_text):
        content_text = loader.get_template(template_name).render(
            Context(context))
    else:
        h = html2text.HTML2Text(baseurl=settings.BASE_URL)
        content_text = h.handle(content_html)

    content_html = Premailer(
        content_html,
        base_url=settings.BASE_URL,
        preserve_internal_links=False,
        exclude_pseudoclasses=False,
        keep_style_tags=True,
        include_star_selectors=True,
        remove_classes=False,
        strip_important=False,
        external_styles=None
    ).transform()

    send_mail(subject, content_text, addr_from, addr_to,
              fail_silently=fail_silently, attachments=attachments,
              body_html=content_html, connection=connection)

