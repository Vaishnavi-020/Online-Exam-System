from enum import Enum

class ExamStatus(str,Enum):
    draft="draft"
    scheduled="scheduled"
    active="active"
    closed="closed"
    evaluated="evaluated"
