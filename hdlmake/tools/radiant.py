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

"""Module providing support for Lattice Radiant IDE"""


from __future__ import absolute_import
from .makefilesyn import MakefileSyn
from ..sourcefiles.srcfile import EDFFile, LPFFile, VHDLFile, VerilogFile, SDCFile, LDCFile, PDCFile, IPXFile


class ToolRadiant(MakefileSyn):

    """Class providing the interface for Lattice Radiant synthesis"""

    TOOL_INFO = {
        'name': 'radiant',
        'id': 'radiant',
        'windows_bin': 'radiantc.exe',
        'linux_bin': 'radiantc ',
        'project_ext': 'rdf'}

    STANDARD_LIBS = ['ieee', 'std']

    _LATTICE_SOURCE = 'prj_add_source {0} $(sourcefile)'

    SUPPORTED_FILES = {
        EDFFile: _LATTICE_SOURCE.format('add'),
        PDCFile: _LATTICE_SOURCE.format('add'),
        LDCFile: _LATTICE_SOURCE.format('add'),
        SDCFile: _LATTICE_SOURCE.format('add'),
        IPXFile: _LATTICE_SOURCE.format('add'),
        LPFFile: _LATTICE_SOURCE.format('add')}

    HDL_FILES = {
        VHDLFile: _LATTICE_SOURCE.format('add'),
        VerilogFile: _LATTICE_SOURCE.format('add')}

    CLEAN_TARGETS = {'clean': ["*.sty", "impl", "*.rdf"],
                     'mrproper': ["*.jed"]}

    TCL_CONTROLS = {'create': 'prj_create -name $(PROJECT)'
                              ' -impl impl'
                              ' -dev {0} -synthesis \"synplify\"',
                    'open': 'prj_open $(PROJECT).rdf',
                    'save': 'prj_save',
                    'close': 'prj_close',
                    'project': '$(TCL_CREATE)\n'
                               'source files.tcl\n'
                               '$(TCL_SAVE)\n'
                               '$(TCL_CLOSE)',
                    'synthesize': '$(TCL_OPEN)\n'
                           'prj_set_impl_opt -impl impl top $(TOP_MODULE)\n'
                           'prj_run_synthesis\n'
                           '$(TCL_SAVE)\n'
                           '$(TCL_CLOSE)',
                    'map': '$(TCL_OPEN)\n'
                           'prj_run_map\n'
                           '$(TCL_SAVE)\n'
                           '$(TCL_CLOSE)',
                    'par': '$(TCL_OPEN)\n'
                           'prj_run_par\n'
                           '$(TCL_SAVE)\n'
                           '$(TCL_CLOSE)',
                    'bitstream': '$(TCL_OPEN)\n'
                                 'prj_run Export'
                                 ' -impl impl -task Bitgen\n'
                                 '$(TCL_SAVE)\n'
                                 '$(TCL_CLOSE)',
                    'install_source': '$(PROJECT)/$(PROJECT)_$(PROJECT).jed'}

    def __init__(self):
        super(ToolRadiant, self).__init__()
        self._tcl_controls.update(ToolRadiant.TCL_CONTROLS)

    def _makefile_syn_tcl(self):
        """Create a Diamond synthesis project by TCL"""
        #synth_tool = self.manifest_dict["syn_tool"]
        #if synth_tool == "radiant_lse":
        #    tool = "lse"
        #else:
        #    tool = "synplify"
        syn_family = self.manifest_dict["syn_family"]
        syn_device = self.manifest_dict["syn_device"]
        syn_grade = self.manifest_dict["syn_grade"]
        syn_package = self.manifest_dict["syn_package"]
        create_tmp = self._tcl_controls["create"]
        target = syn_family + "-" + syn_device + "-" + syn_grade + syn_package
        self._tcl_controls["create"] = create_tmp.format(target.upper())
        super(ToolRadiant, self)._makefile_syn_tcl()
