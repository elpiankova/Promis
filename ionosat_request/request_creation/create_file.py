from request_creation.models import Request
from datetime import date
from ionosat_request.settings import BASE_DIR
import os


def create_file(request):
    device_switches = request.switches.all()

    date_start = date.strftime(request.date_start, "%d%m%y")
    date_end = date.strftime(request.date_end, "%d%m%y")
    file_name = 'KNA%(date_start)s%(number)04d.zp' % {
        "date_start": date_start,
        "number": request.number
    }

    file_path = os.path.join(BASE_DIR, 'request_files', file_name)

    if request.device_amount != request.switches.count():
        request.device_amount = request.switches.count()

    # This block writes first line of request file
    file = open(file_path, 'w')
    first_line = ('KNA %(number)04d %(date_start)s %(date_end)s'
                  ' %(orbit_flag)s %(latitude_start)+05.1f'
                  ' %(longitude_left)05.1f %(longitude_right)05.1f'
                  ' %(device_amount)1d\r\n'
                  % {
                      "number": request.number,
                      "date_start": date_start,
                      "date_end": date_end,
                      "orbit_flag": request.orbit_flag,
                      "latitude_start": float(request.latitude_start),
                      "longitude_left": float(request.longitude_left),
                      "longitude_right": float(request.longitude_right),
                      "device_amount": request.device_amount
                  })
    file.write(first_line)

    # This block writes all another lines to request file
    for device_switch in device_switches:
        device = device_switch.device
        mode = device_switch.mode
        #argument_part_len = len(device_switch.argument_part.split("\r\n"))
        line = ('%(device_code)6s %(mode_code)-8s %(time_delay)06.0f'
                ' %(time_duration)06.0f %(argument_part_len)02d\r\n'
                % {
                    "device_code": device.code,
                    "mode_code": mode.code,
                    "time_delay": device_switch.time_delay.total_seconds(),
                    "time_duration": device_switch.time_duration.total_seconds(),
                    "argument_part_len": device_switch.argument_part_len
                })
        file.write(line)

        # This block writes correct end of lines in argument part
        arg_lines = device_switch.argument_part
        if arg_lines:
            if arg_lines[-2:] != '\r\n':
                if arg_lines[-1] == '\n':
                    arg_lines = arg_lines.rstrip('\n')
                arg_lines += '\r\n'

            file.write(arg_lines)

    file.close()

    return file_name
