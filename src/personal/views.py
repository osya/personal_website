from django.views.generic import TemplateView


class ContactView(TemplateView):
    template_name = 'personal/contact.html'

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)
        context["content"] = ['If you would like to contact me, please email me', 'info@vosipov.com']
        return context
