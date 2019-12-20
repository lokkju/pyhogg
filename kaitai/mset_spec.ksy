meta:
  id: mset_spec
  file-extension: mset
  endian: le

seq:
  - id: header_size
    type: u4
  - id: mset_header
    type: mset_header
    size: header_size - 4
  - id: filelist
    type: filelist
types:
  pstr:
    seq:
    - id: len
      type: u2
    - id: str
      type: str
      size: len
      encoding: UTF-8
    - id: padding
      size: (4 - (len + 2) % 4) % 4
  filelist:
    seq:
    - id: header
      contents: [0x06,0x00,'Files1']
    - id: size
      type: u4
    - id: count
      type: u4
    - id: filelist_entries
      type: filelist_entry
      repeat: expr
      repeat-expr: count
  filelist_entry:
    seq:
    - id: name
      type: pstr
    - id: date
      type: u4
  mset_header:
    meta:
      endian: be
    seq:
      - id: version
        type: u4
      - id: crc
        type: u4
      - id: model_count
        type: u2
      - id: mset_models
        type: mset_header_model
        repeat: expr
        repeat-expr: model_count
  mset_header_model:
    meta:
      endian: be
    seq:
    - id: slen
      type: u2
    - id: name
      type: str
      encoding: "utf-8"
      size: slen
    - id: lodcount
      type: u2
    - id: lods
      type: lod_header
    - id: collision_header
      type: collision_header
  collision_header:
    meta:
      endian: be
    seq:
    - id: collision_data_offet
      type: u4
    - id: collision_data_length
      type: u4
    - id: collision_total_length
      type: u4
    instances:
      colision_data:
        io: _root._io
        pos: collision_data_offet
        size: collision_total_length

  lod_header:
    meta:
      endian: be
    seq:
    - id: data_offset
      type: u4
    - id: data_length
      type: u4
    instances:
      data:
        io: _root._io
        pos:  data_offset
        size: data_length

      
