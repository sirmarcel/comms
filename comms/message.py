"""format output"""

from .terminal import get_size


from click import style

chars_prefix = 15
chars_indicator = 1
chars_suffix = 12
chars_gutter = 1
chars_context = chars_prefix + chars_suffix + chars_indicator + 3 * chars_gutter
chars_total = 80  # default width of output

prefix_bracket = ("[", "]")
suffix_bracket = ("(", ")")

prefix = "comms"
suffix = None

truncation = "…"
gutter = chars_gutter * " "


def message(
    message,
    prefix=prefix,
    suffix=suffix,
    indent=0,
    prefix_bracket=prefix_bracket,
    suffix_bracket=suffix_bracket,
    truncate_message=True,
    indicator=" ",
    style_message=None,
    style_all=None,
):

    prefix = f"{prefix_bracket[0]}{prefix}{prefix_bracket[1]}"
    prefix = f"{prefix:<{chars_prefix}}"

    if isinstance(indent, int):
        indent = " " * indent

    message = indent + message
    if truncate_message:
        if get_size() < 80:
            chars_message = get_size() - chars_context
        else:
            chars_message = chars_total - chars_context

        if len(message) > chars_message:
            message = message[:chars_message-1] + truncation
        message = f"{message:<{chars_message}}"

    if style_message is not None:
        message = style(message, **style_message)

    indicator = f"{indicator}"

    if suffix is not None:
        if len(suffix) > chars_suffix:
            suffix = suffix[:chars_suffix-3] + truncation
        suffix = f"{suffix_bracket[0]}{suffix}{suffix_bracket[1]}"
        suffix = f"{suffix:<{chars_suffix}}"
    else:
        suffix = chars_suffix * " "

    msg = gutter.join([prefix, message, indicator, suffix])

    if style_all is not None:
        msg = style(msg, **style_all)

    return msg
