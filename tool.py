#!/usr/bin/python

from hogg_spec import HoggSpec
from datalist_spec import DatalistSpec
from wtex_spec import WtexSpec
import zlib
import os
import pathlib

FLAG_FFFE = b'\xFE\xFF'
HOG_NO_VALUE = b'\xFF\xFF\xFF\xFF'


class HoggFile(HoggSpec):
    def __init__(self, _io):
        super().__init__(_io)
        self.data_list = {}
        dl_file = self.extract_file(self.hog_header.datalist_file_number)
        dl_spec = DatalistSpec.from_bytes(dl_file)
        for i, e in enumerate(dl_spec.entries):
          self.data_list[i] = e.data
        for e in self.dl_journal.op_entries.op_entry:
          self.data_list[e.id] = e.str

    def extract_file(self, idx, count=None, checksum_valid=None):
        total = self.file_entries[idx].size
        unpacked = self.ea_entries[idx].unpacked_size
        offset = self.file_entries[idx].offset
        if unpacked == 0:
            return self.file_entries[idx].data
        else:
            return zlib.decompress(self.file_entries[idx].data)

    def ea_list_entry(self, idx):
        return self.ea_entries[idx]

    def get_file_name(self, idx):
        file_entry = self.file_entries[idx]
        if file_entry.flag_fffe == FLAG_FFFE and self.ea_entries[idx].name_id != HOG_NO_VALUE and self.ea_entries[idx].name_id in self.data_list:
            return self.data_list[self.ea_entries[idx].name_id].decode('UTF-8').rstrip('\0')
        else:
            return f"autofiles/{idx:08}.dat"

    def ls(self):
        for i, f in enumerate(target.file_entries):
            if f.flag_fffe == FLAG_FFFE:
                ea = self.ea_entries[i]
                print(f"{i:4} {f.size:8} {ea.unpacked_size:8} {target.get_file_name(i)}")
            else:
                print(f"{i:4} {f.size:8}        0 {target.get_file_name(i)}")

    def extract_all(self):
        for i, f in enumerate(target.file_entries):
            fn = self.get_file_name(i)
            data = self.extract_file(i,0,0)
            os.makedirs(os.path.dirname(fn), exist_ok=True)
            with open(fn,'wb') as fo:
                fo.write(data)
            print(f"extracted {fn}")

import click

@click.group()
@click.option("--verbose/--no-verbose", default=False)
@click.pass_context
def cli(ctx, verbose):
  ctx.ensure_object(dict)
  ctx.obj['VERBOSE'] = verbose

forbiddensymb = ["%", ":", "*", "?", ">", "<", "|", "+"] # "%" has to go first, otherwise you might replace it in wrong places/more than once
@cli.command()
@click.argument('hoggfile', type=click.Path(exists=True))
@click.argument('glob', required=False)
@click.option("--out-dir", "-o", default="./", help="output directory")
@click.pass_context
def extract(ctx,hoggfile,glob,out_dir):
  """ Extracts HOGGFILE to OUT_DIR"""
  hogg = HoggFile.from_file(hoggfile)
  click.echo(f'extracting {hoggfile} to {out_dir}')
  with click.progressbar(hogg.file_entries, label='Extracting archive') as bar:
    for i, f in enumerate(bar):
      if f.flag_fffe == FLAG_FFFE:
        fn = os.path.join(out_dir,hogg.get_file_name(i))
        for k, sym in enumerate(forbiddensymb):
            fn = fn.replace(sym, f"%{k}")
        if glob and not pathlib.PurePath(fn).match(glob):
          if ctx.obj['VERBOSE']: click.echo(f"skipping {fn}")
          continue
        data = hogg.extract_file(i,0,0)
        os.makedirs(os.path.dirname(fn), exist_ok=True)
        with open(fn,'wb') as fo:
          fo.write(data)
        if ctx.obj['VERBOSE']:
          click.echo(f"extracted {fn}")

@cli.command()
@click.argument('hoggfile', type=click.Path(exists=True))
def list(hoggfile):
  """ Lists files in HOGGFILE"""
  hogg = HoggFile.from_file(hoggfile)
  click.echo(f"   index   c_size   u_size file_name")
  for i, f in enumerate(hogg.file_entries):
    if f.flag_fffe == FLAG_FFFE:
      ea = hogg.ea_entries[i]
      click.echo(f"{i:8} {f.size:8} {ea.unpacked_size:8} {hogg.get_file_name(i)}")

@cli.command()
@click.argument('wtexfile', type=click.Path(exists=True))
@click.argument('ddsfile', type=click.Path(exists=False), required=False)
def convert_wtex_to_dds(wtexfile,ddsfile):
  """ Converts a WTEX file to a DDS file """
  wtex = WtexSpec.from_file(wtexfile)
  if ddsfile is None:
    ddsfile = pathlib.Path(wtexfile).with_suffix('.dds')
    with open(ddsfile,'wb') as fo:
      fo.write(wtex.data)
  click.echo(f"Wrote DDS to {ddsfile}")

if __name__ == "__main__":
  cli(obj={})

# estrConcatf(estr, "HogFile Info:\n");
# 	estrConcatf(estr, "  HogFile version: %d\n", handle->header.version);
# 	estrConcatf(estr, "  DataList Journal size: %s/%s\n", friendlyBytesBuf(handle->datalist_diff_size, buf), friendlyBytes(handle->header.dl_journal_size));
# 	estrConcatf(estr, "  Number of Files: %ld (%ld)\n", hogFileGetNumUsedFiles(handle), hogFileGetNumFiles(handle));
# 	estrConcatf(estr, "  Number of EAs: %ld (%ld)\n", hogFileGetNumUsedEAs(handle), hogFileGetNumEAs(handle));
# 	estrConcatf(estr, "  Number of Names and HeaderData blocks: %ld (%ld)\n", DataListGetNumEntries(&handle->datalist), DataListGetNumTotalEntries(&handle->datalist));
# 	estrConcatf(estr, "  Internal fragmentation: %1.1f%% (%s)\n", hogFileCalcFragmentation(handle)*100, friendlyBytes(hogFileCalcFragmentationSize(handle)));
# 	estrConcatf(estr, "  Slack: %1.1f%% (%s)\n", slack_size * 100.f / handle->file_size, friendlyBytes(slack_size));
# 	estrConcatf(estr, "  Archive header+journal size: %s (%"FORM_LL"d)\n", friendlyBytes(hogFileOffsetOfData(handle)), (U64)hogFileOffsetOfData(handle));
# 	estrConcatf(estr, "  All files total uncompressed Size: %s (%"FORM_LL"d)\n", friendlyBytes(uncompressed_size), uncompressed_size);
# 	estrConcatf(estr, "  All files total on-disk Size: %s (%"FORM_LL"d)\n", friendlyBytes(ondisk_size), ondisk_size);
# 	estrConcatf(estr, "  Required file size: %s (%"FORM_LL"d)\n", friendlyBytes(archive_size), archive_size);
# 	estrConcatf(estr, "  Actual file size: %s (%"FORM_LL"d)\n", friendlyBytes(handle->file_size), handle->file_size);
# 	bShouldDefrag = hogFileShouldDefragEx(handle, 0, &wasted_bytes);
# 	estrConcatf(estr, "  Should defrag: %s (%s wasted)\n", bShouldDefrag?"YES":"No", friendlyBytes(wasted_bytes));

#target = HoggFile.from_file("/home/lokkju/.steam/steam/steamapps/common/Cryptic Studios/Neverwinter/Live/piggs/bins.hogg")
#target.ls()
#target.extract_all()
