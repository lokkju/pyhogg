meta:
  id: datalist_spec
  file-extension: datalist
  endian: le

seq:
  - id: dl_header
    type: datalist_header
  - id: entries
    type: datalist_entry
    repeat: eos
types:
  datalist_header:
    seq:
    - id: version
      type: u4
    - id: num_entries
      type: u4
  datalist_entry:
    seq:
    - id: data_size
      type: u4
    - id: data
      size: data_size
