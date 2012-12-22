
class AssetChannel:
    """
    Container for information about one of byte buffers stored opaquely in a
    bakery.asset.Asset. More about channels can be found in the doc comment for
    Asset below.

    Attributes

    buffer [PyCapsule]  Opaque objet corresponding to the channel's byte buffer
    size [int]          The number of bytes in self.buffer
    id [str]            The string that identifies this channel among other
                        channels in the same Asset
    typeid [str]        Signifies the type of data contained in the byte 
                        buffer, chosen by convention. Tells extensions how to
                        interpet the data stored in self.buffer (which would
                        otherwise correspond to a plain void* in C)
    """

    def __init__(self, buffer = None, size = 0, id = '', typeid = ''):
        self.buffer = buffer;
        self.size = size
        self.id = id
        self.typeid = typeid

class Asset:
    """
    Tracks an intermediate object that is moving through the build pipeline.
    Wraps a set of byte buffers allocated in native C. The buffers are opaque
    to bakery itself -- they are allocated, used, and subsequently
    deallocated by extensions.

    Each asset is split into a set of channels, which are identified uniquely
    among other channels in this asset by a string. Each channel contains a
    byte buffer, size in bytes, and has a type ID. Type IDs are chosen by
    convention, and tell extensions how to interpret the data in a channel.

    Attributes

    _channels [dict]    A map from channel ID string to an AssetChannel
    _bytype [dict]      A map from type ID to a list of channel IDs, where each
                        channel in the value list has the same type ID as this
                        dictionary's key.
    """

    def __init__(self):
        self._channels = { }
        self._bytype = { }

    def get_channel(self, id):
        """ Gets the AssetChannel object with the given channel ID """

        return self._channels[id]

    def get_all(self, typeid):
        """ Gets a list of AssetChannel objects whose type ID is typeid """

        return [ self._channels[id] for id in self._bytype[typeid] ]

    def set_channel(self, buffer, size, id, typeid):
        """ 
        Stores a channel in this asset, overwriting a previously existing
        channel. Note that, since channel byte buffers are opaque to bakery,
        overwriting a channel containing a valid byte buffer will leak the old
        channel's byte buffer.

        buffer [PyCapsule]  The byte buffer containing the channel's data
        size [int]          The number of bytes in the buffer
        id [str]            The ID of the channel to set
        typeid [str]        The ID of the type of data in the buffer
        """

        ch = AssetChannel(buffer, size, id, typeid)
        self._channels[id] = ch

        if typeid not in self._bytype:
            self._bytype[typeid] = [ ]

        if id not in self._bytype[typeid]:
            self._bytype[typeid].append(id)

    def clear_channel(id):
        """
        Removes the channel with the given ID from this asset.

        Note that, since channel byte buffers are opaque to bakery, clearing a
        channel that has a valid byte buffer will leak the byte buffer.
        """

        ch = self._channels[id]
        typeid = ch.typeid

        del(self._channels[id])
        self._bytype[typeid].remove(id)

        if len(self._bytype[typeid]) == 0:
            del(self._bytype[typeid])

