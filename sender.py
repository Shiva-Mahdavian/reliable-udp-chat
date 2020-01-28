import sys
import random
import signal
import threading
import socket
from struct import pack
from packet import Packet
from utils import *


message = "Hello World!" * MESSAGES_COUNT

sequence_number = 0
window_first_index = -1
window_last_index = -1
last_acked = -1
acked_count = -1

send_completed = False
acked_completed = False

send_buffer = []
timeout_timers = []

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
lock = threading.Lock()


def get_message_string_next_byte():
	global send_completed
	global message
	if message:
		ret = message[0]
		message = message[1:len(message)]
	else:
		ret = ""
		send_completed = True
	return ret


def get_next_message_segment():
	global send_completed
	message = ''
	while len(message) < MAXIMUM_SEGMENT_SIZE and not send_completed:
		message += get_message_string_next_byte()
	return message


def timeouts_signal_handler(signal_number, _):
	global window_first_index
	global window_last_index
	global send_buffer
	global lock
	global timeout_timers
	global WINDOW_SIZE

	if acked_completed:
		return

	i = window_first_index
	while i <= window_last_index:
		timeout_timers[i % WINDOW_SIZE] = timeout_timers[i % WINDOW_SIZE] - 1
		lock.acquire()
		if timeout_timers[i % WINDOW_SIZE] < 1 and send_buffer[i % WINDOW_SIZE] != None:
			packet = send_buffer[i % WINDOW_SIZE]
			print("Timeout, resending packet #" + str(i))
			client_socket.sendto(packet, (HOST_IP, HOST_PORT))
			timeout_timers[i % WINDOW_SIZE] = TIMEOUT
		lock.release()
		i = i + 1


def look_for_acks():
	global window_first_index
	global send_buffer
	global WINDOW_SIZE
	global client_socket
	global acked_count
	global acked_completed
	global send_completed
	global window_last_index

	while not acked_completed:
		packed_packet, addr = client_socket.recvfrom(8)
		packet = Packet(packed_packet)
		ack_number = packet.sequence_number
		print("Received ACK #" + str(ack_number))
		if ack_number == window_first_index:
			lock.acquire()
			send_buffer[window_first_index % WINDOW_SIZE] = None
			timeout_timers[window_first_index % WINDOW_SIZE] = 0
			lock.release()
			acked_count = acked_count + 1
			window_first_index = window_first_index + 1
		elif ack_number >= window_first_index and ack_number <= window_last_index:
			send_buffer[ack_number % WINDOW_SIZE] = None
			timeout_timers[ack_number % WINDOW_SIZE] = 0
			acked_count += 1
		if send_completed and acked_count >= window_last_index:
			acked_completed = True

ack_thread = threading.Thread(target=look_for_acks, args=())
ack_thread.start()

signal.signal(signal.SIGALRM, timeouts_signal_handler)
signal.setitimer(signal.ITIMER_REAL, 0.01, 0.01)

window_first_index = 0

while not send_completed:
	send_index = window_last_index + 1
	packet_data = get_next_message_segment().encode()
	packet_checksum = calculate_string_checksum(pack('IH' + str(len(packet_data)) + 's', sequence_number, ZERO_ONE_INT, packet_data).decode())

	packet = Packet()
	packet.sequence_number = sequence_number
	packet.checksum = int(packet_checksum)
	packet.header = ZERO_ONE_INT
	packet.data = packet_data

	if send_index < WINDOW_SIZE:
		send_buffer.append(packet.get_pack())
		timeout_timers.append(TIMEOUT)
	else:
		send_buffer[send_index % WINDOW_SIZE] = packet.get_pack()
		timeout_timers[send_index % WINDOW_SIZE] = TIMEOUT

	print("Sending #" + str(sequence_number))
	client_socket.sendto(packet.get_pack(), (HOST_IP, HOST_PORT))

	window_last_index = window_last_index + 1
	sequence_number = sequence_number + 1

while not acked_completed:
	pass

close_packet = Packet()
close_packet.sequence_number = sequence_number
close_packet.checksum = ALL_ZEROS_INT
close_packet.header = ALL_ONES_INT
close_packet.data = "".encode()

client_socket.sendto(close_packet.get_pack(), (HOST_IP, HOST_PORT))
client_socket.close()
