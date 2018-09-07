import contextlib
import signal
import sqlite3

from teleinfo import Teleinfo
from test_teleinfo import teleinfo_data


if __name__ == '__main__':

    with contextlib.closing(sqlite3.connect('kalewa.db')) as connection:
        with connection:
            with contextlib.closing(connection.cursor()) as cursor:
                cursor.execute('create table if not exists teleinfo (date timestamp default current_timestamp, '
                               'adco varchar(12), papp integer, hchp integer, hchc integer, ptec varchar(4), '
                               'iinst1 integer, iinst2 integer, iinst3 integer, imax1 integer, imax2 integer, '
                               'imax3 integer, isousc integer, pmax integer, optarif varchar(4), ppot varchar(2), '
                               'motdetat varchar(6))')

            with Teleinfo(url='loop://', timeout=10, baudrate=115200) as teleinfo:
                def _exit_gracefully(signum, frame):
                    print('roeuchoreuh')
                    print('roeuchoreuh')
                    print('roeuchoreuh')
                    print('roeuchoreuh')
                    teleinfo.stop()

                signal.signal(signal.SIGINT, _exit_gracefully)
                signal.signal(signal.SIGTERM, _exit_gracefully)

                for frame in teleinfo.read_frames():
                    with contextlib.closing(connection.cursor()) as cursor:
                        sql = 'insert into teleinfo (ppot, motdetat, optarif, imax1, imax2, imax3, adco, hchc, hchp, papp, iinst1, iinst2, iinst3, isousc, pmax, ptec) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
                        cursor.execute(sql, (frame['PPOT'], frame['MOTDETAT'], frame['OPTARIF'], frame['IMAX1'], frame['IMAX2'], frame['IMAX3'], frame['ADCO'], frame['HCHC'], frame['HCHP'], frame['PAPP'], frame['IINST1'], frame['IINST2'], frame['IINST3'], frame['ISOUSC'], frame['PMAX'], frame['PTEC']))
                    connection.commit()

