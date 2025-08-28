# Package init for smart_librarian
# Import minimal helpers; defer heavy retriever imports to build_retriever
from .tools import get_summary_by_title
from .filters import is_clean_text
from .utils import load_env
