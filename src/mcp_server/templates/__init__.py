# Pydantic Schema and Renderer for each template

# Default Template
from .default.schema import ResumeSchema as DefaultResumeSchema
from .default.renderer import get_context as get_default_context


# Modern Template
from .modern.schema import ModernResumeSchema


from .decide_schema import get_schema