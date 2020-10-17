from django.conf import settings
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView

import os
import json

file_path = os.path.join(settings.PROJECT_ROOT,
                         'dashboard_script/dataset_details.json')
diff_path = os.path.join(settings.PROJECT_ROOT,
                         'dashboard_script/diffs/')


class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        try:
            json_detail = json.load(open(file_path, 'r'))
        except IOError:
            json_detail = dict({'dataset_details': None, 'last_checked_on': None})
        context.update({
            'datasets': json_detail['dataset_details'],
            'last_checked_on': json_detail['last_checked_on']
        })
        return context


class DiffView(View):
    def get(self, request, filename):
        return HttpResponse(open(os.path.join(diff_path, filename)))
