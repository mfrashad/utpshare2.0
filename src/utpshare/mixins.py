from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator




class LoginRequiredMixin(object):
  @method_decorator(login_required)
  def dispatch(self, request, *args, **kwargs):
    return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class StatffRequiredMixin(object):
  @method_decorator(staff_member_required)
  def dispatch(self, request, *args, **kwargs):
    return super(StatffRequiredMixin, self).dispatch(request, *args, **kwargs)