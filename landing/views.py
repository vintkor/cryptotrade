from django.shortcuts import render
from django.views.generic import View
from django.urls import reverse_lazy
from django.shortcuts import redirect
from user_profile.models import User, TopUsers
from random import choice


class LandingView(View):

    def get(self, request):
        ref_code = self.request.COOKIES.get('ref')
        context = {}

        if ref_code:
            try:
                User.objects.get(ref_code=ref_code)
                context['register_url'] = reverse_lazy('user:register-by-ref', kwargs={'ref_code': ref_code})
            except User.DoesNotExist:
                pass
        else:
            top_user_id = choice([i['id'] for i in TopUsers.objects.values('id').all()])
            user_ref_code = User.objects.values('ref_code').get(id=top_user_id)
            context['register_url'] = reverse_lazy('user:register-by-ref', kwargs={'ref_code': user_ref_code.get('ref_code')})

        return render(request, 'landings/index.html', context)

class LandingRefView(View):
    
    def get(self, request, ref_code):
        return redirect(reverse_lazy('landing:home'))

    def dispatch(self, request, *args, **kwargs):
        response = super(LandingRefView, self).dispatch(request, *args, **kwargs)
        response.set_cookie('ref', kwargs.get('ref_code'), max_age=60*60*24*365)
        return response
