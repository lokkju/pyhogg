# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class WtexSpec(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.wtex_header = self._root.WtexHeader(self._io, self, self._root)
        self.data = self._io.read_bytes(self.wtex_header.file_size)

    class WtexHeader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.header_size = self._io.read_u4le()
            self.file_size = self._io.read_u4le()
            self.width = self._io.read_u4le()
            self.height = self._io.read_u4le()
            self.tex_opt_flags = self._root.TexOptFlags(self._io, self, self._root)
            self.unused3 = self._io.read_f4le()
            self.max_levels = self._io.read_u1()
            self.base_levels = self._io.read_u1()
            self.unused = self._io.read_u2le()
            self.rdr_format = self._io.read_u4le()
            self.alpha = self._io.read_u1()
            self.verpad = (self._io.read_bytes(3)).decode(u"utf-8")


    class TexOptFlags(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.exclude = self._io.read_bits_int(1) != 0
            self.srbg = self._io.read_bits_int(1) != 0
            self.magfilter_point = self._io.read_bits_int(1) != 0
            self.cubemap = self._io.read_bits_int(1) != 0
            self.fix_alpha_mips = self._io.read_bits_int(1) != 0
            self.split = self._io.read_bits_int(1) != 0
            self.clamps = self._io.read_bits_int(1) != 0
            self.clampt = self._io.read_bits_int(1) != 0
            self.mirrors = self._io.read_bits_int(1) != 0
            self.mirrort = self._io.read_bits_int(1) != 0
            self.normalmap = self._io.read_bits_int(1) != 0
            self.bumpmap = self._io.read_bits_int(1) != 0
            self.alphaborder_lr = self._io.read_bits_int(1) != 0
            self.alphaborder_tb = self._io.read_bits_int(1) != 0
            self.colorborder = self._io.read_bits_int(1) != 0
            self.nomip = self._io.read_bits_int(1) != 0
            self.jpeg = self._io.read_bits_int(1) != 0
            self.volumemap = self._io.read_bits_int(1) != 0
            self.gdbe = self._io.read_bits_int(1) != 0
            self.for_fallback = self._io.read_bits_int(1) != 0
            self.colorborder_legacy = self._io.read_bits_int(1) != 0
            self.no_aniso = self._io.read_bits_int(1) != 0
            self.compression_mask = self._io.read_bits_int(4)
            self.lightmap = self._io.read_bits_int(1) != 0
            self.reversed_mips = self._io.read_bits_int(1) != 0
            self.crunch = self._io.read_bits_int(1) != 0



