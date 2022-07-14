import datetime

from django import template
import re

register = template.Library()


# custom filter
@register.filter()
def censor(value):
    for repl in ["fuck", "damn", "dick", "cunt", "cock", "twat", "shit", "piss", "arsehole",
                 "asshole", "prick", "pussy", "хуй", "хуе", "хуи", "хуя", "хуё", "пизд", "ебат", "ебан", "ёба", "еби",
                 "бля", "дерьм", "муда", "муди", "мудо"]:
        repl = f"({repl[:1]}){repl[1:-1]}\\w*(\\w)(?=[\\s\\.,!?])"

        value = re.sub(repl, '\\1**\\2', value, flags=re.IGNORECASE)

    return f'{value}'

@register.simple_tag(takes_context = True, name = "tagname")
def func(context, other_arg):
    pass
