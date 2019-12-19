meta:
  id: wtex_spec
  file-extension: wtex
  endian: le

seq:
  - id: wtex_header
    type: wtex_header
  - id: data
    size: wtex_header.file_size
types:
  wtex_header:
    seq:
      - id: header_size
        type: u4
      - id: file_size
        type: u4
      - id: width
        type: u4
      - id: height
        type: u4
      - id: tex_opt_flags
        type: tex_opt_flags
      - id: unused3
        type: f4
      - id: max_levels
        type: u1
      - id: base_levels
        type: u1
      - id: unused
        type: u2
      - id: rdr_format
        type: u4
      - id: alpha
        type: u1
      - id: verpad
        type: str
        encoding: "utf-8"
        size: 3

  tex_opt_flags:
    seq:
      - id: exclude
        type: b1
      - id: srbg
        type: b1
      - id: magfilter_point
        type: b1
      - id: cubemap
        type: b1
      - id: fix_alpha_mips
        type: b1
      - id: split
        type: b1
      - id: clamps
        type: b1
      - id: clampt
        type: b1
      - id: mirrors
        type: b1
      - id: mirrort
        type: b1
      - id: normalmap
        type: b1
      - id: bumpmap
        type: b1
      - id: alphaborder_lr
        type: b1
      - id: alphaborder_tb
        type: b1
      - id: colorborder
        type: b1
      - id: nomip
        type: b1
      - id: jpeg
        type: b1
      - id: volumemap
        type: b1
      - id: gdbe
        type: b1
      - id: for_fallback
        type: b1
      - id: colorborder_legacy
        type: b1
      - id: no_aniso
        type: b1
      - id: compression_mask
        type: b4
      - id: lightmap
        type: b1
      - id: reversed_mips
        type: b1
      - id: crunch
        type: b1
        
