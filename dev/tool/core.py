from engine.engine_template import EngineTemplate


def run(cmds):
    return eval("{}({})".format(cmds[0], EngineTemplate.exec_formatter_api(cmds)))


def usage(cmds):
    import dev.tool.gooz_usage
    return dev.tool.gooz_usage.mem_state()


def calc(cmds):
    import dev.tool.gooz_calculator
    return dev.tool.gooz_calculator.calc(cmds)


def rtc(cmds):
    import dev.tool.gooz_rtc
    return dev.tool.gooz_rtc.run(cmds)


def cpu_temp(cmds):
    import dev.tool.gooz_internal_sensors
    return dev.tool.gooz_internal_sensors.cpu_temperature(cmds)


def hall(cmds):
    import dev.tool.gooz_internal_sensors
    return dev.tool.gooz_internal_sensors.hall(cmds)


def thread(cmds):
    import dev.tool.gooz_thread
    return dev.tool.gooz_thread.run(cmds)


def client(cmds):
    import dev.tool.gooz_client
    return dev.tool.gooz_client.run(cmds)


def cpu_freq(cmds):
    import dev.tool.gooz_cpu_freq
    return dev.tool.gooz_cpu_freq.cpu_freq(cmds)
