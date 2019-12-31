class Queue:



	def __init__(self, window_size, queue_size):
		self.window_size = window_size
		self.current_index = 0
		self.queue = [0] * queue_size
		self.queue_size = queue_size

	def __