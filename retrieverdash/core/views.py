from django.http import HttpResponse
from django.views import View


class DashboardView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("This is the dashboard view.")
