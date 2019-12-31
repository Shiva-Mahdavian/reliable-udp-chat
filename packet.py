class Packet:

	STATE_READY = (4, "Ready")
	STATE_SENT = (5, "Sent")
	STATE_ACKED = (10, "Acked")
	STATE_RECEIVED = (13, "Received")
	STATE_LOSS = (15, "Loss")
	STATE_CORRUPT = (20, "Corrupt")
	STATE_RESENT = (25, "Resent")


	def __init__(self, sequence_number=0, acked=False, payload=[], length=1024, state=0, retransmits=0):
		self.sequence_number = sequence_number
		self.acked = acked
		self.payload = payload
		self.length = length
		self.state = state


	def set_sequence_number(self, sequence_number):
		self.sequence_number = sequence_number


	def set_acked(self, acked):
		self.acked = acked


	def set_payload(self, payload):
		self.payload = payload


	def get_payload(self):
		return self.payload


	def get_sequence_number(self):
		return self.sequence_number


	def get_acked(self):
		return self.acked


	def __str__(self):
		return str(sequence_number) + ", " + str(self.state) + ", " + str(self.retransmits)

