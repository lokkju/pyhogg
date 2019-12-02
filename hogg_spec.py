# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class HoggSpec(KaitaiStruct):

    class DljOpTypes(Enum):
        dlj_invalid = 0
        dlj_add_or_update = 1
        dlj_free = 2
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.hog_header = self._root.HogHeader(self._io, self, self._root)
        self.op_journal = self._io.read_bytes(self.hog_header.op_journal_size)
        self._raw_dl_journal = self._io.read_bytes(self.hog_header.dl_journal_size)
        io = KaitaiStream(BytesIO(self._raw_dl_journal))
        self.dl_journal = self._root.DlJournal(io, self, self._root)
        self.file_entries = [None] * (self.hog_header.file_list_size // self.sizeof_file_header)
        for i in range(self.hog_header.file_list_size // self.sizeof_file_header):
            self.file_entries[i] = self._root.FileHeader(self._io, self, self._root)

        self.ea_entries = [None] * (self.hog_header.ea_list_size // self.sizeof_ea_header)
        for i in range(self.hog_header.ea_list_size // self.sizeof_ea_header):
            self.ea_entries[i] = self._root.EaHeader(self._io, self, self._root)


    class DljOpEntries(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.op_entry = []
            i = 0
            while not self._io.is_eof():
                self.op_entry.append(self._root.DljOpEntry(self._io, self, self._root))
                i += 1



    class DlJournal(KaitaiStruct):
        """DataList Journal."""
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.in_use_flag = self._io.read_u4le()
            self.size = self._io.read_u4le()
            self.oldsize = self._io.read_u4le()
            self._raw_op_entries = self._io.read_bytes(self.size)
            io = KaitaiStream(BytesIO(self._raw_op_entries))
            self.op_entries = self._root.DljOpEntries(io, self, self._root)


    class HogHeader(KaitaiStruct):
        """Header to archive file."""
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.hog_header_flag = self._io.ensure_fixed_contents(b"\x0D\xF0\xAD\xDE")
            self.version = self._io.read_u2le()
            self.op_journal_size = self._io.read_u2le()
            self.file_list_size = self._io.read_u4le()
            self.ea_list_size = self._io.read_u4le()
            self.datalist_file_number = self._io.read_u4le()
            self.dl_journal_size = self._io.read_u4le()


    class EaHeader(KaitaiStruct):
        """Extended Attributes (optional) contains more information about a file."""
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.name_id = self._io.read_u4le()
            self.header_data_id = self._io.read_u4le()
            self.unpacked_size = self._io.read_u4le()
            self.flags = self._io.read_u4le()


    class DljOpEntry(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.op_type = self._root.DljOpTypes(self._io.read_u1())
            self.id = self._io.read_s4le()
            self.datasize = self._io.read_u4le()
            self.str = self._io.read_bytes(self.datasize)


    class FileHeader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.offset = self._io.read_u8le()
            self.size = self._io.read_u4le()
            self.timestamp = self._io.read_u4le()
            self.checksum = self._io.read_bytes(8)
            self.flag_fffe = self._io.read_bytes(2)
            self.reserved = self._io.read_u2le()
            self.ea_id = self._io.read_s4le()

        @property
        def data(self):
            if hasattr(self, '_m_data'):
                return self._m_data if hasattr(self, '_m_data') else None

            io = self._root._io
            _pos = io.pos()
            io.seek(self.offset)
            self._m_data = io.read_bytes(self.size)
            io.seek(_pos)
            return self._m_data if hasattr(self, '_m_data') else None


    @property
    def sizeof_file_header(self):
        if hasattr(self, '_m_sizeof_file_header'):
            return self._m_sizeof_file_header if hasattr(self, '_m_sizeof_file_header') else None

        self._m_sizeof_file_header = 32
        return self._m_sizeof_file_header if hasattr(self, '_m_sizeof_file_header') else None

    @property
    def sizeof_ea_header(self):
        if hasattr(self, '_m_sizeof_ea_header'):
            return self._m_sizeof_ea_header if hasattr(self, '_m_sizeof_ea_header') else None

        self._m_sizeof_ea_header = 16
        return self._m_sizeof_ea_header if hasattr(self, '_m_sizeof_ea_header') else None


