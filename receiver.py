import sys
import random
import socket
from struct import *
from utils import *
from packet import Packet


def send_ack(sequence_number, client_address, server_socket):
	ack_packet = pack('IHH', sequence_number, ACK_HEADER_INT, ZERO_ONE_INT)
	server_socket.sendto(ack_packet, client_address)


if __name__ == '__main__':
	port = int(sys.argv[1])
	host = HOST_IP
	window_size = int(sys.argv[2])

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	server_socket.bind((host, port))

	window_first_index = 0
	window_last_index = window_first_index + window_size - 1
	probability = 0.1
	last_received = -1
	is_received = [False] * window_size
	receive_buffer = [None] * window_size

	while True:
		packed_packet, server_address = server_socket.recvfrom(1024)
		packet = Packet(packed_packet)

		if packet.header == CLOSE_HEADER_INT:
			break

		random_number = random.random()

		print("Packet number", packet.sequence_number, "received")

		if packet.sequence_number < window_first_index:
			send_ack(packet.sequence_number, server_address, server_socket)
		else:
			if packet.equal_checksums(packet.sequence_number, packet.header, packet.data):
				if packet.sequence_number >= window_first_index and packet.sequence_number <= window_last_index:
					if packet.sequence_number == window_first_index:
						receive_buffer[window_first_index % window_size] = None
						is_received[window_first_index % window_size] = False
						window_first_index += 1
						window_last_index += 1
					elif not is_received[packet.sequence_number % window_size]:
						receive_buffer[packet.sequence_number] = packet
						is_received[packet.sequence_number % window_size] = True
				print("Acknowledge sent for packet number", packet.sequence_number)
				send_ack(packet.sequence_number, server_address, server_socket)
			else:
				print("Different checksums")
