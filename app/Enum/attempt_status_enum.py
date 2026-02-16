from enum import Enum

class AttemptStatus(str,Enum):
    pending='pending'
    submitted='submitted'
    expired='expired'
    evaluated='evaluated'