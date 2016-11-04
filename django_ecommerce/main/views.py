from django.shortcuts import render_to_response
from main.models import MarketingItem, StatusReport
from payments.models import User
from django.shortcuts import render_to_response, RequestContext
from payments.models import User
import ipdb


def index(request):
    uid = request.session.get('user')
    if uid is None:
        #main landing page
        market_items = MarketingItem.objects.all()
#        ipdb.set_trace()
        return render_to_response(
                'main/index.html',
                {'marketing_items': market_items}
                )
    else:
        #membership page
#        status = StatusReport.objects.all().order_by('-when')[:20]
        status = StatusReport.objects.latest()
        return render_to_response(
                'main/user.html',
                {'user': User.get_by_id(uid), 'reports': status},
                context_instance=RequestContext(request),
                )

def circle_item(request):
    return render_to_response('circle_item.html')

def report(request):
    if request.method=="post":
        status = request.POST.get('status', '')
        # Update the database with the status
        if status:
            uid = request.session.get('user')
            user = User.get_by_id(uid)
            StatusReport(user=user, status=status).save()
        return index(request)
