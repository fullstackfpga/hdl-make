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

"""Module providing support for Xilinx Vivado simulation"""


from __future__ import absolute_import
from .makefilesim import MakefileSim
from ..sourcefiles.srcfile import VerilogFile, VHDLFile, SVFile

class ToolVivadoSimUVM(MakefileSim):

    """Class providing the interface for Xilinx Vivado synthesis"""

    TOOL_INFO = {
        'name': 'vivado-sim',
        'id': 'vivado-sim',
        'windows_bin': 'vivado -mode tcl -source',
        'linux_bin': 'vivado -mode tcl -source',
    }

    STANDARD_LIBS = ['ieee', 'std']

    HDL_FILES = {VerilogFile: '', VHDLFile: '', SVFile: ''}

    CLEAN_TARGETS = {'clean': [".Xil", "*.jou", "*.log", "*.pb",
                               "work", "xsim.dir"],
                     'mrproper': ["*.wdb", "*.vcd"]}

    SIMULATOR_CONTROLS = {'vlog': 'xvlog $<',
                          'vhdl': 'xvhdl $<',
                          'compiler': 'xelab -debug all $(TOP_MODULE) '
                                      '-s $(TOP_MODULE)'}

    def __init__(self):
        super(ToolVivadoSimUVM, self).__init__()

    def _makefile_sim_compilation(self):
        """Generate compile simulation Makefile target for Vivado Simulator"""
        self.writeln("simulation: $(VERILOG_OBJ) $(VHDL_OBJ)")
        self.writeln("\t\t" + self.SIMULATOR_CONTROLS['compiler'])
        self.writeln()
        self._makefile_sim_dep_files()
