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

"""Module providing support for Mentor Questa simulation"""

from __future__ import print_function
from __future__ import absolute_import
import os

from .makefilevsim import MakefileVsim

class ToolModelsim(MakefileVsim):

    """Class providing the interface for Mentor Questa simulator"""

    TOOL_INFO = {'name': 'Questa',
                 'id': 'questasim',
                 'windows_bin': 'vsim.exe',
                 'linux_bin': 'vsim'}

    STANDARD_LIBS = ['ieee', 'std', 'altera_mf']

    CLEAN_TARGETS = {'clean': ["modelsim.ini", "transcript"],
                     'mrproper': ["*.vcd", "*.wlf"]}

    def __init__(self):
        super(ToolModelsim, self).__init__()
        self.copy_rules["modelsim.ini"] = os.path.join(
            "$(MODELSIM_INI_PATH)", "modelsim.ini")
        self.additional_deps.append("modelsim.ini")

    def _makefile_sim_options(self):
        """Print the Modelsim options to the Makefile"""
        modelsim_ini_path = self.manifest_dict.get("modelsim_ini_path")
        uvm_path = self.manifest_dict.get("uvm_path")
        if modelsim_ini_path == None:
            if self.manifest_dict['sim_path']:
                modelsim_ini_path = os.path.join(
                    self.manifest_dict["sim_path"], "..")
            else:
                modelsim_ini_path = os.path.join(
                    "$(HDLMAKE_QUESTA_PATH)", "..")
        self.custom_variables["MODELSIM_INI_PATH"] = modelsim_ini_path
        modelsim_ini = "-modelsimini modelsim.ini "
        vcom_opt = self.manifest_dict.get("vcom_opt", '')
        self.manifest_dict["vcom_opt"] = modelsim_ini + vcom_opt
        vlog_opt = self.manifest_dict.get("vlog_opt", '')
        self.manifest_dict["vlog_opt"] = modelsim_ini + vlog_opt
        vmap_opt = self.manifest_dict.get("vmap_opt", '')
        self.manifest_dict["vmap_opt"] = modelsim_ini + vmap_opt
        super(ToolModelsim, self)._makefile_sim_options()
