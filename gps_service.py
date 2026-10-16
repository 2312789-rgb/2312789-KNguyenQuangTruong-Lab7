class GPSSignalLostError(Exception):
    """Raised when the device loses its GPS signal."""


def get_current_location():
    """Return the simulated GPS coordinates for the device."""
    return (10.0, 105.0)
