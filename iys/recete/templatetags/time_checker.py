from django import template

register = template.Library()


@register.filter(name='timeChecker')
def timeChecker(value):
    if (value is None or value == ''):
        return ''
    strTime = str(value)
    strTimeArr = strTime.split(':')

    return strTimeArr[0] + ':' + strTimeArr[1]
