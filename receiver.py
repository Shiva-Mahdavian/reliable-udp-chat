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
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	server_socket.bind((HOST_IP, HOST_PORT))

	window_first_index = 0
	window_last_index = window_first_index + WINDOW_SIZE - 1
	last_received = -1
	is_received = [False] * WINDOW_SIZE
	receive_buffer = [None] * WINDOW_SIZE

	while True:
		packed_packet, server_address = server_socket.recvfrom(1024)
		packet = Packet(packed_packet)

		if packet.header == CLOSE_HEADER_INT:
			break

		print("Packet number", packet.sequence_number, "received")

		if packet.sequence_number < window_first_index:
			send_ack(packet.sequence_number, server_address, server_socket)
		else:
			if packet.equal_checksums(packet.sequence_number, packet.header, packet.data):
				if packet.sequence_number >= window_first_index and packet.sequence_number <= window_last_index:
					if packet.sequence_number == window_first_index:
						receive_buffer[window_first_index % WINDOW_SIZE] = None
						is_received[window_first_index % WINDOW_SIZE] = False
						window_first_index += 1
						window_last_index += 1
					elif not is_received[packet.sequence_number % WINDOW_SIZE]:
						receive_buffer[packet.sequence_number] = packet
						is_received[packet.sequence_number % WINDOW_SIZE] = True
				print("Acknowledge sent for packet number", packet.sequence_number)
				send_ack(packet.sequence_number, server_address, server_socket)
			else:
				print("Different checksums")
