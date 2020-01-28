from struct import pack, unpack, calcsize
from utils import BYTES_TO_BITS, ones_complement_not, calculate_string_checksum
from sys import getsizeof 


class Packet:

	def __init__(self, packed_packet=None):
		if packed_packet:
			unpacked_packet = unpack('IHH' + str(getsizeof(packed_packet) - 41) + 's', packed_packet)
			self.sequence_number = unpacked_packet[0]
			self.checksum = unpacked_packet[1]
			self.header = unpacked_packet[2]
			self.data = unpacked_packet[3]
		else:
			self.sequence_number = 0
			self.checksum = 0
			self.header = 0
			self.data = "".encode()

	def __str__(self):
		return str(self.sequence_number) + ", " + str(self.checksum) + ", " + str(self.header) + ", " + str(self.data)

	def get_pack(self):
		return pack('IHH' + str(len(self.data)) + 's', self.sequence_number,self.checksum, self.header, self.data)

	def calculate_checksum(self):
		packed_packet = self.get_pack()
		return calculate_string_checksum(packed_packet)

	def equal_checksums(self, sequence_number, header, data):
		s = pack('IH' + str(len(data)) + 's', sequence_number, header, data).decode()
		return calculate_string_checksum(s) == self.checksum

