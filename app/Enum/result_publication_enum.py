from enum import Enum

class ResultPublication(str,Enum):
    published='published'
    not_published='not_published'