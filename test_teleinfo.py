import unittest

from teleinfo import Teleinfo


class TestTeleinfo(unittest.TestCase):

    def setUp(self):
        self.teleinfo = Teleinfo(url='loop://', timeout=0, baudrate=115200)

    def test_read_simple_complete_frame(self):

        with self.teleinfo as teleinfo:
            self.teleinfo._write(bytearray.fromhex(teleinfo_data))

            frame = teleinfo._read_next_frame()
            self.assertEqual(frame['PPOT'], '00')
            self.assertEqual(frame['MOTDETAT'], '000000')
            self.assertEqual(frame['OPTARIF'], 'HC..')
            self.assertEqual(frame['IMAX3'], '016')
            self.assertEqual(frame['IMAX1'], '011')
            self.assertEqual(frame['ADCO'], '049801282083')
            self.assertEqual(frame['HCHC'], '008005927')
            self.assertEqual(frame['PAPP'], '00330')
            self.assertEqual(frame['HHPHC'], 'E')
            self.assertEqual(frame['IINST1'], '001')
            self.assertEqual(frame['IMAX2'], '019')
            self.assertEqual(frame['IINST3'], '001')
            self.assertEqual(frame['IINST2'], '000')
            self.assertEqual(frame['ISOUSC'], '20')
            self.assertEqual(frame['PMAX'], '05090')
            self.assertEqual(frame['PTEC'], 'HP..')
            self.assertEqual(frame['HCHP'], '008197993')

    def test_read_a_frame_during_a_stream(self):

        with self.teleinfo as teleinfo:
            self.teleinfo._write(bytearray.fromhex(teleinfo_data[-20:] + teleinfo_data + teleinfo_data[30:]))

            frame = teleinfo._read_next_frame()
            self.assertEqual(frame['PPOT'], '00')
            self.assertEqual(frame['MOTDETAT'], '000000')
            self.assertEqual(frame['OPTARIF'], 'HC..')
            self.assertEqual(frame['IMAX3'], '016')
            self.assertEqual(frame['IMAX1'], '011')
            self.assertEqual(frame['ADCO'], '049801282083')
            self.assertEqual(frame['HCHC'], '008005927')
            self.assertEqual(frame['PAPP'], '00330')
            self.assertEqual(frame['HHPHC'], 'E')
            self.assertEqual(frame['IINST1'], '001')
            self.assertEqual(frame['IMAX2'], '019')
            self.assertEqual(frame['IINST3'], '001')
            self.assertEqual(frame['IINST2'], '000')
            self.assertEqual(frame['ISOUSC'], '20')
            self.assertEqual(frame['PMAX'], '05090')
            self.assertEqual(frame['PTEC'], 'HP..')
            self.assertEqual(frame['HCHP'], '008197993')


teleinfo_data = '02 0a 41 44 43 4f 20 30 34 39 38 30 31 32 38 32 30 38 33 20 44 0d 0a 4f 50 54 41 52 49 46 20 48 43 2e 2e 20 3c 0d 0a 49 53 4f 55 53 43 20 32 30 20 38 0d 0a 48 43 48 43 20 30 30 38 30 30 35 39 32 37 20 25 0d 0a 48 43 48 50 20 30 30 38 31 39 37 39 39 33 20 41 0d 0a 50 54 45 43 20 48 50 2e 2e 20 20 0d 0a 49 49 4e 53 54 31 20 30 30 31 20 49 0d 0a 49 49 4e 53 54 32 20 30 30 30 20 49 0d 0a 49 49 4e 53 54 33 20 30 30 31 20 4b 0d 0a 49 4d 41 58 31 20 30 31 31 20 32 0d 0a 49 4d 41 58 32 20 30 31 39 20 3b 0d 0a 49 4d 41 58 33 20 30 31 36 20 39 0d 0a 50 4d 41 58 20 30 35 30 39 30 20 34 0d 0a 50 41 50 50 20 30 30 33 33 30 20 27 0d 0a 48 48 50 48 43 20 45 20 30 0d 0a 4d 4f 54 44 45 54 41 54 20 30 30 30 30 30 30 20 42 0d 0a 50 50 4f 54 20 30 30 20 23 0d 03'
