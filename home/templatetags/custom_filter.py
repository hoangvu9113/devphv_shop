from django import template
from ..models import *

register=template.Library()
@register.filter
def count_product_cart(user):
    try:
        order = Order.objects.get(user=user, status=0)
        order_detail = order.orderdetail_set.all()
        return sum([item.order_quantity for item in order_detail])
    except BaseException as e:
        return 0
        
@register.filter
def get_childs(parent_id):
    return Category.objects.filter(category_parent_id=parent_id)
