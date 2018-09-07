import serial
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Teleinfo(object):

    def __init__(self, url, timeout=1, baudrate=9600):
        self._url = url
        self._timeout = timeout
        self._baudrate = baudrate
        self._stop_me = False

    def __enter__(self):
        self._serial = serial.serial_for_url(url=self._url, timeout=self._timeout, baudrate=self._baudrate)
        return self

    def __exit__(self, *args, **kwargs):
        self._serial.close()

    def _write(self, bytes):
        self._serial.write(bytes)

    def read_frames(self):
        while not self._stop_me:
            yield self._read_next_frame()

    def stop(self):
        self._stop_me = True

    def _read_next_frame(self):
        frame = list()

        while frame[-2:] != ['\x02', '\n']:
            frame.append(self._serial.read(1))
        logger.debug('A new frame is coming...')

        frame = list()
        while frame[-1:] != ['\x03']:
            frame.append(self._serial.read(1))

        result = ''.join(frame[:-2])
        logger.debug('New frame received: %s' % result)

        return self._decode_frame(result)

    def _decode_frame(self, frame):
        values = frame.split('\r\n')

        return dict(self._check_item(value) for value in values)

    def _check_item(self, item):
        checksum = self._get_checksum(item)
        values = item.split(' ', 2)

        if values[-1] != checksum:
            raise Exception('Checksum error for item %s' % values[0])

        return values[0], values[1]

    def _get_checksum(self, item):
        result = 0
        for char in item[:-2]:
            result += ord(char)

        result = (result & 63) + 32
        return chr(result)
