#!/usr/bin/python

from hogg_spec import HoggSpec
import zlib
import os

FLAG_FFFE = b'\xFE\xFF'
HOG_NO_VALUE = b'\xFF\xFF\xFF\xFF'


class HoggFile(HoggSpec):
    def __init__(self, _io):
        super().__init__(_io)
        self.data_list = {}
        for e in self.dl_journal.op_entries.op_entry:
            self.data_list[e.id] = e.str

    def file_extract(self,idx, count, checksum_valid):
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

    def extract_all(self):
        for i, f in enumerate(target.file_entries):
            fn = self.get_file_name(i)
            data = self.file_extract(i,0,0)
            os.makedirs(os.path.dirname(fn), exist_ok=True)
            with open(fn,'wb') as fo:
                fo.write(data)
            print(f"extracted {fn}")

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

target = HoggFile.from_file("/home/lokkju/.steam/steam/steamapps/common/Cryptic Studios/Neverwinter/Live/piggs/bins.hogg")
target.ls()
target.extract_all()