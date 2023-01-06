#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 - 2017 CERN
# Author: Javier D. Garcia Lasheras (jgarcia@gl-research.com)
#
# This file is part of Hdlmake.
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
# Copyright (c) 2023 Fullstackfpga
# Author: Henry Feng (fullstackfpga@gmail.com)

"""Module providing support for the Colorlight yosys nxtpnr flow"""


from __future__ import absolute_import

from .makefilesyn import MakefileSyn
from ..sourcefiles.srcfile import VerilogFile, LPFFile


class ToolColorlight(MakefileSyn):

    """Class providing the interface for Colorlight synthesis"""

    TOOL_INFO = {
        'name': 'Colorlight',
        'id': 'Colorlight',
        'windows_bin': None,
        'linux_bin': 'yosys -p',
        'project_ext': ''}

    STANDARD_LIBS = []

    SUPPORTED_FILES = {LPFFile: None}

    HDL_FILES = {VerilogFile: 'read_verilog $(sourcefile)'}

    CLEAN_TARGETS = {'clean': ["$(PROJECT).asc", "$(PROJECT).json"],
                     'mrproper': ["$(PROJECT).bin"]}

    TCL_CONTROLS = {
        'synthesize': 'yosys -import\n' +
                      'source files.tcl\n' +
                      'synth_ecp5 -top $(TOP_MODULE) -json $(PROJECT).json',
        'par': 'catch {exec nextpnr-ecp5' +
               ' --$(SYN_DEVICE)' +
               ' --package $(SYN_PACKAGE)' +
               ' --lpf $(SOURCES_LPFFile)' +
               ' $(PROJECT).json}',
        'ecppack': 'catch {exec ecppack --svf $(PROJECT).svf $(PROJECT).bin}',
        'bitstream': 'catch {exec openFPGALoader -c $(JTAG_POD) $(PROJECT).bit}',
        'install_source': ''}

    def __init__(self):
        super(ToolColorlight, self).__init__()
        self._tcl_controls.update(ToolColorlight.TCL_CONTROLS)

    def _makefile_syn_top(self):
        self.manifest_dict["syn_family"] = 'ecp5'
        super(ToolColorlight, self)._makefile_syn_top()

