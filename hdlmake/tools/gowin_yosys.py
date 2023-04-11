#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2023 Fullstackfpga
# Author: Henry Feng (fullstackfpga@gmail.com)
#
# Hdlmake is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hdlmake is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hdlmake.  If not, see <http://www.gnu.org/licenses/>.
#

"""Module providing support for the Gowin yosys nxtpnr flow"""

from __future__ import absolute_import

from .makefilesyn import MakefileSyn
from ..sourcefiles.srcfile import VerilogFile, CSTFile


class ToolGowinYosys(MakefileSyn):

    """Class providing the interface for Gowin synthesis"""

    TOOL_INFO = {
        'name': 'Gowin',
        'id': 'Gowin',
        'windows_bin': None,
        'linux_bin': 'yosys -c ',
        'project_ext': ''}

    STANDARD_LIBS = []

    SUPPORTED_FILES = {CSTFile: None}

    HDL_FILES = {VerilogFile: 'read_verilog $(sourcefile)'}

    CLEAN_TARGETS = {'clean': ["$(PROJECT).fs", "$(PROJECT).json", "$(PROJECT).pack"],
                     'mrproper': ["$(PROJECT).bit"]}

    TCL_CONTROLS = {
        'synthesize': 'yosys -import\n' +
                      'source files.tcl\n' +
                      'synth_gowin -top $(TOP_MODULE) -json $(PROJECT).json',
        'par': 'catch {exec nextpnr-gowin' +
               ' --device $(SYN_FAMILY)$(SYN_FAMILY_SURFIX)-$(SYN_DEVICE_PREFIX)$(SYN_DEVICE)$(SYN_PACKAGE)$(SYN_GRADE)' +
               ' --cst $(SOURCES_CSTFile)' +
               ' --write $(PROJECT).pack' +
               ' --json $(PROJECT).json}',
        'bitstream': 'catch {exec gowin_pack -d $(SYN_FAMILY)-$(SYN_DEVICE) -o $(PROJECT).fs $(PROJECT).pack}',
        'install_source': 'catch {exec openFPGALoader -c $(JTAG_POD) $(PROJECT).fs}'}

    def __init__(self):
        super(ToolGowinYosys, self).__init__()
        self._tcl_controls.update(ToolGowinYosys.TCL_CONTROLS)

    def _makefile_syn_top(self):
        super(ToolGowinYosys, self)._makefile_syn_top()

