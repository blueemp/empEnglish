"""Services package for empEnglish."""

try:
    from pseudocode.services.user_service import UserService
except ImportError:
    UserService = None

try:
    from pseudocode.services.question_service import QuestionService
except ImportError:
    QuestionService = None

try:
    from pseudocode.services.practice_service import PracticeService
except ImportError:
    PracticeService = None

try:
    from pseudocode.services.scoring_service import ScoringService
except ImportError:
    ScoringService = None

services_list = [
    s
    for s in [UserService, QuestionService, PracticeService, ScoringService]
    if s is not None
]
__all__ = services_list
