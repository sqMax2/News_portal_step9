from django import template
import re

register = template.Library()


# custom filter
@register.filter()
def censor(value):
    for repl in ["fuck", "damn", "dick", "cunt", "cock", "twat", "shit", "piss", "arsehole",
                 "asshole", "prick", "pussy"]:
        repl = "(" + repl[:1] + ")" + repl[1:-1] + "(" + repl[-1:] + ")"
        value = re.sub(repl, '\\1**\\2', value, flags=re.IGNORECASE)

    return f'{value}'
