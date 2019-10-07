#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 - 2015 CERN
# Author: Pawel Szostek (pawel.szostek@cern.ch)
# Multi-tool support by Javier D. Garcia-Lasheras (javier@garcialasheras.com)
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

"""Module providing support for Aldec Active-HDL simulator"""

from __future__ import absolute_import
from .makefilesim import MakefileSim
from ..sourcefiles.srcfile import VHDLFile, VerilogFile, SVFile


class ToolActiveHDL(MakefileSim):

    """Class providing the interface to control an Active-HDL simulation"""

    TOOL_INFO = {
        'name': 'Aldec Active-HDL',
        'id': 'active_hdl',
        'windows_bin': 'vsimsa.exe',
        'linux_bin': None}

    STANDARD_LIBS = ['ieee', 'std']

    HDL_FILES = {VHDLFile: None, VerilogFile: None, SVFile: None}

    CLEAN_TARGETS = {'clean': ["run.command", "library.cfg", "work"],
                     'mrproper': ["*.vcd", "*.asdb"]}

    def __init__(self):
        super(ToolActiveHDL, self).__init__()

    def _makefile_sim_compilation(self):
        """Print Makefile compilation target for Aldec Active-HDL simulator"""
        fileset = self.fileset
        self.writeln("simulation:")
        self.writeln("\t\techo # Active-HDL command file,"
                     " generated by HDLMake > run.command")
        self.writeln()
        self.writeln("\t\techo # Create library and set as"
                     " default target >> run.command")
        self.writeln("\t\techo alib work >> run.command")
        self.writeln("\t\techo set worklib work >> run.command")
        self.writeln()
        self.writeln(
            "\t\techo # Compiling HDL source files >> run.command")
        for vl_file in fileset.filter(VerilogFile):
            self.writeln(
                "\t\techo alog \"" +
                vl_file.rel_path(
                ) +
                "\" >> run.command")
        for sv_file in fileset.filter(SVFile):
            self.writeln(
                "\t\techo alog \"" +
                sv_file.rel_path(
                ) +
                "\" >> run.command")
        for vhdl_file in fileset.filter(VHDLFile):
            self.writeln(
                "\t\techo acom \"" +
                vhdl_file.rel_path(
                ) +
                "\" >> run.command")
        self.writeln()
        self.writeln("\t\tvsimsa -do run.command")
