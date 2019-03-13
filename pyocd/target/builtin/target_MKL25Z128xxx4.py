# pyOCD debugger
# Copyright (c) 2006-2013,2018 Arm Limited
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ..family.target_kinetis import Kinetis
from ..family.flash_kinetis import Flash_Kinetis
from ...core.memory_map import (FlashRegion, RamRegion, MemoryMap)
from ...debug.svd import SVDFile
import logging

FLASH_ALGO = { 'load_address' : 0x20000000,
               'instructions' : [
    0xE00ABE00, 0x062D780D, 0x24084068, 0xD3000040, 0x1E644058, 0x1C49D1FA, 0x2A001E52, 0x4770D1F2,
    0x4604b570, 0x4616460d, 0x49302000, 0x48306008, 0xf0004448, 0x2800f8e9, 0x2001d001, 0x2000bd70,
    0x4601e7fc, 0x47702000, 0x492ab510, 0x44484828, 0xf8c2f000, 0x2c004604, 0x2100d105, 0x44484824,
    0xf9bef000, 0xf0004604, 0x4620f838, 0xb570bd10, 0x481f4604, 0x4b1f4448, 0x68c24621, 0xf862f000,
    0x2d004605, 0x481ad107, 0x23004448, 0x68c24621, 0xf956f000, 0xf0004605, 0x4628f820, 0xb5febd70,
    0x460c4605, 0x46234616, 0x46294632, 0x44484810, 0xf90af000, 0x2f004607, 0x2201d10b, 0x46339001,
    0x90029200, 0x46294622, 0x44484809, 0xf99af000, 0xf0004607, 0x4638f802, 0x4807bdfe, 0x210168c0,
    0x43880289, 0x49041840, 0x477060c8, 0x40048100, 0x00000004, 0x6b65666b, 0xf0003000, 0x4a102070,
    0x20807010, 0xbf007010, 0x7800480d, 0x280009c0, 0x480bd0fa, 0x20207801, 0x28004008, 0x2067d001,
    0x20104770, 0x28004008, 0x2068d001, 0x07c8e7f8, 0x28000fc0, 0x2069d001, 0x2000e7f2, 0x0000e7f0,
    0x40020000, 0xb081b5ff, 0x460d4604, 0xf0009804, 0x4606f89f, 0xd0022e00, 0xb0054630, 0x2304bdf0,
    0x46204629, 0xf0009a03, 0x4606f876, 0xd0012e00, 0xe7f24630, 0x18289803, 0x46381e47, 0xf00068e1,
    0x2900f983, 0x4638d009, 0xf00068e1, 0x1c40f97d, 0x68e19000, 0x43489800, 0xe0131e47, 0x4478480c,
    0x60056800, 0x490b2009, 0xf7ff71c8, 0x4606ffa7, 0x280069a0, 0x69a0d001, 0x2e004780, 0xe003d000,
    0x194568e0, 0xd9e942bd, 0x4630bf00, 0x0000e7c5, 0x00000462, 0x40020000, 0x4604b570, 0x4628460d,
    0xf856f000, 0x2e004606, 0x4630d001, 0x2c00bd70, 0x2004d101, 0x2044e7fa, 0x71c84902, 0xff7ef7ff,
    0x0000e7f4, 0x40020000, 0x29004601, 0x2004d101, 0x482a4770, 0x010068c0, 0x00400f00, 0x447b4b28,
    0x03025a18, 0xd1012a00, 0xe7f12064, 0x60082000, 0x2001604a, 0x02806088, 0x200060c8, 0x61486108,
    0xbf006188, 0x4602e7e4, 0xd1012a00, 0x47702004, 0x20006191, 0xb530e7fb, 0x2c004604, 0x2004d101,
    0x1e58bd30, 0x28004008, 0x1e58d103, 0x28004010, 0x2065d001, 0x6820e7f4, 0xd8054288, 0x68206865,
    0x188d1940, 0xd20142a8, 0xe7e92066, 0xe7e72000, 0x480c4601, 0xd0014281, 0x4770206b, 0xe7fc2000,
    0x2b004603, 0x2004d101, 0x290f4770, 0x2a04d801, 0x2004d001, 0x2000e7f8, 0x0000e7f6, 0x40048040,
    0x000003c0, 0x6b65666b, 0xb081b5ff, 0x46144607, 0x2c00461d, 0x2004d102, 0xbdf0b005, 0x462a2304,
    0x99024638, 0xffb7f7ff, 0x2e004606, 0x4630d001, 0xe01ce7f2, 0x44794910, 0x68099802, 0xcc016008,
    0x4479490d, 0x6809390c, 0x20066048, 0x71c8490b, 0xfef4f7ff, 0x69b84606, 0xd0012800, 0x478069b8,
    0xd0002e00, 0x9802e005, 0x90021d00, 0x2d001f2d, 0xbf00d1e0, 0xe7cf4630, 0x0000030a, 0x40020000,
    0xb083b5ff, 0x2304460c, 0x9a054621, 0xf7ff9803, 0x9002ff82, 0x28009802, 0x9802d002, 0xbdf0b007,
    0x68919a03, 0xf0006850, 0x4605f88f, 0x42684261, 0x424e4001, 0xd10042a6, 0x9f051976, 0x1b30e027,
    0x98019001, 0xd90042b8, 0x98019701, 0x90000880, 0x44784811, 0x60046800, 0x49102001, 0x980071c8,
    0x0e010400, 0x72c1480d, 0x9800490c, 0x98067288, 0xf7ff7248, 0x9002fea3, 0x28009802, 0x9802d001,
    0x9801e7cc, 0x98011a3f, 0x19761824, 0x2f00bf00, 0x2000d1d5, 0x0000e7c2, 0x0000026e, 0x40020000,
    0x4604b570, 0x2c00460d, 0x2004d101, 0x2040bd70, 0x71c84903, 0x71854608, 0xfe80f7ff, 0x0000e7f6,
    0x40020000, 0xb081b5ff, 0x4617460c, 0x2d00461d, 0x2004d102, 0xbdf0b005, 0x463a2304, 0x98014621,
    0xff19f7ff, 0x2e004606, 0x4630d001, 0xe022e7f2, 0x44784813, 0x60046800, 0x49122002, 0x980a71c8,
    0x490f72c8, 0x39124479, 0x68096828, 0xf7ff6088, 0x4606fe55, 0xd00b2e00, 0x2800980b, 0x980bd001,
    0x980c6004, 0xd0022800, 0x980c2100, 0xe0046001, 0x1d2d1f3f, 0x2f001d24, 0xbf00d1da, 0xe7c94630,
    0x000001ce, 0x40020000, 0x09032200, 0xd32c428b, 0x428b0a03, 0x2300d311, 0xe04e469c, 0x430b4603,
    0x2200d43c, 0x428b0843, 0x0903d331, 0xd31c428b, 0x428b0a03, 0x4694d301, 0x09c3e03f, 0xd301428b,
    0x1ac001cb, 0x09834152, 0xd301428b, 0x1ac0018b, 0x09434152, 0xd301428b, 0x1ac0014b, 0x09034152,
    0xd301428b, 0x1ac0010b, 0x08c34152, 0xd301428b, 0x1ac000cb, 0x08834152, 0xd301428b, 0x1ac0008b,
    0x08434152, 0xd301428b, 0x1ac0004b, 0x1a414152, 0x4601d200, 0x46104152, 0xe05d4770, 0xd0000fca,
    0x10034249, 0x4240d300, 0x22004053, 0x0903469c, 0xd32d428b, 0x428b0a03, 0x22fcd312, 0xba120189,
    0x428b0a03, 0x0189d30c, 0x428b1192, 0x0189d308, 0x428b1192, 0x0189d304, 0x1192d03a, 0x0989e000,
    0x428b09c3, 0x01cbd301, 0x41521ac0, 0x428b0983, 0x018bd301, 0x41521ac0, 0x428b0943, 0x014bd301,
    0x41521ac0, 0x428b0903, 0x010bd301, 0x41521ac0, 0x428b08c3, 0x00cbd301, 0x41521ac0, 0x428b0883,
    0x008bd301, 0x41521ac0, 0x0843d2d9, 0xd301428b, 0x1ac0004b, 0x1a414152, 0x4601d200, 0x41524663,
    0x4610105b, 0x4240d301, 0xd5002b00, 0x47704249, 0x105b4663, 0x4240d300, 0x2000b501, 0x46c046c0,
    0x0002bd02, 0x00000004, 0x00000008, 0x00000010, 0x00000020, 0x00000040, 0x00000000, 0x00000000,
    0x00000020, 0x40020004, 0x00000000,
                                ],
               'pc_init' : 0x20000021,
               'pc_eraseAll' : 0x20000049,
               'pc_erase_sector' : 0x2000006F,
               'pc_program_page' : 0x2000009F,
               'begin_stack' : 0x20000800,
               'begin_data' : 0x20000800,       # Analyzer uses a max of 1 KB data (256 pages * 4 bytes / page)
                                                # Note: 128 pages on KL25 and KL26, 256 pages on KL46
               'static_base' : 0x20000000 + 0x20 + 0x5E8,
               'min_program_length' : 4,
               'page_buffers' : [0x20000800, 0x20000c00], # Enable double buffering
               'analyzer_supported' : True,
               'analyzer_address' : 0x1ffff000  # Analyzer 0x1ffff000..0x1ffff600
              };

class KL25Z(Kinetis):

    memoryMap = MemoryMap(
        FlashRegion(    start=0,           length=0x20000,      blocksize=0x400, is_boot_memory=True,
            algo=FLASH_ALGO, flash_class=Flash_Kinetis),
        RamRegion(      start=0x1ffff000,  length=0x4000)
        )

    def __init__(self, link):
        super(KL25Z, self).__init__(link, self.memoryMap)
        self._svd_location = SVDFile(vendor="Freescale", filename="MKL25Z4.svd", is_local=False)

