# Copyright (c) 2010 - 2023, Nordic Semiconductor ASA All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of Nordic Semiconductor ASA nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY, AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL NORDIC SEMICONDUCTOR ASA OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import logging
from ...core.memory_map import FlashRegion, RamRegion, MemoryMap
from ...debug.svd.loader import SVDFile
from ..family.target_nRF53 import NRF53
from ...flash.flash import Flash

LOG = logging.getLogger(__name__)

class Flash_NRF5340(Flash):
    def __init__(self, target, flash_algo):
        super(Flash_NRF5340, self).__init__(target, flash_algo)

    def prepare_target(self):
        self.target.other_core.reset_and_halt()


FLASH_ALGO_APP = {
    'load_address' : 0x20000000,

    # Flash algorithm as a hex string
    'instructions': [
    0xe7fdbe00,
    0xf240b5b0, 0xf2c00504, 0x20000500, 0x0105eb09, 0x0005f849, 0x0001e9c1, 0xb2d060c8, 0xf0004614,
    0xb120fa3d, 0x0105eb09, 0x0402e9c1, 0xeb09bdb0, 0x21010005, 0xf0006041, 0x2000fa2b, 0xbf00bdb0,
    0x4604b510, 0xf0002000, 0xb138fa29, 0x0104f240, 0x0100f2c0, 0xe9c14449, 0xbd100402, 0x0004f240,
    0x0000f2c0, 0x0100eb09, 0x29006889, 0x2000bf04, 0xf244bd10, 0xf2c20100, 0x22010100, 0xf859600a,
    0x44482000, 0x6842604a, 0x6882608a, 0x68c060ca, 0x20006108, 0xbf00bd10, 0x0004f240, 0x0000f2c0,
    0xf8492101, 0x44481000, 0xe9c02100, 0x60c11101, 0xba28f000, 0xf240b5b0, 0x46040504, 0x0500f2c0,
    0xf8492002, 0xeb090005, 0x21000005, 0x1101e9c0, 0xf00060c1, 0xfbb4f9a5, 0xfb01f1f0, 0xb1304010,
    0x0005eb09, 0xe9c02103, 0x20651402, 0xeb09bdb0, 0x21010005, 0xf0006041, 0x42a0f9ad, 0xf000d813,
    0x42a0f9ab, 0xeb09d90f, 0x21020005, 0x46206041, 0xf9c2f000, 0xbf1c2803, 0xbdb02067, 0xf0004620,
    0x2000f9e7, 0xeb09bdb0, 0x21040005, 0x1402e9c0, 0xbdb02066, 0x41f0e92d, 0x0704f240, 0xf2c04604,
    0x46150700, 0x2003460e, 0x0107eb09, 0x07a32200, 0x0007f849, 0x2201e9c1, 0xd00660ca, 0x0107eb09,
    0x0402e9c1, 0xe8bd2065, 0xeb0981f0, 0x21010007, 0xf0006041, 0x42a0f96f, 0xf000d815, 0x42a0f96d,
    0xeb09d911, 0x21030007, 0xeb066041, 0xf0000804, 0x4580f963, 0xeb09d90f, 0x21040007, 0x1802e9c0,
    0xe8bd2066, 0xeb0981f0, 0x21040007, 0x1402e9c0, 0xe8bd2066, 0xeb0981f0, 0x21040007, 0xf0006041,
    0xb130f969, 0x0007eb09, 0x60812102, 0xe8bd2067, 0xeb0981f0, 0x21050007, 0x46206041, 0xf95cf000,
    0xd2072802, 0x0007eb09, 0xe9c02102, 0x20671402, 0x81f0e8bd, 0x22ffd10f, 0x46314620, 0xf836f000,
    0x2003b148, 0x0007f849, 0x0007eb09, 0x60412105, 0xe8bd2067, 0x200381f0, 0x0007f849, 0xebb02000,
    0xeb090f96, 0xf04f0107, 0x604a0206, 0xe8bdbf08, 0xea4f81f0, 0x26000896, 0x0026f854, 0xd10c3001,
    0x0026f855, 0x0026f844, 0xf942f000, 0x45463601, 0x0000f04f, 0xe8bdd3f0, 0xeb0981f0, 0x21050007,
    0xe9c019a2, 0x20681202, 0x81f0e8bd, 0x41f0e92d, 0x0704f240, 0x4604460d, 0x0700f2c0, 0x46162005,
    0x0007f849, 0x0007eb09, 0x07aa2100, 0x1101e9c0, 0xd00760c1, 0x0007eb09, 0xe9c02103, 0x20651502,
    0x81f0e8bd, 0x0007eb09, 0x60412102, 0xf8d2f000, 0xd81542a0, 0xf8d0f000, 0xd91142a0, 0x0007eb09,
    0x60412103, 0x0804eb05, 0xf8c6f000, 0xd90f4580, 0x0007eb09, 0xe9c02104, 0x20661802, 0x81f0e8bd,
    0x0007eb09, 0xe9c02104, 0x20661402, 0x81f0e8bd, 0x0007eb09, 0x2d002104, 0xbf046041, 0xe8bd2000,
    0x210081f0, 0xbf00e007, 0x42a93101, 0x0000f04f, 0xe8bdbf28, 0x5c6081f0, 0xd0f542b0, 0xeb091860,
    0x22050107, 0x2002e9c1, 0xe8bd2001, 0xbf0081f0, 0x41f0e92d, 0x0504f240, 0xf2c04604, 0x20040500,
    0x460f4690, 0x0005f849, 0x0005eb09, 0x07a22100, 0x1101e9c0, 0xd00860c1, 0x0005eb09, 0x26652103,
    0x1402e9c0, 0xe8bd4630, 0xeb0981f0, 0x21010005, 0xf0006041, 0x42a0f86f, 0xf000d812, 0x42a0f86d,
    0xeb09d90e, 0x21030005, 0x193e6041, 0xf864f000, 0xd90e4286, 0x0005eb09, 0xe9c02104, 0xe0041602,
    0x0005eb09, 0xe9c02104, 0x26661402, 0xe8bd4630, 0x210081f0, 0x0f97ebb1, 0x0005eb09, 0x0104f04f,
    0xd00b6041, 0x210008b8, 0xf8586822, 0x429a3021, 0x3101d10b, 0xf1044281, 0xd3f50404, 0x0005eb09,
    0x60412105, 0xe8bd4630, 0xeb0981f0, 0x21060005, 0x1402e9c0, 0xe8bd4620, 0x000081f0, 0x1030f240,
    0x00fff2c0, 0x31016801, 0x6800bf1c, 0xf6404770, 0xf2cf71e0, 0x78080100, 0xf3616849, 0x4770200b,
    0x2020f240, 0x00fff2c0, 0x31016801, 0x6800bf14, 0x5080f44f, 0xbf004770, 0x2024f240, 0x00fff2c0,
    0x31016801, 0x6800bf14, 0x7000f44f, 0xbf004770, 0x47702000, 0x47702000, 0xf7ffb510, 0x4604ffe1,
    0xffeaf7ff, 0xf004fb00, 0xbf00bd10, 0x42814401, 0x2001bf9c, 0xe0034770, 0xbf244288, 0x47702001,
    0x2b04f850, 0xbf1c3201, 0x47702000, 0xbf00e7f4, 0xbf004770, 0x47702000, 0x47702003, 0xbf842803,
    0x47702069, 0xb240b580, 0xf851a105, 0xf2490020, 0xf2c55104, 0x60080103, 0xf80af000, 0xbd802000,
    0x00000000, 0x00000002, 0x00000001, 0x00000000, 0x4000f249, 0x0003f2c5, 0x29006801, 0x4770d0fc,
    0x500cf249, 0x0003f2c5, 0x60012101, 0xbf00e7f0, 0x9000b081, 0xf04f9800, 0x600131ff, 0xe7e7b001,
    0x47702069, 0xf7ffb5b0, 0x4604ffa7, 0x2500b140, 0xf7ff4628, 0xf7ffffed, 0x4405ff83, 0xd3f742a5,
    0xbdb02000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000
    ],

    # Relative function addresses
    'pc_init': 0x20000005,
    'pc_unInit': 0x20000045,
    'pc_program_page': 0x20000139,
    'pc_erase_sector': 0x200000b9,
    'pc_eraseAll': 0x2000009d,

    'static_base' : 0x20000000 + 0x00000004 + 0x00000524,
    'begin_stack' : 0x20003540,
    'begin_data' : 0x20000000 + 0x1000,
    'page_size' : 0x1000,
    'analyzer_supported' : False,
    'analyzer_address' : 0x00000000,
    # Enable double buffering
    'page_buffers' : [
        0x20000540,
        0x20001540
    ],
    'min_program_length' : 0x1000,

    # Relative region addresses and sizes
    'ro_start': 0x4,
    'ro_size': 0x524,
    'rw_start': 0x528,
    'rw_size': 0x4,
    'zi_start': 0x52c,
    'zi_size': 0x10,

    # Flash information
    'flash_start': 0x0,
    'flash_size': 0x200000,
    'sector_sizes': (
        (0x0, 0x1000),
    )
}


FLASH_ALGO_NET = {
    'load_address' : 0x21000000,

    # Flash algorithm as a hex string
    'instructions': [
    0xe7fdbe00,
    0xf240b5b0, 0xf2c00504, 0x20000500, 0x0105eb09, 0x0005f849, 0x0001e9c1, 0xb2d060c8, 0xf0004614,
    0xb120fa3f, 0x0105eb09, 0x0402e9c1, 0xeb09bdb0, 0x21010005, 0xf0006041, 0x2000fa2d, 0xbf00bdb0,
    0x4604b510, 0xf0002000, 0xb138fa2b, 0x0104f240, 0x0100f2c0, 0xe9c14449, 0xbd100402, 0x0004f240,
    0x0000f2c0, 0x0100eb09, 0x29006889, 0x2000bf04, 0xf244bd10, 0xf2c20100, 0x22011100, 0xf859600a,
    0x44482000, 0x6842604a, 0x6882608a, 0x68c060ca, 0x20006108, 0xbf00bd10, 0x0004f240, 0x0000f2c0,
    0xf8492101, 0x44481000, 0xe9c02100, 0x60c11101, 0xba2af000, 0xf240b5b0, 0x46040504, 0x0500f2c0,
    0xf8492002, 0xeb090005, 0x21000005, 0x1101e9c0, 0xf00060c1, 0xfbb4f9a5, 0xfb01f1f0, 0xb1304010,
    0x0005eb09, 0xe9c02103, 0x20651402, 0xeb09bdb0, 0x21010005, 0xf0006041, 0x42a0f9ab, 0xf000d813,
    0x42a0f9ab, 0xeb09d90f, 0x21020005, 0x46206041, 0xf9c4f000, 0xbf1c2803, 0xbdb02067, 0xf0004620,
    0x2000f9e9, 0xeb09bdb0, 0x21040005, 0x1402e9c0, 0xbdb02066, 0x41f0e92d, 0x0704f240, 0xf2c04604,
    0x46150700, 0x2003460e, 0x0107eb09, 0x07a32200, 0x0007f849, 0x2201e9c1, 0xd00660ca, 0x0107eb09,
    0x0402e9c1, 0xe8bd2065, 0xeb0981f0, 0x21010007, 0xf0006041, 0x42a0f96d, 0xf000d815, 0x42a0f96d,
    0xeb09d911, 0x21030007, 0xeb066041, 0xf0000804, 0x4580f963, 0xeb09d90f, 0x21040007, 0x1802e9c0,
    0xe8bd2066, 0xeb0981f0, 0x21040007, 0x1402e9c0, 0xe8bd2066, 0xeb0981f0, 0x21040007, 0xf0006041,
    0xb130f96b, 0x0007eb09, 0x60812102, 0xe8bd2067, 0xeb0981f0, 0x21050007, 0x46206041, 0xf95ef000,
    0xd2072802, 0x0007eb09, 0xe9c02102, 0x20671402, 0x81f0e8bd, 0x22ffd10f, 0x46314620, 0xf836f000,
    0x2003b148, 0x0007f849, 0x0007eb09, 0x60412105, 0xe8bd2067, 0x200381f0, 0x0007f849, 0xebb02000,
    0xeb090f96, 0xf04f0107, 0x604a0206, 0xe8bdbf08, 0xea4f81f0, 0x26000896, 0x0026f854, 0xd10c3001,
    0x0026f855, 0x0026f844, 0xf944f000, 0x45463601, 0x0000f04f, 0xe8bdd3f0, 0xeb0981f0, 0x21050007,
    0xe9c019a2, 0x20681202, 0x81f0e8bd, 0x41f0e92d, 0x0704f240, 0x4604460d, 0x0700f2c0, 0x46162005,
    0x0007f849, 0x0007eb09, 0x07aa2100, 0x1101e9c0, 0xd00760c1, 0x0007eb09, 0xe9c02103, 0x20651502,
    0x81f0e8bd, 0x0007eb09, 0x60412102, 0xf8d0f000, 0xd81542a0, 0xf8d0f000, 0xd91142a0, 0x0007eb09,
    0x60412103, 0x0804eb05, 0xf8c6f000, 0xd90f4580, 0x0007eb09, 0xe9c02104, 0x20661802, 0x81f0e8bd,
    0x0007eb09, 0xe9c02104, 0x20661402, 0x81f0e8bd, 0x0007eb09, 0x2d002104, 0xbf046041, 0xe8bd2000,
    0x210081f0, 0xbf00e007, 0x42a93101, 0x0000f04f, 0xe8bdbf28, 0x5c6081f0, 0xd0f542b0, 0xeb091860,
    0x22050107, 0x2002e9c1, 0xe8bd2001, 0xbf0081f0, 0x41f0e92d, 0x0504f240, 0xf2c04604, 0x20040500,
    0x460f4690, 0x0005f849, 0x0005eb09, 0x07a22100, 0x1101e9c0, 0xd00860c1, 0x0005eb09, 0x26652103,
    0x1402e9c0, 0xe8bd4630, 0xeb0981f0, 0x21010005, 0xf0006041, 0x42a0f86d, 0xf000d812, 0x42a0f86d,
    0xeb09d90e, 0x21030005, 0x193e6041, 0xf864f000, 0xd90e4286, 0x0005eb09, 0xe9c02104, 0xe0041602,
    0x0005eb09, 0xe9c02104, 0x26661402, 0xe8bd4630, 0x210081f0, 0x0f97ebb1, 0x0005eb09, 0x0104f04f,
    0xd00b6041, 0x210008b8, 0xf8586822, 0x429a3021, 0x3101d10b, 0xf1044281, 0xd3f50404, 0x0005eb09,
    0x60412105, 0xe8bd4630, 0xeb0981f0, 0x21060005, 0x1402e9c0, 0xe8bd4620, 0x000081f0, 0x1030f240,
    0x10fff2c0, 0x31016801, 0x6800bf1c, 0xf6404770, 0xf2cf71e0, 0x78080100, 0xf3616849, 0x4770200b,
    0x2020f240, 0x10fff2c0, 0x31016801, 0x6800bf14, 0x6000f44f, 0xbf004770, 0x2024f240, 0x10fff2c0,
    0x31016801, 0x6800bf14, 0x47702080, 0x47702000, 0x7080f04f, 0xbf004770, 0xf7ffb510, 0x4604ffe1,
    0xffeaf7ff, 0xf004fb00, 0x7080f100, 0xbf00bd10, 0x42814401, 0x2001bf9c, 0xe0034770, 0xbf244288,
    0x47702001, 0x2b04f850, 0xbf1c3201, 0x47702000, 0xbf00e7f4, 0xbf004770, 0x47702000, 0x47702003,
    0xbf842803, 0x47702069, 0xb240b580, 0xf851a105, 0xf2400020, 0xf2c45104, 0x60081108, 0xf80af000,
    0xbd802000, 0x00000000, 0x00000002, 0x00000001, 0x00000000, 0x4000f240, 0x1008f2c4, 0x29006801,
    0x4770d0fc, 0x500cf240, 0x1008f2c4, 0x60012101, 0xbf00e7f0, 0x9000b081, 0xf04f9800, 0x600131ff,
    0xe7e7b001, 0x47702069, 0xf7ffb5b0, 0x4604ffa5, 0x7f80f1b0, 0xf04fd90a, 0xbf007580, 0xf7ff4628,
    0xf7ffffe9, 0x4405ff7d, 0xd3f742a5, 0xbdb02000, 0x00000000, 0x00000000, 0x00000000, 0x00000000,
    0x00000000
    ],

    # Relative function addresses
    'pc_init': 0x21000005,
    'pc_unInit': 0x21000045,
    'pc_program_page': 0x21000139,
    'pc_erase_sector': 0x210000b9,
    'pc_eraseAll': 0x2100009d,

    'static_base' : 0x21000000 + 0x00000004 + 0x00000530,
    'begin_stack' : 0x21002550,
    'begin_data' : 0x21000000 + 0x1000,
    'page_size' : 0x800,
    'analyzer_supported' : False,
    'analyzer_address' : 0x00000000,
    # Enable double buffering
    'page_buffers' : [
        0x21000550,
        0x21000d50
    ],
    'min_program_length' : 0x800,

    # Relative region addresses and sizes
    'ro_start': 0x4,
    'ro_size': 0x530,
    'rw_start': 0x534,
    'rw_size': 0x4,
    'zi_start': 0x538,
    'zi_size': 0x10,

    # Flash information
    'flash_start': 0x1000000,
    'flash_size': 0x40000,
    'sector_sizes': (
        (0x1000000, 0x800),
    )
}


FLASH_ALGO_APP_UICR = {
    'load_address' : 0x20000000,

    # Flash algorithm as a hex string
    'instructions': [
    0xe7fdbe00,
    0xf240b570, 0xf2c00604, 0x25000600, 0x0006eb09, 0x5006f849, 0x5501e9c0, 0xb2d060c5, 0xf0004614,
    0x2800fa99, 0xeb09bf1e, 0xe9c10106, 0x46050402, 0xbd704628, 0x4604b510, 0xf0002000, 0xf240fa8b,
    0xf2c00104, 0x44490100, 0xe9c1b110, 0xe0030402, 0x29006889, 0xbd10bf08, 0x0100f244, 0x0100f2c2,
    0x600a2201, 0x0204f240, 0x0200f2c0, 0x3002f859, 0x604b444a, 0x608b6853, 0x60cb6893, 0x610a68d2,
    0xbf00bd10, 0xf240b580, 0xf2c00004, 0x21010000, 0x1000f849, 0x21004448, 0x1101e9c0, 0xf00060c1,
    0x2000fa8f, 0xbf00bd80, 0xf240b570, 0xf2c00404, 0x20020400, 0x0504eb09, 0xf8492600, 0xe9c50004,
    0x60ee6601, 0xf9e0f000, 0xf8492105, 0x21011004, 0x0f03f010, 0x1601e9c5, 0xd00460ee, 0x0104eb09,
    0x608a2203, 0xf248e013, 0xf2c00c00, 0xeb000cff, 0xf50c010c, 0xeb095380, 0x42990204, 0x0303f04f,
    0xd9106053, 0x0004eb09, 0x60822204, 0xeb094608, 0x60c80104, 0xfa7ef000, 0x28694601, 0x2900bf14,
    0x46082100, 0xb1f0bd70, 0xf81c2300, 0x29ff1003, 0x1c59d123, 0xd2164281, 0x0103eb0c, 0x2aff784a,
    0x1c9ad114, 0xd20e4282, 0x2aff788a, 0x1cdad111, 0xd2084282, 0x29ff78c9, 0x3304d10e, 0xf04f4283,
    0xd3e20100, 0x2100e7dd, 0xbd704608, 0x0301f043, 0xf043e003, 0xe0000302, 0xeb0c4613, 0xeb090003,
    0x22050104, 0xbf00e7ad, 0xf240b570, 0xf2c00c04, 0x23050c00, 0x300cf849, 0x030ceb09, 0x0e00f04f,
    0xe9c30784, 0xf8c3ee01, 0xd005e00c, 0x010ceb09, 0xe9c12203, 0xe00c2002, 0x030ceb09, 0x0e01f04f,
    0xf8c3078c, 0xd007e004, 0x000ceb09, 0xe9c02203, 0x23652102, 0xbd704618, 0x7efff648, 0x0efff2c0,
    0x030ceb09, 0x45702402, 0xd905605c, 0x010ceb09, 0xe9c12204, 0xe00d2002, 0xf10e180b, 0xeb090501,
    0x2603040c, 0x606642ab, 0xeb09d907, 0x2104000c, 0x1302e9c0, 0x46182366, 0xb319bd70, 0x0e00f04f,
    0x300ef810, 0xd1274293, 0x0301f10e, 0xd219428b, 0x030eeb00, 0x4294785c, 0xf10ed117, 0x428c0402,
    0x789cd210, 0xd1134294, 0x0403f10e, 0xd209428c, 0x429378db, 0xf10ed10f, 0x458e0e04, 0x0300f04f,
    0xe010d3de, 0x46182300, 0xf04ebd70, 0xe0030e01, 0x0e02f04e, 0x46a6e000, 0xeb094470, 0x2205010c,
    0xe9c12301, 0x46182002, 0xbf00bd70, 0x41f0e92d, 0x0604f240, 0x0600f2c0, 0x46044615, 0xeb092003,
    0x23000206, 0xf849078f, 0xe9c20006, 0x60d33301, 0xeb09d006, 0xe9c20206, 0x20650102, 0x81f0e8bd,
    0x70fff648, 0x00fff2c0, 0x0206eb09, 0x42842302, 0xd9076053, 0x0006eb09, 0xe9c02104, 0x20661402,
    0x81f0e8bd, 0x3001190a, 0x0306eb09, 0x42822703, 0xd907605f, 0x0006eb09, 0xe9c02104, 0x20661202,
    0x81f0e8bd, 0xebb02000, 0xd01b0f91, 0x0891ea4f, 0xe00c2700, 0x0027f855, 0x0027f844, 0xf940f000,
    0x45473701, 0x0000f04f, 0xe8bdbf28, 0xf85481f0, 0x30010027, 0xeb09d0ee, 0x21050006, 0xe9c019e2,
    0x20681202, 0x81f0e8bd, 0x41f0e92d, 0x0c04f240, 0x0c00f2c0, 0xf8492304, 0xeb09300c, 0x2600030c,
    0xe9c30785, 0x60de6601, 0xeb09d005, 0x2203010c, 0x2002e9c1, 0xeb09e00a, 0x2601030c, 0x605e078d,
    0xeb09d008, 0x2203000c, 0x2102e9c0, 0x46182365, 0x81f0e8bd, 0x74fff648, 0x04fff2c0, 0x030ceb09,
    0x42a02602, 0xd905605e, 0x010ceb09, 0xe9c12204, 0xe00c2002, 0x3401180b, 0x060ceb09, 0x42a32503,
    0xd9086075, 0x000ceb09, 0xe9c02104, 0x23661302, 0xe8bd4618, 0x250081f0, 0x0f91ebb5, 0x060ceb09,
    0x0504f04f, 0xd0396075, 0x0e91ea4f, 0x240c2100, 0x19161905, 0x5c0cf855, 0x6c0cf856, 0xd12642b5,
    0x45751c4d, 0xeb00d22a, 0xeb020581, 0xf8d50681, 0x68778004, 0xd11345b8, 0x45771c8f, 0x68add21e,
    0x42b568b6, 0x1ccdd10f, 0xd2174575, 0x59175906, 0xd10b42be, 0x45713104, 0x0410f104, 0xe00dd3d8,
    0x0101f041, 0xf041e003, 0xe0000102, 0xeb004629, 0xeb090381, 0x2106000c, 0x1302e9c0, 0xe8bd4618,
    0x000081f0, 0x1030f240, 0x00fff2c0, 0x31016801, 0x6800bf1c, 0xf6404770, 0xf2cf71e0, 0x78080100,
    0xf3616849, 0x4770200b, 0x2020f240, 0x00fff2c0, 0x31016801, 0x6800bf14, 0x5080f44f, 0xbf004770,
    0x2024f240, 0x00fff2c0, 0x31016801, 0x6800bf14, 0x7000f44f, 0xbf004770, 0x47702000, 0x47702000,
    0x2120f240, 0x01fff2c0, 0x30016808, 0x6808bf14, 0x5080f44f, 0x3201684a, 0x6849bf14, 0x7100f44f,
    0xf000fb01, 0xbf004770, 0x42814401, 0x2001bf9c, 0xbf004770, 0x32016802, 0x2000bf1c, 0x30044770,
    0xbf244288, 0x47702001, 0x32016802, 0x2000bf1c, 0x30044770, 0xbf244288, 0x47702001, 0x32016802,
    0x2000bf1c, 0x30044770, 0xbf244288, 0x47702001, 0x32016802, 0x2000bf1c, 0x30044770, 0xbf244288,
    0x47702001, 0xbf00e7d6, 0xbf004770, 0x47702000, 0x47702003, 0xbf842803, 0x47702069, 0xa10cb240,
    0x1020f851, 0x4000f249, 0x0003f2c5, 0x1104f8c0, 0xbf00e005, 0x29006801, 0x2000bf1c, 0x68014770,
    0x6801b921, 0x6801b911, 0xd0f32900, 0x47702000, 0x00000000, 0x00000002, 0x00000001, 0x00000000,
    0x4000f249, 0x0003f2c5, 0xb9416801, 0xb9316801, 0x29006801, 0x4770bf18, 0x29006801, 0x4770d0f4,
    0x4000f249, 0x0003f2c5, 0xf8c02101, 0xbf00110c, 0xb9416801, 0xb9316801, 0x29006801, 0x4770bf18,
    0x29006801, 0x4770d0f4, 0x9000b081, 0x4100f249, 0xf2c59800, 0xf04f0103, 0x600232ff, 0xb9306808,
    0xb9206808, 0xb9106808, 0x28006808, 0xb001d0f6, 0xbf004770, 0x47702069, 0xb081b580, 0x2e20f240,
    0x0efff2c0, 0x0000f8de, 0xbf143001, 0x1000f8de, 0x5180f44f, 0x0004f8de, 0xbf143001, 0x2004f8de,
    0x7200f44f, 0xf101fb02, 0xf249b1f1, 0x22004300, 0x0303f2c5, 0x3cfff04f, 0x98009200, 0xc000f8c0,
    0xb9306818, 0xb9206818, 0xb9106818, 0x28006818, 0xf8ded0f6, 0x30010000, 0xf8debf14, 0xf44f0000,
    0x44025080, 0xd3e7428a, 0xb0012000, 0x0000bd80, 0x00000000, 0x00000000, 0x00000000, 0x00000000,
    0x00000000
    ],

    # Relative function addresses
    'pc_init': 0x20000005,
    'pc_unInit': 0x20000039,
    'pc_program_page': 0x20000291,
    'pc_erase_sector': 0x200000ad,
    'pc_eraseAll': 0x20000089,

    'static_base' : 0x20000000 + 0x00000004 + 0x00000690,
    'begin_stack' : 0x200036b0,
    'begin_data' : 0x20000000 + 0x1000,
    'page_size' : 0x1000,
    'analyzer_supported' : False,
    'analyzer_address' : 0x00000000,
    # Enable double buffering
    'page_buffers' : [
        0x200006b0,
        0x200016b0
    ],
    'min_program_length' : 0x1000,

    # Relative region addresses and sizes
    'ro_start': 0x4,
    'ro_size': 0x690,
    'rw_start': 0x694,
    'rw_size': 0x4,
    'zi_start': 0x698,
    'zi_size': 0x10,

    # Flash information
    'flash_start': 0xff8000,
    'flash_size': 0x1000,
    'sector_sizes': (
        (0x0, 0x1000),
    )
}


FLASH_ALGO_NET_UICR = {
    'load_address' : 0x21000000,

    # Flash algorithm as a hex string
    'instructions': [
    0xe7fdbe00,
    0xf240b570, 0xf2c00604, 0x25000600, 0x0006eb09, 0x5006f849, 0x5501e9c0, 0xb2d060c5, 0xf0004614,
    0x2800f9e5, 0xeb09bf1e, 0xe9c10106, 0x46050402, 0xbd704628, 0x4604b510, 0xf0002000, 0xf240f9d7,
    0xf2c00104, 0x44490100, 0xe9c1b110, 0xe0030402, 0x29006889, 0xbd10bf08, 0x0100f244, 0x1100f2c2,
    0x600a2201, 0x0204f240, 0x0200f2c0, 0x3002f859, 0x604b444a, 0x608b6853, 0x60cb6893, 0x610a68d2,
    0xbf00bd10, 0xf240b580, 0xf2c00004, 0x21010000, 0x1000f849, 0x21004448, 0x1101e9c0, 0xf00060c1,
    0x2000f9c7, 0xbf00bd80, 0xf240b510, 0xf2c00004, 0x21020000, 0x1000f849, 0x24004448, 0x4401e9c0,
    0xf00060c4, 0x4601f953, 0x0000f248, 0x10fff2c0, 0xf00022ff, 0xb130f80b, 0xf9baf000, 0x28694604,
    0x2c00bf14, 0x46202400, 0xbf00bd10, 0xf240b570, 0xf2c00c04, 0x23050c00, 0x300cf849, 0x030ceb09,
    0x0e00f04f, 0xe9c30784, 0xf8c3ee01, 0xd005e00c, 0x010ceb09, 0xe9c12203, 0xe00c2002, 0x030ceb09,
    0x0e01f04f, 0xf8c3078c, 0xd008e004, 0x000ceb09, 0xe9c02203, 0xf04f2102, 0x46700e65, 0xf648bd70,
    0xf2c07eff, 0xeb091eff, 0x2402030c, 0x605c4570, 0xeb09d905, 0x2204010c, 0x2002e9c1, 0x180be00d,
    0x0501f10e, 0x040ceb09, 0x42ab2603, 0xd9086066, 0x000ceb09, 0xe9c02104, 0xf04f1302, 0x46700e66,
    0xb151bd70, 0xf04f2300, 0xbf000e00, 0x42965cc6, 0x3301d107, 0xd3f9428b, 0xf04fe00b, 0x46700e00,
    0x4418bd70, 0x010ceb09, 0xf04f2205, 0xe9c10e01, 0x46702002, 0xbf00bd70, 0x41f0e92d, 0x0604f240,
    0x0600f2c0, 0x46044615, 0xeb092003, 0x23000206, 0xf849078f, 0xe9c20006, 0x60d33301, 0xeb09d006,
    0xe9c20206, 0x20650102, 0x81f0e8bd, 0x70fff648, 0x10fff2c0, 0x0206eb09, 0x42842302, 0xd9076053,
    0x0006eb09, 0xe9c02104, 0x20661402, 0x81f0e8bd, 0x3001190a, 0x0306eb09, 0x42822703, 0xd907605f,
    0x0006eb09, 0xe9c02104, 0x20661202, 0x81f0e8bd, 0xebb02000, 0xd01b0f91, 0x0891ea4f, 0xe00c2700,
    0x0027f855, 0x0027f844, 0xf8eaf000, 0x45473701, 0x0000f04f, 0xe8bdbf28, 0xf85481f0, 0x30010027,
    0xeb09d0ee, 0x21050006, 0xe9c019e2, 0x20681202, 0x81f0e8bd, 0xf240b570, 0xf2c00c04, 0x23040c00,
    0x300cf849, 0x030ceb09, 0x0e00f04f, 0xe9c30784, 0xf8c3ee01, 0xd005e00c, 0x010ceb09, 0xe9c12203,
    0xe00c2002, 0x030ceb09, 0x0e01f04f, 0xf8c3078c, 0xd007e004, 0x000ceb09, 0xe9c02203, 0x23652102,
    0xbd704618, 0x7efff648, 0x1efff2c0, 0x030ceb09, 0x45702402, 0xd905605c, 0x010ceb09, 0xe9c12204,
    0xe00d2002, 0xf10e180b, 0xeb090501, 0x2603040c, 0x606642ab, 0xeb09d907, 0x2104000c, 0x1302e9c0,
    0x46182366, 0x2500bd70, 0x0f91ebb5, 0x060ceb09, 0x0504f04f, 0xd0146075, 0x0e91ea4f, 0xbf002100,
    0xf8526804, 0x42ac5021, 0x3101d105, 0xf1004571, 0xd3f50004, 0xeb09e005, 0x2206010c, 0xe9c14603,
    0x46182002, 0x0000bd70, 0x1030f240, 0x10fff2c0, 0x31016801, 0x6800bf1c, 0xf6404770, 0xf2cf71e0,
    0x78080100, 0xf3616849, 0x4770200b, 0x2020f240, 0x10fff2c0, 0x31016801, 0x6800bf14, 0x6000f44f,
    0xbf004770, 0x2024f240, 0x10fff2c0, 0x31016801, 0x6800bf14, 0x47702080, 0x47702000, 0x7080f04f,
    0xbf004770, 0xf7ffb510, 0x4604ffe1, 0xffeaf7ff, 0xf004fb00, 0x7080f100, 0xbf00bd10, 0x42814401,
    0x2001bf9c, 0xe0034770, 0xbf244288, 0x47702001, 0x2b04f850, 0xbf1c3201, 0x47702000, 0xbf00e7f4,
    0xbf004770, 0x47702000, 0x47702003, 0xbf842803, 0x47702069, 0xb240b580, 0xf851a105, 0xf2400020,
    0xf2c45104, 0x60081108, 0xf80af000, 0xbd802000, 0x00000000, 0x00000002, 0x00000001, 0x00000000,
    0x4000f240, 0x1008f2c4, 0x29006801, 0x4770d0fc, 0x500cf240, 0x1008f2c4, 0x60012101, 0xbf00e7f0,
    0x9000b081, 0xf04f9800, 0x600131ff, 0xe7e7b001, 0x47702069, 0xf7ffb5b0, 0x4604ffa5, 0x7f80f1b0,
    0xf04fd90a, 0xbf007580, 0xf7ff4628, 0xf7ffffe9, 0x4405ff7d, 0xd3f742a5, 0xbdb02000, 0x00000000,
    0x00000000, 0x00000000, 0x00000000, 0x00000000
    ],

    # Relative function addresses
    'pc_init': 0x21000005,
    'pc_unInit': 0x21000039,
    'pc_program_page': 0x210001bd,
    'pc_erase_sector': 0x210000ad,
    'pc_eraseAll': 0x21000089,

    'static_base' : 0x21000000 + 0x00000004 + 0x0000047c,
    'begin_stack' : 0x210024a0,
    'begin_data' : 0x21000000 + 0x1000,
    'page_size' : 0x800,
    'analyzer_supported' : False,
    'analyzer_address' : 0x00000000,
    # Enable double buffering
    'page_buffers' : [
        0x210004a0,
        0x21000ca0
    ],
    'min_program_length' : 0x800,

    # Relative region addresses and sizes
    'ro_start': 0x4,
    'ro_size': 0x47c,
    'rw_start': 0x480,
    'rw_size': 0x4,
    'zi_start': 0x484,
    'zi_size': 0x10,

    # Flash information
    'flash_start': 0x1ff8000,
    'flash_size': 0x1000,
    'sector_sizes': (
        (0x1000000, 0x800),
    )
}


class NRF53XX(NRF53):
    MEMORY_MAP = MemoryMap(
        FlashRegion(
            start=0x0,
            length=0x200000,
            blocksize=0x1000,
            algo=FLASH_ALGO_APP,
            flash_class=Flash_NRF5340,
            core_index=0,
        ),
        FlashRegion(
            start=0x01000000,
            length=0x00040000,
            blocksize=0x800,
            algo=FLASH_ALGO_NET,
            flash_class=Flash_NRF5340,
            core_index=1,
        ),
        FlashRegion(
            start=0x00ff8000,
            length=0x1000,
            blocksize=0x1000,
            is_erasable=False,
            algo=FLASH_ALGO_APP_UICR,
            flash_class=Flash_NRF5340,
            core_index=0,
        ),
        FlashRegion(
            start=0x01ff8000,
            length=0x800,
            blocksize=0x800,
            is_erasable=False,
            algo=FLASH_ALGO_NET,
            flash_class=Flash_NRF5340,
            core_index=1,
        ),
        RamRegion(start=0x20000000, length=0x80000),
    )

    def __init__(self, session):
        super(NRF53XX, self).__init__(session, self.MEMORY_MAP)
        self._svd_location = SVDFile.from_builtin("nrf5340_application.svd") # TODO
