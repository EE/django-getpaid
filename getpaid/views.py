# getpaid views
import logging
from django.conf import settings
from django.core.exceptions import PermissionDenied, ImproperlyConfigured
from django.urls import reverse
from django import http
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView
from getpaid.forms import PaymentMethodForm, ValidationError


logger = logging.getLogger(__name__)


class NewPaymentView(FormView):
    form_class = PaymentMethodForm
    template_name = "getpaid/payment_post_form.html"

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        self.currency = self.kwargs['currency']
        return form_class(self.currency, **self.get_form_kwargs())

    def get(self, request, *args, **kwargs):
        """
        This view operates only on POST requests from order view where
        you select payment method
        """
        return http.HttpResponseNotAllowed(['POST'])

    def form_valid(self, form):
        from getpaid.models import Payment
        order = form.cleaned_data['order']
        next_url, method, form, processor = Payment.run_payment(
            order,
            form.cleaned_data['backend'],
            request=self.request
        )
        if next_url is None and getattr(order, 'recurring', False):
            next_url = getattr(settings, 'GETPAID_SUCCESS_URL_NAME', None)
            return http.HttpResponseRedirect(reverse(next_url))

        if method.upper() == 'GET':
            return http.HttpResponseRedirect(next_url)
        elif method.upper() == 'POST':
            context = self.get_context_data()
            context['gateway_url'] = processor.get_gateway_url(self.request)[0]
            context['form'] = processor.get_form(form)

            return TemplateResponse(
                request=self.request,
                template=self.get_template_names(),
                context=context)
        else:
            raise ImproperlyConfigured()

    def form_invalid(self, form):
        raise PermissionDenied


class FallbackView(RedirectView):
    success = None
    permanent = False

    def get_redirect_url(self, **kwargs):
        from getpaid.models import Payment
        self.payment = get_object_or_404(Payment, pk=self.kwargs['pk'])

        if self.success:
            url_name = getattr(settings, 'GETPAID_SUCCESS_URL_NAME', None)
        else:
            url_name = getattr(settings, 'GETPAID_FAILURE_URL_NAME', None)

        if url_name is not None:
            return reverse(url_name, kwargs={'pk': self.payment.order_id})
        return self.payment.order.get_absolute_url()
