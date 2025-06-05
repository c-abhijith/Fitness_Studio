from django.core.paginator import EmptyPage, PageNotAnInteger


def pagination(page, paginator):
    try:
        result = paginator.page(page)
        return result
    except PageNotAnInteger:
        result = paginator.page(1)
        return result
    except EmptyPage:
        result = paginator.page(paginator.num_pages)
        return result
