from django import template


register = template.Library()


@register.filter()
def censor(value):
    bad_word = ['Искусство', 'Мэр', 'геймеров', 'очко']
    for word in value.split():
        for i in bad_word:
            if i.lower() in word.lower().replace(',.:;/-\\""', ''):
                value = value.replace(i, f"{i[0]}{'*' * (len(i) - 1)}")

    if not isinstance(value, str):
        raise TypeError(f'Filter applied to an unresolved type {type(value)}\nAllowed type str')

    return value