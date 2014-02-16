# -*- encoding: utf-8 -*-
from crispy_forms.layout import Field
from crispy_forms.utils import TEMPLATE_PACK


class PrependedIconText(Field):
    template = "fields/prepend_text_with_icon.html"
    icon_class = "fa fa-user"

    def __init__(self, *args, **kwargs):
        if not hasattr(self, 'attrs'):
            self.attrs = {}
        if 'icon_class' in kwargs:
            self.icon_class = kwargs.pop('icon_class')
        super(PrependedIconText, self).__init__(*args, **kwargs)

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):
        if hasattr(self, 'icon_class'):
            context['icon_class'] = self.icon_class
        return super(PrependedIconText, self).render(form, form_style, context, template_pack=template_pack)