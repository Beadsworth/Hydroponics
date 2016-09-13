#!/usr/bin/env python
# imports
import unittest
import time

from HydroIO import interpret_response, BAD_MESSAGE_PACKET, BAD_PIN_PACKET, TIMEOUT_ERR_PACKET, UNKNOWN_ERR_PACKET, \
    ACK_MESSAGE, ACK_PACKET, send_binary, on_off, set_pin, START_MESSAGE, trigger_safe_mode, init_command, \
    send_command, int_2_hex_str, get_pin, cycle

import HydroIO

time.sleep(3)
tested_pins = [2, 3, 4, 5, 6, 7, 8, 9]


def arduino_reset():
    # time.sleep(0.1)
    send_binary(START_MESSAGE)
    # time.sleep(0.1)
    send_binary('E0 E4 02 00 E1')
    # time.sleep(0.1)

    send_binary(START_MESSAGE)
    # time.sleep(0.1)
    send_binary('E0 E4 02 01 E1')
    # time.sleep(0.1)

    send_binary(START_MESSAGE)
    # time.sleep(0.1)
    send_binary('E0 E4 02 00 E1')
    # time.sleep(0.1)


#@unittest.skip("Skipping TestBinary Class...")
class TestBinary(unittest.TestCase):
    def test_sanity(self):
        pass

    def setUp(self):

        pass

    def tearDown(self):

        arduino_reset()

    @classmethod
    def setUpClass(cls):
        arduino_reset()
        trigger_safe_mode()
        time.sleep(5)

    def test_interpret_response_ack_message(self):

        ack_message_response = bytes.fromhex(ACK_MESSAGE)
        status = interpret_response(ack_message_response)
        self.assertEqual(status, (False, ACK_PACKET), 'Wrong status returned!')

    def test_interpret_response_correct_command_message(self):

        good_command_message_responses = [
            bytes.fromhex('E0 E4 08 00 E1'),
            bytes.fromhex('E0 E4 08 01 E1')
        ]
        for good_response in good_command_message_responses:
            status = interpret_response(good_response)
            self.assertEqual(status, (True, good_response[3]), 'Wrong status returned!')

        bad_command_message_responses = [
            bytes.fromhex('E0 E4 08 02 E1'),
            bytes.fromhex('E0 E4 08 03 E1'),
            bytes.fromhex('E0 E4 08 04 E1'),
            bytes.fromhex('E0 E4 08 05 E1'),
            bytes.fromhex('E0 E4 08 FF E1')
        ]
        for bad_response in bad_command_message_responses:
            status = interpret_response(bad_response)
            self.assertEqual(status, (False, UNKNOWN_ERR_PACKET), 'Wrong status returned!')

    def test_interpret_response_bad_message(self):

        bad_message_response = bytes.fromhex('E0 E3 E7 E3 E1')
        status = interpret_response(bad_message_response)
        self.assertEqual(status, (False, BAD_MESSAGE_PACKET), 'Wrong status returned!')

    def test_interpret_response_bad_pin(self):

        bad_pin_response = bytes.fromhex('E0 E3 E6 E3 E1')
        status = interpret_response(bad_pin_response)
        self.assertEqual(status, (False, BAD_PIN_PACKET), 'Wrong status returned!')

    def test_interpret_response_timeout(self):

        timeout_response = bytes.fromhex('E0 E3 E8 E3 E1')
        status = interpret_response(timeout_response)
        self.assertEqual(status, (False, TIMEOUT_ERR_PACKET), 'Wrong status returned!')

    def test_interpret_response_unknown_message(self):

        unknown_responses = [
            bytes.fromhex('E1 E4 08 00 E1'),
            bytes.fromhex('E0 E4 08 00 E0'),
            bytes.fromhex('E0 FF 08 00 E1'),
            bytes.fromhex('E0 01 08 00 E1'),
            bytes.fromhex('E3 E3 E3 E3 E3'),
            bytes.fromhex('E0 E4 08 00 E1 E1'),
            bytes.fromhex('E0 E4 08 00 E1 E0 E4 08 00 E1'),
            bytes.fromhex(''),
            bytes.fromhex('E0 E4 08 E1'),
            bytes.fromhex('E0 E4 08 02 E1'),
            bytes(100),
            bytes.fromhex('00 00 00 00 00'),
            bytes.fromhex('E9 E9 E9 E9 E9')
        ]
        for response in unknown_responses:
            status = interpret_response(response)
            self.assertEqual(status, (False, UNKNOWN_ERR_PACKET), 'Wrong status returned!')

    def test_send_binary_long_message_is_truncated(self):

        bad_message1 = ACK_MESSAGE + ' E0'
        bad_message2 = 'E4 02 01 E0'

        response1 = send_binary(bad_message1)
        # time.sleep(0.1)
        response2 = send_binary(bad_message2)

        status1 = interpret_response(response1)
        status2 = interpret_response(response2)
        self.assertEqual(status1, (False, BAD_MESSAGE_PACKET), 'Bad message sent -- second message')
        self.assertEqual(status2, (False, BAD_MESSAGE_PACKET), 'Bad message sent -- second message')

    def test_send_binary_bad_message(self):

        bad_messages = [
            'E1 E4 08 00 E1',
            'E0 E4 08 00 E0',
            'E0 FF 08 00 E1',
            'E0 01 08 00 E1',
            'E3 E3 E3 E3 E3',
            'E0 E4 08 00 E1 E1',
            'E0 E4 08 00 E1 E0 E4 08 00',
            'E0 E4 08 00 E1 E0 E4 08 00 E4'  # 100 byte message
            'E0 E4 08 00 E1 E0 E4 08 00 E4'  # 100 byte message
            'E0 E4 08 00 E1 E0 E4 08 00 E4'  # 100 byte message
            'E0 E4 08 00 E1 E0 E4 08 00 E4'  # 100 byte message
            'E0 E4 08 00 E1 E0 E4 08 00 E4'  # 100 byte message
            'E0 E4 08 00 E1 E0 E4 08 00 E4'  # 100 byte message
            'E0 E4 08 00 E1 E0 E4 08 00 E4'  # 100 byte message
            'E0 E4 08 00 E1 E0 E4 08 00 E4'  # 100 byte message
            'E0 E4 08 00 E1 E0 E4 08 00 E4'  # 100 byte message
            'E0 E4 08 00 E1 E0 E4 08 00 E4',  # 100 byte message
            'E0 E4 08 E1',
            'E0 E4 08 02 E1',
            '00 00 00 00 00',
            'E9 E9 E9 E9 E9'
        ]
        for message in bad_messages:  # first message, i.e. waiting state

            arduino_reset()
            print('test case: ' + str(message))
            response = send_binary(message)
            status = interpret_response(response)
            self.assertEqual(status, (False, BAD_MESSAGE_PACKET), 'Bad message sent -- first message')

        for message in bad_messages:  # second message, i.e. listening state

            arduino_reset()
            send_binary(START_MESSAGE)
            # time.sleep(0.1)

            response = send_binary(message)
            status = interpret_response(response)
            self.assertEqual(status, (False, BAD_MESSAGE_PACKET), 'Bad message sent -- second message')

    def test_send_binary_bad_pin(self):

        bad_pins = [
            'E0 E4 00 00 E1',
            'E0 E4 01 00 E1',
            'E0 E4 13 00 E1',
            'E0 E4 14 00 E1',
            'E0 E4 15 00 E1',
            'E0 E4 E0 00 E1',
            'E0 E4 E1 00 E1',
            'E0 E4 E2 00 E1',
            'E0 E4 E3 00 E1',
            'E0 E4 E4 00 E1',
            'E0 E4 E5 00 E1',
            'E0 E4 E6 00 E1',
            'E0 E4 E7 00 E1',
            'E0 E4 E8 00 E1',
            'E0 E4 E9 00 E1',
            'E0 E4 0D 00 E1',
            'E0 E4 0E 00 E1',
            'E0 E4 0F 00 E1',
            'E0 E4 10 00 E1'

        ]

        for pin in bad_pins:  # second message, i.e. listening state

            arduino_reset()
            send_binary(START_MESSAGE)  # go to arduino listening state
            # time.sleep(0.1)

            response = send_binary(pin)
            status = interpret_response(response)
            self.assertEqual(status, (False, BAD_PIN_PACKET), 'Bad pin sent -- second message')

    def test_send_binary_timeout(self):

        send_binary(START_MESSAGE)  # go to arduino listening state
        print('sleeping...')
        time.sleep(15)

        response = send_binary(START_MESSAGE)  # send dummy message to read response
        # time.sleep(0.1)

        status = interpret_response(response)
        self.assertEqual(status, (False, TIMEOUT_ERR_PACKET), 'No timeout!')


#@unittest.skip("Skipping TestCommands Class...")
class TestCommands(unittest.TestCase):
    def setUp(self):

        pass

    def tearDown(self):

        arduino_reset()

    @classmethod
    def setUpClass(cls):
        arduino_reset()

    def test_trigger_safe_mode(self):

        for i in range(2):
            time.sleep(5)
            arduino_reset()
            status = trigger_safe_mode()
            self.assertEqual(status, (True, BAD_MESSAGE_PACKET))

    def test_init_command(self):

        arduino_reset()

        status = trigger_safe_mode()
        self.assertEqual(status, (True, BAD_MESSAGE_PACKET))
        time.sleep(10)

        status = init_command()
        self.assertEqual(status, [True, bytes.fromhex(ACK_MESSAGE)])  # first time -> good

        status = init_command()
        self.assertEqual(status, [False, bytes.fromhex('E0 E3 E7 E3 E1')])  # second time -> bad

    def test_send_command(self):

        arduino_reset()
        tested_states = [1, 0]

        for state in tested_states:  # setting commands
            for pin in tested_pins:
                arduino_reset()

                n_pin_hex_string = int_2_hex_str(pin)
                n_state_hex_string = int_2_hex_str(state)
                hex_string = 'E0 E4 ' + n_pin_hex_string + ' ' + n_state_hex_string + ' E1'

                status = init_command()
                self.assertEqual(status, [True, bytes.fromhex(ACK_MESSAGE)])  # make sure init_command worked

                status = send_command(pin, state)
                self.assertEqual(status, [True, bytes.fromhex(hex_string)])  # make sure pin AND state are same

            for pin in tested_pins:  # query, do for each state change above

                arduino_reset()

                n_pin_hex_string = int_2_hex_str(pin)
                query_number = 229
                n_state_hex_string_0 = int_2_hex_str(0)
                n_state_hex_string_1 = int_2_hex_str(1)
                hex_string_0 = 'E0 E4 ' + n_pin_hex_string + ' ' + n_state_hex_string_0 + ' E1'
                hex_string_1 = 'E0 E4 ' + n_pin_hex_string + ' ' + n_state_hex_string_1 + ' E1'

                status = init_command()
                self.assertEqual(status, [True, bytes.fromhex(ACK_MESSAGE)])  # make sure init_command worked

                status = send_command(pin, query_number)
                self.assertEqual(status[0], True)  # make sure executed correctly
                self.assertTrue((status[1] == bytes.fromhex(hex_string_0))
                                or (status[1] == bytes.fromhex(hex_string_1)))


#@unittest.skip("Skipping TestGetSetPins Class...")
class TestGetSetPins(unittest.TestCase):
    def setUp(self):

        pass

    def tearDown(self):

        arduino_reset()

    @classmethod
    def setUpClass(cls):
        arduino_reset()
        trigger_safe_mode()
        time.sleep(5)

    def test_get_pin(self):

        for pin in tested_pins:
            arduino_reset()

            status1 = get_pin(pin)
            status2 = get_pin(pin)
            self.assertTrue(status1[0])
            self.assertTrue((status1[1] == 0) or (status1[1] == 1))
            self.assertTrue(status2[0])
            self.assertTrue((status2[1] == 0) or (status2[1] == 1))

    def test_set_pin(self):

        query_state = 229
        tested_states = [1, 0]

        for pin in tested_pins:

            arduino_reset()

            tf_state_5 = set_pin(pin, query_state)
            tf_state_6 = set_pin(pin, query_state)  # repeat, should do nothing

            self.assertTrue(tf_state_5[0] and tf_state_6[0])  # all successful
            self.assertTrue((tf_state_5[1] == 0) or (tf_state_5[1] == 1))
            self.assertTrue((tf_state_6[1] == 0) or (tf_state_6[1] == 1))

            for state in tested_states:
                arduino_reset()

                tf_state_1 = set_pin(pin, state)
                tf_state_2 = get_pin(pin)
                tf_state_3 = set_pin(pin, state)  # repeat, should do nothing
                tf_state_4 = get_pin(pin)

                self.assertTrue(tf_state_1[0] and tf_state_2[0] and tf_state_3[0] and tf_state_4[0])  # all successful
                self.assertEqual(tf_state_1[1], state)
                self.assertEqual(tf_state_2[1], state)
                self.assertEqual(tf_state_3[1], state)
                self.assertEqual(tf_state_4[1], state)

    def test_cycle(self):

        cycle(2)
        pass

    def test_many_valid_get_pin_calls(self):

        for i in range(25):
            status = get_pin(2)
            self.assertTrue(status[0])

    def test_many_valid_set_pin_calls(self):
        for i in range(25):
            status = set_pin(2, 0)
            self.assertTrue(status[0])

    def test_set_pin_with_invalid_state(self):

        bad_states = [2, 230, 0.1, -1, 'a']

        for state in bad_states:
            with self.assertRaises(ValueError):
                set_pin(2, state)


if __name__ == '__main__':
    unittest.main()
