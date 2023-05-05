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

"""Module providing generic support for Xilinx synthesis tools"""


from __future__ import absolute_import
from .makefilesyn import MakefileSyn
from ..sourcefiles.srcfile import VHDLFile, VerilogFile, SVFile, TCLFile, XCIFile
import os
import logging
from ..util import shell


class ToolXilinx(MakefileSyn):

    """Class providing the interface for Xilinx Vivado synthesis"""

    _XILINX_SOURCE = (
        "add_files -norecurse $(sourcefile); "
        "set_property IS_GLOBAL_INCLUDE 1 [get_files $(sourcefile)]")

    _XILINX_CORE = (
        "IP_CORES += [get_files $(sourcefile)]")

    HDL_FILES = {
        VHDLFile: _XILINX_SOURCE,
        VerilogFile: _XILINX_SOURCE,
        SVFile: _XILINX_SOURCE}

    SUPPORTED_FILES = {TCLFile: 'source $(sourcefile)'}

    CORE_FILES = { XCIFile: _XILINX_CORE}

    CLEAN_TARGETS = {'mrproper': ["*.bit", "*.bin"]}

    _XILINX_RUN = '''\
$(TCL_OPEN)
{1}
reset_run {0}
launch_runs {0}
wait_on_run {0}
set result [get_property STATUS [get_runs {0}]]
set keyword [lindex [split '$$'result " "] end]
if {{ '$$'keyword != \\"Complete!\\" }} {{
    exit 1
}}
$(TCL_CLOSE)'''

    TCL_CONTROLS = {'create': 'create_project $(PROJECT) ./',
                    'open': 'open_project $(PROJECT_FILE)',
                    'close': 'exit',
                    'project': '$(TCL_CREATE)\n'
                               '{0}\n'
                               'source files.tcl\n'
                               'set_property include_dirs {{$(INCLUDE_DIRS)}} [current_fileset]\n'
                               'update_compile_order -fileset sources_1\n'
                               'report_ip_status\n'
                               'upgrade_ip [get_ips {{$(IP_CORES)}}] -log ip_upgrade.log\n'
                               'export_ip_user_files -of_objects [get_ips {{$(IP_CORES)}}] -no_script -sync -force -quiet\n'
                               'update_compile_order -fileset sources_1\n'
                               'update_compile_order -fileset sim_1\n'
                               '$(TCL_CLOSE)',
                    'synthesize': _XILINX_RUN,
                    'par': _XILINX_RUN,
                    'install_source': '$(PROJECT).runs/impl_1/$(SYN_TOP).bit'}

    def __init__(self):
        super(ToolXilinx, self).__init__()
        self._tcl_controls.update(ToolXilinx.TCL_CONTROLS)

    def _get_properties(self):
        """Create the property list"""
        syn_properties = self.manifest_dict.get("syn_properties")
        language = self.manifest_dict.get("language")
        if language == None:
            language = "vhdl"
        properties = [
            ['part', '$(SYN_DEVICE)' +
                     '$(SYN_PACKAGE)' +
                     '$(SYN_GRADE)', 'current_project'],
            ['target_language', language, 'current_project'],
            ['top', '$(TOP_MODULE)', 'get_property srcset [current_run]']]
        fetchto = self.manifest_dict.get("fetchto")
        if not fetchto is None:
            properties.append(['ip_repo_paths', fetchto, 'current_fileset'])
        if not syn_properties is None:
            properties.extend(syn_properties)
        return properties

    def _makefile_syn_tcl(self):
        """Create a Xilinx synthesis project by TCL"""
        prop_val = 'set_property "{0}" "{1}" [{2}]'
        prop_opt = 'set_property -name {{{0}}} -value {{{1}}} -objects [{2}]'
        project_new = ['# project properties']
        synthesize_new = ['# synthesize properties']
        par_new = ['# par properties']
        properties = self._get_properties()
        for prop in properties:
            if len(prop) > 1:
                tmp = prop_val
                name_list = prop[0].split()
                if len(name_list) == 2:
                    if name_list[1] == "options":
                        tmp = prop_opt
                    else:
                        logging.error('Unknown project property: %s', prop[0])
                if len(prop) == 2:
                    name_hierarchy = name_list[0].split(".")
                    if name_hierarchy[0] == "steps":
                        if name_hierarchy[1] == "synth_design":
                            synthesize_new.append(tmp.format(
                                prop[0], prop[1], 'get_runs synth_1'))
                        else:
                            par_new.append(tmp.format(
                                prop[0], prop[1], 'get_runs impl_1'))
                    else:
                        project_new.append(tmp.format(
                            prop[0], prop[1], 'current_project'))
                elif len(prop) == 3:
                    project_new.append(tmp.format(prop[0], prop[1], prop[2]))
                else:
                    logging.error('Unknown project property: %s', prop[0])
        tmp_dict = {}
        tmp_dict["project"] = self._tcl_controls["project"]
        tmp_dict["synthesize"] = self._tcl_controls["synthesize"]
        tmp_dict["par"] = self._tcl_controls["par"]
        self._tcl_controls["project"] = tmp_dict["project"].format(
            "\n".join(project_new))
        self._tcl_controls["synthesize"] = tmp_dict["synthesize"].format(
            "synth_1",
            "\n".join(synthesize_new))
        self._tcl_controls["par"] = tmp_dict["par"].format(
            "impl_1",
            "\n".join(par_new))
        super(ToolXilinx, self)._makefile_syn_tcl()


    def _makefile_syn_files(self):
        """Write the files TCL section of the Makefile"""
        super(ToolXilinx, self)._makefile_syn_files()
        ret = []
        fileset_dict = {}
        sources_list = []
        fileset_dict.update(self.CORE_FILES)
        for filetype in fileset_dict:
            ip_list = []
            for file_aux in self.fileset:
                if isinstance(file_aux, filetype):
                    ip_core = os.path.splitext(os.path.basename(shell.tclpath(file_aux.rel_path())))[0]
                    ip_list.append(ip_core)
            if not ip_list == []:
                ret.append( 'IP_CORES += ' '{1}\n'.format(filetype.__name__, ' \n' 'IP_CORES += '.format(filetype.__name__).join(ip_list)))
                if not fileset_dict[filetype] is None:
                    sources_list.append(filetype)
        self.writeln('\n'.join(ret))


