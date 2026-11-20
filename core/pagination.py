from django.core.paginator import Paginator


def paginate(objects, request, per_page=10):
    paginator = Paginator(objects, per_page)
    return paginator.get_page(request.GET.get('page'))
