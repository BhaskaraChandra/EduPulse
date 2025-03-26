from django import template

register = template.Library()

@register.inclusion_tag('selection_popup.html')
def selection_popup(title, items, selected_items, item_name='name'):
    return {
        'title': title,
        'items': items,
        'selected_items': selected_items,
        'item_name': item_name,
    }
