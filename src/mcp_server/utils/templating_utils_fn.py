from docxtpl import RichText


def make_link(doc, text: str | None, url: str | None, underline=False, bold=False):
    """
    Create a RichText hyperlink safely with optional underline and bold.

    Args:
        doc: DocxTemplate document object (used for building url_id).
        text (str | None): The display text for the hyperlink.
        url (str | None): The URL for the hyperlink.
        underline (bool): Whether the link text should be underlined.
        bold (bool): Whether the link text should be bold.

    Returns:
        RichText: RichText object with hyperlink, or empty string if text/url missing.
    """
    if not text or not url:
        return ""
    rt = RichText()
    rt.add(text, url_id=doc.build_url_id(url), underline=underline, bold=bold)
    return rt


def safe_get(obj, *attrs):
    """
    Safely navigate nested dicts or objects.

    Args:
        obj: The root object or dict.
        *attrs: Sequence of attribute or key names to traverse.

    Returns:
        The nested value, or None if any attribute/key is missing.
    """
    for attr in attrs:
        if obj is None:
            return None
        if isinstance(obj, dict):
            obj = obj.get(attr)
        else:
            obj = getattr(obj, attr, None)
    return obj
