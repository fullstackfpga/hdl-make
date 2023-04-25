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

"""Module providing support for SBY Formal Verification"""

from __future__ import absolute_import
import string

from .makefilesim import MakefileSim
from ..sourcefiles.srcfile import VerilogFile, SVFile


class ToolFormalSby(MakefileSim):

    """Class providing the interface for SymbiYosys Formal Verification"""

    TOOL_INFO = {
        'name': 'SymbiYosys',
        'id': 'sby',
        'windows_bin': None,
        'linux_bin': 'sby'}

    HDL_FILES = {VerilogFile: '', SVFile: ''}

    CLEAN_TARGETS = {'clean': ["*.sby", "$(TOP_MODULE)_prf", "$(TOP_MODULE)_cvr"],
                     'mrproper': ["*.vcd", "*.vvp"]}

    SIMULATOR_CONTROLS = {'vlog': 'echo $< >> $(TOP_MODULE).sby',
                          'sim_prf': 'sby $(SBY_OPT) $(TOP_MODULE).sby prf',
                          'sim_cvr': 'sby $(SBY_OPT) $(TOP_MODULE).sby cvr'}

    def __init__(self):
        super(ToolFormalSby, self).__init__()

    def _makefile_sim_top(self):
        """Generic method to write the simulation Makefile top section"""
        super(ToolFormalSby, self)._makefile_sim_top()

    def _makefile_sim_dep_files(self):
        """Print dummy targets to handle file dependencies"""
        for file_aux in self.fileset.sort():
            # Consider only HDL files.
            if isinstance(file_aux, tuple(self.HDL_FILES)):
                self.writeln("verilog_obj: $(VERILOG_SRC)")
                if isinstance(file_aux, VerilogFile):
                    command_key = 'vlog'
                self.writeln("\t\t" + self.SIMULATOR_CONTROLS[command_key].format(work=file_aux.library))
                #self._makefile_touch_stamp_file()
                self.writeln()

    def _makefile_sim_compilation(self):
        """Generate compile simulation Makefile target for SBY"""
        self.writeln("$(TOP_MODULE): $(TOP_MODULE)_prf/PASS $(TOP_MODULE)_cvr/PASS")
        self.writeln()
        self.writeln("$(TOP_MODULE)_prf/PASS: $(TOP_MODULE).sby verilog_obj")
        self.writeln("\t\t" + self.SIMULATOR_CONTROLS['sim_prf'])
        self.writeln()
        self.writeln("$(TOP_MODULE)_cvr/PASS: $(TOP_MODULE).sby verilog_obj")
        self.writeln("\t\t" + self.SIMULATOR_CONTROLS['sim_cvr'])
        self.writeln()
        self._makefile_sim_dep_files()

    def _makefile_sim_phony(self):
        """Print simulation PHONY target list to the Makefile"""
        self.writeln(
            ".PHONY: all")
        self.writeln(
            "all: $(TOP_MODULE)")

    def _makefile_sim_local(self):
        """Generic method to write the simulation Makefile local target"""
        pass

    def _makefile_sim_sources_lang(self, name, klass):
        """Generic method to write the simulation Makefile HDL sources"""
        fileset = self.fileset
        for vlog in fileset.filter(klass).sort():
            self.writeln("{}_SRC += ".format(name) + vlog.rel_path())
        self.writeln()

    def _makefile_sim_command(self):
        """Generic method to write the simulation Makefile user commands"""
        sim_command = """
$(TOP_MODULE).sby: 
\t\t@echo "[tasks]" >> $(TOP_MODULE).sby
\t\t@echo "prf" >> $(TOP_MODULE).sby
\t\t@echo "cvr" >> $(TOP_MODULE).sby
\t\t@echo "" >> $(TOP_MODULE).sby
\t\t@echo "[options]" >> $(TOP_MODULE).sby
\t\t@echo "prf: mode prove" >> $(TOP_MODULE).sby
\t\t@echo "prf: depth 98" >> $(TOP_MODULE).sby
\t\t@echo "cvr: mode cover" >> $(TOP_MODULE).sby
\t\t@echo "cvr: depth 240" >> $(TOP_MODULE).sby
\t\t@echo "" >> $(TOP_MODULE).sby
\t\t@echo "multiclock on" >> $(TOP_MODULE).sby
\t\t@echo "" >> $(TOP_MODULE).sby
\t\t@echo "[engines]" >> $(TOP_MODULE).sby
\t\t@echo "smtbmc" >> $(TOP_MODULE).sby
\t\t@echo "" >> $(TOP_MODULE).sby
\t\t@echo "[script]" >> $(TOP_MODULE).sby
\t\t@echo "read -formal $(TOP_MODULE).v" >> $(TOP_MODULE).sby
\t\t@echo "prep -top $(TOP_MODULE)" >> $(TOP_MODULE).sby
\t\t@echo "" >> $(TOP_MODULE).sby
\t\t@echo "[files]" >> $(TOP_MODULE).sby
"""
        self.writeln(sim_command)

