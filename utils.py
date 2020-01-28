HOST_IP = "127.0.0.1"
HOST_PORT = 9797

WINDOW_SIZE = 8
TIMEOUT = 10
MAXIMUM_SEGMENT_SIZE = 30

BYTES_TO_BITS = 8

ALL_ZEROS_STR = "0" * (BYTES_TO_BITS * 2)
ALL_ZEROS_INT = int(ALL_ZEROS_STR, 2)

ALL_ONES_STR = "1" * (BYTES_TO_BITS * 2)
ALL_ONES_INT = int(ALL_ZEROS_STR, 2)

ZERO_ONE_STRING = "01" * BYTES_TO_BITS
ZERO_ONE_INT = int(ZERO_ONE_STRING, 2)

ACK_HEADER_STRING = ALL_ZEROS_STR
ACK_HEADER_INT = ALL_ZEROS_INT

CLOSE_HEADER_STR = ALL_ONES_STR
CLOSE_HEADER_INT = ALL_ONES_INT


def ones_complement_not(number):
	return (1 << (2 * BYTES_TO_BITS - 1)) - 1 - number


def calculate_string_checksum(s):
	if len(s) % 2 != 0:
		s = s + str(0)
	index = 0
	ret = 0
	while index < len(s):
		tmp1 = ord(s[index]) * (1 << (BYTES_TO_BITS - 1)) + ord(s[index + 1])
		tmp2 = ret + ones_complement_not(tmp1)
		ret = (tmp2 % (1 << (BYTES_TO_BITS * 2 - 1))) + (tmp2 / (1 << (BYTES_TO_BITS * 2 - 1)))
		index += 2
	return ones_complement_not(ret)
