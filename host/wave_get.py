import sys
import wave_rx as rx


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print 'Usage: %s PORT' % sys.argv[0]
		sys.exit(-1)
	try:
		for mic, phd in rx.get_data(sys.argv[1]):
			print mic, phd
	except KeyboardInterrupt:
		sys.stdout.flush()

