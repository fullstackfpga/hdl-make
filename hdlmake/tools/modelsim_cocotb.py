#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 - 2015 CERN
# Author: Pawel Szostek (pawel.szostek@cern.ch)
# Multi-tool support by Javier D. Garcia-Lasheras (javier@garcialasheras.com)
#
# This file is part of Hdlmake.
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

"""Module providing support for Mentor Modelsim simulation"""

from __future__ import print_function
from __future__ import absolute_import
import os

from .makefilevsim import MakefileVsim
from ..sourcefiles.srcfile import VerilogFile, VHDLFile, SVFile


class ToolModelsimCocotb(MakefileVsim):

    """Class providing the interface for Mentor Modelsim simulator"""

    TOOL_INFO = {'name': 'Modelsim',
                 'id': 'modelsim',
                 'windows_bin': 'vsim.exe',
                 'linux_bin': 'vsim'}

    STANDARD_LIBS = ['ieee', 'std', 'altera_mf']

    CLEAN_TARGETS = {'clean': ["modelsim.ini", "transcript"],
                     'mrproper': ["*.vcd", "*.fst", "*.wlf", "work"]}

    def __init__(self):
        super(ToolModelsimCocotb, self).__init__()
        #self.copy_rules["modelsim.ini"] = os.path.join(
        #    "$(MODELSIM_INI_PATH)", "modelsim.ini")
        #self.additional_deps.append("modelsim.ini")

    def _makefile_sim_top(self):
        """Generic method to write the simulation Makefile top section"""
        super(ToolModelsimCocotb, self)._makefile_sim_top()
        top_level = """\
SIM   ?= modelsim
WAVES ?= 0

TOPLEVEL_LANG ?=verilog

COCOTB_HDL_TIMEUNIT      = 1ns
COCOTB_HDL_TIMEPRECISION = 1ps

TOPLEVEL = {top_module}
MODULE   = test_{top_module}

PWD=$(shell pwd)

export PYTHONPATH := $(PWD)/../model:$(PYTHONPATH)

ifeq ($(TOPLEVEL_LANG),verilog)
    VERILOG_SOURCES = $(PWD)/../top/{top_module}.v
else ifeq ($(TOPLEVEL_LANG),vhdl)
    VHDL_SOURCES = $(PWD)/../top/{top_module}.vhdl
else
    $(error A valid value (verilog or vhdl) was not provided for TOPLEVEL_LANG=$(TOPLEVEL_LANG))
endif

"""
        self.writeln(top_level.format(
            top_module=self.manifest_dict["sim_top"]))

    def _makefile_sim_options(self):
        """Print the Modelsim options to the Makefile"""
        #modelsim_ini_path = self.manifest_dict.get("modelsim_ini_path")
        #if modelsim_ini_path == None:
        #    if self.manifest_dict['sim_path']:
        #        modelsim_ini_path = os.path.join(
        #            self.manifest_dict["sim_path"], "..")
        #    else:
        #        modelsim_ini_path = os.path.join(
        #            "$(HDLMAKE_MODELSIM_PATH)", "..")
        #self.custom_variables["MODELSIM_INI_PATH"] = modelsim_ini_path
        #modelsim_ini = "-modelsimini modelsim.ini "
        #vcom_opt = self.manifest_dict.get("vcom_opt", '')
        #self.manifest_dict["vcom_opt"] = modelsim_ini + vcom_opt
        #vlog_opt = self.manifest_dict.get("vlog_opt", '')
        #self.manifest_dict["vlog_opt"] = modelsim_ini + vlog_opt
        #vmap_opt = self.manifest_dict.get("vmap_opt", '')
        #self.manifest_dict["vmap_opt"] = modelsim_ini + vmap_opt
        self.writeln("include $(shell cocotb-config --makefiles)/Makefile.sim\n\n")
        #super(ToolModelsimCocotb, self)._makefile_sim_options()

    def _makefile_sim_local(self):
        """Generic method to write the simulation Makefile local target"""
        pass

    def _cocotb_makefile_sim_sources_lang(self, name, klass):
        """Generic method to write the simulation Makefile HDL sources"""
        fileset = self.fileset
        for vlog in fileset.filter(klass).sort():
            self.writeln("{}_SOURCES += ".format(name) + vlog.rel_path())
        self.writeln()

    def _makefile_sim_sources(self):
        """Generic method to write the simulation Makefile HDL sources"""
        self._cocotb_makefile_sim_sources_lang("VERILOG", VerilogFile)
        self._cocotb_makefile_sim_sources_lang("VHDL", VHDLFile)

    def _makefile_sim_compilation(self):
        """Write a properly formatted Makefile for the simulator.
        The Makefile format is shared, but flags, dependencies, clean rules,
        etc are defined by the specific tool.
        """
        pass

    def _makefile_sim_command(self):
        """Generic method to write the simulation Makefile user commands"""
        pass

    def _makefile_sim_clean(self):
        """Generic method to write the simulation Makefile user clean target"""
        pass

    def _makefile_sim_phony(self):
        """Print simulation PHONY target list to the Makefile"""
        pass


