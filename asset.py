
class Asset:
    """ 
    Represents an asset that is currently moving through the build pipeline.
    
    Asset is a typed wrapper around a native C++ byte buffer, allocated and
    manipulated by bakery extensions.

    Attributes:
        name [str]      This asset's unique ID
        typeid [str]    The type of binary asset this Asset wraps
        data [?]        A pointer to a native byte array containing the asset
                        data
    """

    name = "none"
    typeid = "none"
    data = None

    def __init__(self, typeid):
        self.typeid = typeid


