import enum

class TripleExtractorEnum(str, enum.Enum):
    """
    Enumeration containing the constant values for the TripleExtractor class
    """
    # Enums
    PUBLISHER = "Publisher"
    PUBLICATION = "Publication"
    ARTICLE = "Article"
    AUTHOR = "Author"
    PUMP = "Pump"
    MANUAL = "Manual"

