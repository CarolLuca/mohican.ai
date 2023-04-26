class ComplexityLevel(object):
    """
    Class to represent the complexity levels
    of a site or an ad template.

    Fields
    ======
    chromatic_level
        The chromatic level as described in the
        image_utils.py

    informational_level
        The informational level as described in
        the site_utils.py
    """

    def __init__(self, _chromatic_level, _informational_level):
        self.chromatic_level = _chromatic_level
        self.informational_level = _informational_level
