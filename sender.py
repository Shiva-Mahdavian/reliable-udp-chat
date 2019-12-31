class Sender:

	MAXIMUM_QUEUE_LENGTH = 100000
	PACKET_SIZE = 512
	ACK = 1
	NAK = 0

	def __init__(self, window_size=0, timeout=0, receive_port=0, send_port=0):
		self.max_window_size = window_size
		self.timeout = timeout
		self.windows = [0] * self.max_window_size
		# TODO:
		socket = DatagramSocket(receive_port)
		self.windows_list = []
		self.receive_port = receive_port
		self.send_port = send_port

		self.window_size = 0
		self.sequence_number = 0
		self.is_block = False
		self.queue = []
		self.queue_index = 0
		# TODO:
		self.timeout_timer = Timer()
		self.number_of_timeouts = 0
		self.max_window_size = 0
		self.receive_port = 0
		self.send_port = 0

		self.log = {}


	def push_to_queue(buf):
		try:
			# TODO:
			packet = Packet(self.sequence_number, buf.bytes(), Packet.STATE_READY)
			self.sequence_number += 1
			queue.append(packet)
			self.write(packet.get_sequence_number(), Packet.STATE_READY)
		except:
			pass


	def write(sequence_number, state):
		if sequence_number in log.keys():
			log.append(state)
		else:
			log[sequence_number] = [state]


	def send_data(self):
		self.is_block = True
		self.number_of_timeouts = 0
		self.packet_data = [0] * self.PACKET_SIZE
		self.timeout_timer = Timer(True)
		self.window_size = 0
		while True:
			while (not self.queue or len(self.queue) == 0) and self.window_size == 0:
				self.is_block = False
			if self.window_size == 0:
				self.is_block = True
				self.window_size = min(len(self.queue), self.max_window_size)
				self.windows = [self.NAK] * self.window_size
				for i in range(self.window_size):
					packet = self.queue[self.queue_index]
					packet.state = Packet.STATE_SENT
					windows_list.append(packet)
					self.write(packet.get_sequence_number(), Packet.STATE_SENT)
					self.send_packet(packet)
			else:
				self.is_block = True
				empty_space = self.adjust_window()
				new_windows = [0] * self.window_size
				ping = 0
				windows_list = windows_list[empty_space:]
				for i in range(empty_space, self.window_size):
					new_windows[ping] = windows[i]
					ping += 1
				