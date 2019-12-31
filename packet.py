from struct import pack, unpack
from utils import BYTES_TO_BITS, ones_complement_not


class Packet:

	def __init__(self, sequence_number, checksum, header, data):
		self.sequence_number = int(sequence_number)
		self.checksum = int(checksum)
		self.header = header
		self.data = data

	def __init__(self, packed_packet):
		unpacked_packet = unpack('IHH' + str(len(packed_packet.data) - 8) + 's', self.data)
		self.sequence_number = unpacked_packet[0]
		self.checksum = unpacked_packet[1]
		self.header = unpacked_packet[2]
		self.data = unpacked_packet[3]

	def __str__(self):
		return str(self.sequence_number) + ", " + str(self.checksum) + ", " + str(self.header) + ", " + str(self.data)

	def get_pack(self):
		return pack('IHH' + str(len(self.data)) + 's', self.sequence_number,self.checksum, self.header, self.data)

	def calculate_checksum(self):
		packed_packet = self.get_pack()
		return self.calculate_string_checksum(packed_packet)

	def calculate_string_checksum(self, s):
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

	def equal_checksums(self, sequence_number, header, data):
		s = pack('IH' + str(len(data)) + 's', sequence_number, header, data)
		return self.calculate_string_checksum(s)

