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

"""Module providing support for the Colorlight yosys nxtpnr flow"""


from __future__ import absolute_import

from .makefilesyn import MakefileSyn
from ..sourcefiles.srcfile import VerilogFile, LPFFile


class ToolEcp5Yosys(MakefileSyn):

    """Class providing the interface for Colorlight synthesis"""

    TOOL_INFO = {
        'name': 'Colorlight',
        'id': 'Colorlight',
        'windows_bin': None,
        'linux_bin': 'yosys -c',
        'project_ext': ''}

    STANDARD_LIBS = []

    SUPPORTED_FILES = {LPFFile: None}

    HDL_FILES = {VerilogFile: 'read_verilog $(sourcefile)'}

    CLEAN_TARGETS = {'clean': ["$(PROJECT).asc", "$(PROJECT).json", "$(PROJECT).svf", "$(PROJECT)_out.config"],
                     'mrproper': ["$(PROJECT).bit"]}

    TCL_CONTROLS = {
        'synthesize': 'yosys -import\n' +
                      'source files.tcl\n' +
                      'synth_ecp5 -top $(TOP_MODULE) -json $(PROJECT).json',
        'par': 'catch {exec nextpnr-ecp5' +
               ' --$(SYN_DEVICE)' +
               ' --speed $(SYN_GRADE)' +
               ' --package $(SYN_PACKAGE)' +
               ' --lpf $(SOURCES_LPFFile)' +
               ' --textcfg $(PROJECT)_out.config' +
               ' --json $(PROJECT).json}',
        'bitstream': 'catch {exec ecppack --svf $(PROJECT).svf $(PROJECT)_out.config $(PROJECT).bit}',
        'install_source': 'catch {exec openFPGALoader -c $(JTAG_POD) $(PROJECT).bit}'}

    def __init__(self):
        super(ToolEcp5Yosys, self).__init__()
        self._tcl_controls.update(ToolEcp5Yosys.TCL_CONTROLS)

    def _makefile_syn_top(self):
        self.manifest_dict["syn_family"] = 'ecp5'
        super(ToolEcp5Yosys, self)._makefile_syn_top()

