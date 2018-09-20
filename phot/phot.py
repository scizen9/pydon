"""Module for astronomical photometry.

"""

__version__ = "$Id$"
# $Source$


class Filter:
    """Filter class definition.

    Attributes:
    id       - short common id for filter
    fullname - verbose filter name
    responsetype    - either photon based (0) or energy based (1)
    vegazp   - Vega system zero point
    abzp     - AB system zero point
    ab_offset - offset between Vega and AB system
    area_lambda - integrated filter area (Ang)
    area_nu  - integrated filter area (Hz)
    mean_wave - mean wavelength (Ang)
    calibtype - Vega (1) or AB (2)
    vega_color - color in vega system
    vegacolsys - what system in Vega
    wave - wavelengths of response (Ang)
    response - normalized response

    """
