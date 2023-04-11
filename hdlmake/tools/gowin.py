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

"""Module providing support for Xilinx Vivado synthesis"""


from __future__ import absolute_import
from .makefilesyn import MakefileSyn
from ..sourcefiles.srcfile import (VHDLFile, VerilogFile, SVFile,
                                   SDCFile, CSTFile)


class ToolGowin(MakefileSyn):

    """Class providing the interface for Xilinx Vivado synthesis"""

    TOOL_INFO = {
        'name': 'Gowin',
        'id': 'gowin',
        'windows_bin': 'gw_sh.exe ',
        'linux_bin': 'gw_sh ',
        'project_ext': ''
    }

    STANDARD_LIBS = ['ieee', 'std']

    SUPPORTED_FILES = {
        SDCFile: 'add-file $(sourcefile)',
        CSTFile: 'add-file $(sourcefile)'}

    HDL_FILES = {
        VHDLFile:    'add-file $(sourcefile)',
        SVFile:      'add-file $(sourcefile)',
        VerilogFile: 'add-file $(sourcefile)'}

    CLEAN_TARGETS = {'clean': [".fs", "*.gprj.user", "*.gprj", "$(PROJECT).impl", "$(PROJECT_FILE)"]}

    TCL_CONTROLS = {'bitstream': '$(TCL_OPEN)\n'
                                 'run syn'
                                 '\n'
                                 'run pnr\n'
                                 '$(TCL_CLOSE)'}

    def __init__(self):
        super(ToolGowin, self).__init__()
        self._tcl_controls.update(ToolGowin.TCL_CONTROLS)
