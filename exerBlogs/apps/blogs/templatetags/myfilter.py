from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def filterBlog(caption, multi, key, tagValue, setValue):
    """
    <a href="/index-1-0-{{ kwargs.article_type_id }}" class="conItem {% if kwargs.category_id == 0 %}conSelect{% endif %}">全部</a>
    :param multi:
    :param key:
    :param value:
    :return:
    """
    rtn = "<a href='/index-1-"
    if key == "category_id":
        rtn += str(tagValue) + "-"
    else:
       rtn += str(multi["category_id"]) + "-"
    if key == "article_type_id":
        rtn += str(tagValue)
    else:
        rtn += str(multi["article_type_id"])

    if tagValue == setValue:
        rtn += "' class='conItem conSelect'>" + caption + "</a>"
    else:
        rtn += "' class='conItem'>" + caption + "</a>"

    return mark_safe(rtn)
