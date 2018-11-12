import argparse

def add_standard_env_args(parser):
    parser.add_argument('--tick_speed', type=int,
                        default=20,
                        help='Tick Speed of the Malmo Client in ms (default is 20ms)')
    parser.add_argument('--log_level', type=str,
                        default='DEBUG',
                        help='Python Logging level EG: INFO, ERROR (default is DEBUG)')
    parser.add_argument('--record', type=bool,
                        default=False,
                        help='Flag for Recording Video.')
    parser.add_argument('--record_destination', type=str,
                        default='recording.tgz',
                        help='File to Record video to.')
    parser.add_argument('--boot_minecraft_server', type=bool,
                        default=True,
                        help='Flag for starting the minecraft client as '
                             'as subprocess. If this flag is not set it tries to '
                             'connect on the standard client ports and you need to '
                             'launch the client separately.')
    return parser