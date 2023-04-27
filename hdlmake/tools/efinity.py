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

"""Module providing support for Efinix Efinity synthesis"""


from __future__ import absolute_import
from .makefilesyn import MakefileSyn
from ..sourcefiles.srcfile import (VHDLFile, VerilogFile, SVFile,
                                   SDCFile, XMLFile)
from ..util import shell
import os
from jinja2 import Environment, PackageLoader

class ToolEfinity(MakefileSyn):

    """Class providing the interface for Gowin synthesis"""

    TOOL_INFO = {
        'name': 'efinity',
        'id': 'efinity',
        'windows_bin': 'efx_run.bat ',
        'linux_bin': 'efx_run.py ',
        'project_ext': 'xml'
    }

    STANDARD_LIBS = ['ieee', 'std']

    SUPPORTED_FILES = {
        SDCFile: 'add_file $(sourcefile)'}

    HDL_FILES = {
        VHDLFile:    'add_file $(sourcefile)',
        SVFile:      'add_file $(sourcefile)',
        VerilogFile: 'add_file $(sourcefile)'}

    CLEAN_TARGETS = {'clean': ["*.log", "*.hex", "*.vdb", "work_*", "outflow"],
                     'mrproper': [""]}

    TCL_CONTROLS = {'bitstream': '$(TCL_INTERPRETER) $(PROJECT).xml\n' }

    def __init__(self):
        super(ToolEfinity, self).__init__()
        self._tcl_controls.update(ToolEfinity.TCL_CONTROLS)
        self.jinja_env = Environment(
            loader=PackageLoader(__package__, "templates"),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )
        self.project_template=self.jinja_env.get_template("efinity/project_top.xml.j2")

    def _render_template(self, target_file, template_vars={}):
        """
        Render project template 
        """
        file_path = os.path.join("./", target_file)
        with open(file_path, "w") as f:
            f.write(self.project_template.render(template_vars))

    def _makefile_syn_tcl(self):
        """Create the Makefile TCL dictionary for the selected tool"""
        pass

    def _makefile_syn_files(self):
        """Write the files TCL section of the Makefile"""
        ret = []
        fileset_dict = {}
        sources_list = []
        vlog_list = []
        vhdl_list = []
        sdc_list = []
        fileset_dict.update(self.HDL_FILES)
        fileset_dict.update(self.SUPPORTED_FILES)
        for filetype in fileset_dict:
            file_list = []
            for file_aux in self.fileset:
                if isinstance(file_aux, filetype):
                    if filetype == VHDLFile: 
                        vhdl_list.append(shell.tclpath(file_aux.rel_path()))
                    if filetype == SDCFile: 
                        sdc_list.append(shell.tclpath(file_aux.rel_path()))
                    if filetype == VerilogFile: 
                        vlog_list.append(shell.tclpath(file_aux.rel_path()))
                        if isinstance(file_aux, SVFile):
                        # Discard SVerilog files for verilog type.
                            continue
                    file_list.append(shell.tclpath(file_aux.rel_path()))
            if not file_list == []:
                ret.append( 'SOURCES_{0} += ' '{1}\n'.format(filetype.__name__, ' \n' 'SOURCES_{0} += '.format(filetype.__name__).join(file_list)))
                if not fileset_dict[filetype] is None:
                    sources_list.append(filetype)
        temp_var = {
            "project_name":self.manifest_dict["syn_project"],
            "device_family":self.manifest_dict["syn_family"],
            "device_device":self.manifest_dict["syn_device"]+self.manifest_dict["syn_package"],
            "device_speedgrade":self.manifest_dict["syn_grade"],
            "vlog_files":vlog_list,
            "vhdl_files":vhdl_list,
            "sdc_files":sdc_list,
        }
        project_file=self.manifest_dict["syn_project"] + ".xml"
        self._render_template(project_file, temp_var)
        self.writeln('\n'.join(ret))

    def _makefile_syn_build(self):
        """Generate the synthesis Makefile targets for handling design build"""
        stage_previous = "files.tcl"
        stage_list = ["project", "synthesize", "translate",
                      "map", "par", "bitstream"]
        for stage in stage_list:
            if stage in self._tcl_controls:
                echo_command = '\t\t'
                tcl_command = []
                for command in self._tcl_controls[stage].split('\n'):
                    tcl_command.append(echo_command.format(command))
                command_string = "\n".join(tcl_command)
                if shell.check_windows_commands():
                    command_string = command_string.replace(
                        "'", "")
                self.writeln("""\
{0}: $(PROJECT).xml
\t\t$(TCL_INTERPRETER)$(PROJECT).xml
""".format(stage, stage_previous, stage.upper(),
           command_string, shell.touch_command()))
                stage_previous = stage

    def _makefile_syn_command(self):
        """Create the Makefile targets for user defined commands"""
        pass

    def _makefile_syn_clean(self):
        """Print the Makefile clean target for synthesis"""
        self.makefile_clean()
        self.writeln()
        self.makefile_mrproper()

