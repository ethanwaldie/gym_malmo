import os
import sys
import argparse
import subprocess
import traceback
import logging

from rosalind.db.connection import RosalindDatabase
from rosalind.db.queries import create_client



def build_log_dir():
    base_log_dir = os.path.join(os.path.dirname(__file__), "logs")

    if not os.path.isdir(base_log_dir):
        os.mkdir(base_log_dir)

    log_dir = os.path.join(base_log_dir, "client_pool")

    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)

    return log_dir


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Boots Malmo Minecraft clients for use by experiments. ')


    parser.add_argument('--number', type=int,
                        default=1,
                        help='The number of clients to boot.')
    parser.add_argument('--host', type=str,
                        default='localhost',
                        help='The hostname to stamp in the experiments database.')
    parser.add_argument('--start_port', type=int,
                        default=10000,
                        help='The starting port, client ports will increment from here.')

    args = parser.parse_args()

    try:
        rosiland_connection = RosalindDatabase()
    except:
        print("Unable to connect to Rosiland Database")
        print(traceback.format_exc())
        sys.exit(1)

    if "MALMO_MINECRAFT_ROOT" in os.environ:
        minecraft_dir = os.environ["MALMO_MINECRAFT_ROOT"]
    else:
        print("Unable to find MALMO ROOT DIR! Set $MALMO_MINECRAFT_ROOT!")
        sys.exit(1)

    virtual_monitor = "xvfb-run -a -e /dev/stdout -s '-screen 0 1400x900x24' "

    for i in range(args.number):
        cmd = virtual_monitor + minecraft_dir + "launchClient.sh" + " -port " + str(args.start_port + i)

        proc = subprocess.Popen(cmd,
                                # pipe entire output
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                # use process group, see http://stackoverflow.com/a/4791612/18576
                                preexec_fn=os.setsid, shell=True)

        while True:
            line = proc.stdout.readline()
            print(line)
            if not line:
                raise EOFError("Minecraft process finished unexpectedly")
            if b"CLIENT enter state: DORMANT" in line:
                break
        print("Minecraft process at port {} ready".format(args.start_port + i))
        create_client(rosalind_connection=rosiland_connection,
                      client_address="{}:{}".format(args.host, args.start_port + i))














