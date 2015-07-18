import serial

chunk = 1024
msg_sz = 8

def skip_to_msg(buff):
	"""Returns the number of bytes to skip to the next message"""
	skip = 0
	while True:
		if skip >= len(buff): 
			return None
		byte = ord(buff[skip])
		if byte & 0x80:
			return skip
		skip += 1

def unpack_msg(bytes):
	"""Returns mic and phd readings given 7 message bytes"""
	mic = bytes[0] | (bytes[1] << 7) | (bytes[2] << 14) | (bytes[3] << 21) | ((bytes[4] & 0xf) << 28)
	if mic & (1 << 31): mic -= 1 << 32
	phd = bytes[5] | (bytes[6] << 7)
	return mic, phd

def get_data(port):
	"""Data stream iterator"""
	com  = serial.Serial(port)
	buff = ''
	skip = None
	hdr  = None
	while True:
		s = com.read(chunk)
		if buff:
			buff += s
		else:
			buff = s
		if len(buff) < chunk:
			continue
		if skip is None:
			skip = skip_to_msg(buff)
			if skip is None:
				buff = ''
				continue
			buff = buff[skip:]
		n = len(buff) // msg_sz
		for i in range(n):
			msg = buff[i*msg_sz:(i+1)*msg_sz]
			bytes = [ord(c) for c in msg]
			if hdr is None:
				hdr = bytes[0]
			else:
				hdr += 1
				hdr &= 0xff
				hdr |= 0x80
				assert hdr == bytes[0]
			yield unpack_msg(bytes[1:])
		buff = buff[n*msg_sz:]
