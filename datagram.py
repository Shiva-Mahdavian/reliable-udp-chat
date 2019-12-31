class Datagram:
	
	def __init__(self, source_port, destination_port, length, sequence_number, data):
		self.source_port = source_port
		self.destination_port = destination_port
		self.length = length
		self.sequence_number = sequence_number
		self.data = data

	def to_bytes(self):
		return str(self.source_port) + " " + str(self.destination_port) + " " + str(self.length) + " " + str(self.sequence_number) + " " + str(self.data)
