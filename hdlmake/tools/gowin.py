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

"""Module providing support for Gowin synthesis"""


from __future__ import absolute_import
from .makefilesyn import MakefileSyn
from ..sourcefiles.srcfile import (VHDLFile, VerilogFile, SVFile,
                                   SDCFile, CSTFile)


class ToolGowin(MakefileSyn):

    """Class providing the interface for Gowin synthesis"""

    TOOL_INFO = {
        'name': 'Gowin',
        'id': 'gowin',
        'windows_bin': 'gw_sh.exe ',
        'linux_bin': 'gw_sh ',
        'project_ext': ''
    }

    STANDARD_LIBS = ['ieee', 'std']

    SUPPORTED_FILES = {
        SDCFile: 'add_file $(sourcefile)',
        CSTFile: 'add_file $(sourcefile)'}

    HDL_FILES = {
        VHDLFile:    'add_file $(sourcefile)',
        SVFile:      'add_file $(sourcefile)',
        VerilogFile: 'add_file $(sourcefile)'}

    CLEAN_TARGETS = {'clean': ["*.fs", "*.gprj.user", "*.gprj", "impl", "$(PROJECT_FILE)"],
                     'mrproper': ["$(PROJECT).fs"]}

    TCL_CONTROLS = {'bitstream': 'source files.tcl\n'
                                 'set_device -device_version $(SYN_DEVICE_VERSION) \
                                  $(SYN_FAMILY)$(SYN_FAMILY_SURFIX)-$(SYN_DEVICE_PREFIX)$(SYN_DEVICE)$(SYN_PACKAGE)$(SYN_GRADE)\n'
                                 'set_option -output_base_name $(PROJECT)_proj\n'
                                 'set_option -top_module $(TOP_MODULE)\n'
                                 'set_option -use_sspi_as_gpio 1\n'
                                 'set_option -use_mspi_as_gpio 1\n'
                                 'set_option -use_ready_as_gpio 1\n'
                                 'set_option -use_done_as_gpio 1\n'
                                 'run syn\n'
                                 'run pnr'}

    def __init__(self):
        super(ToolGowin, self).__init__()
        self._tcl_controls.update(ToolGowin.TCL_CONTROLS)
