"""Module providing the synthesis functionality for writing Makefiles"""


import logging

def load_syn_tool(tool_name):
    """Funtion that checks the provided module_pool and generate an
    initialized instance of the the appropriated synthesis tool"""
    from .ise import ToolISE
    from .planahead import ToolPlanAhead
    from .vivado import ToolVivado
    from .quartus import ToolQuartus
    from .diamond import ToolDiamond
    from .radiant import ToolRadiant
    from .libero import ToolLibero
    from .liberosoc import ToolLiberoSoC
    from .ice_yosys import ToolIceYosys
    from .ecp5_yosys import ToolEcp5Yosys
    from .gowin_yosys import ToolGowinYosys
    from .gowin import ToolGowin
    available_tools = {'ise': ToolISE,
                       'planahead':  ToolPlanAhead,
                       'vivado': ToolVivado,
                       'quartus': ToolQuartus,
                       'diamond': ToolDiamond,
                       'radiant_synp': ToolRadiant,
                       'libero': ToolLibero,
                       'liberosoc': ToolLiberoSoC,
                       'ecp5_yosys': ToolEcp5Yosys,
                       'gowin_yosys': ToolGowinYosys,
                       'gowin': ToolGowin,
                       'ice_yosys': ToolIceYosys}
    if tool_name in available_tools:
        logging.debug("Synthesis tool to be used found: %s", tool_name)
        return available_tools[tool_name]()
    else:
        raise Exception("Unknown synthesis tool: " + tool_name
                        + "    Supported synthesis tools are " + available_tools.keys())


def load_sim_tool(tool_name):
    """Funtion that checks the provided module_pool and generate an
    initialized instance of the the appropriated simulation tool"""
    from .iverilog import ToolIVerilog
    from .iverilog_cocotb import ToolIVerilogCocotb
    from .isim import ToolISim
    from .modelsim import ToolModelsim
    from .modelsim_cocotb import ToolModelsimCocotb
    from .questasim import ToolQuestasim
    from .active_hdl import ToolActiveHDL
    from .riviera import ToolRiviera
    from .ghdl import ToolGHDL
    from .vivado_sim import ToolVivadoSim
    from .vivado_sim_uvm import ToolVivadoSimUVM
    available_tools = {'iverilog': ToolIVerilog,
                       'iverilog_cocotb': ToolIVerilogCocotb,
                       'isim': ToolISim,
                       'modelsim':  ToolModelsim,
                       'modelsim_cocotb':  ToolModelsimCocotb,
                       'questasim':  ToolQuestasim,
                       'active_hdl': ToolActiveHDL,
                       'riviera':  ToolRiviera,
                       'ghdl': ToolGHDL,
                       'vivado_sim_uvm': ToolVivadoSimUVM,
                       'vivado_sim': ToolVivadoSim}
    if tool_name in available_tools:
        logging.debug("Simulation tool to be used found: %s", tool_name)
        return available_tools[tool_name]()
    else:
        raise Exception("Unknown simulation tool: " + tool_name
                        + "    Supported simulation tools are " + available_tools.keys())
