from docxtpl import RichText


def make_link(doc, text: str | None, url: str | None, underline=False, bold=False):
    """Create a RichText hyperlink safely with optional underline and bold."""
    if not text or not url:
        return ""
    rt = RichText()
    rt.add(text, url_id=doc.build_url_id(url), underline=underline, bold=bold)
    return rt


def safe_get(obj, *attrs):
    """Safely navigate nested dicts or objects."""
    for attr in attrs:
        if obj is None:
            return None
        if isinstance(obj, dict):
            obj = obj.get(attr)
        else:
            obj = getattr(obj, attr, None)
    return obj
