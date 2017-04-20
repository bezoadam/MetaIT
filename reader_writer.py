#! /usr/bin/env python3

import threading

class ReadWriteLock:
	
	def __init__(self):
		self.__readSwitch = _LightSwitch()
		self.__roomEmpty = threading.Lock()
		self.__turnstile = threading.Lock()
	
	def reader_acquire(self):
		self.__turnstile.acquire()
		self.__turnstile.release()
		self.__readSwitch.acquire(self.__roomEmpty)
	
	def reader_release(self):
		self.__readSwitch.release(self.__roomEmpty)
	
	def writer_acquire(self):
		self.__turnstile.acquire()
		self.__roomEmpty.acquire()
	
	def writer_release(self):
		self.__turnstile.release()
		self.__roomEmpty.release()

#signal = release
#wait = acquire

class _LightSwitch:
	"""An auxiliary "light switch"-like object. The first thread turns on the 
	"switch", the last one turns it off (see [1, sec. 4.2.2] for details)."""
	def __init__(self):
		self.__counter = 0
		self.__mutex = threading.Lock()
	
	def acquire(self, lock):
		self.__mutex.acquire()
		self.__counter += 1
		if self.__counter == 1:
			lock.acquire()
		self.__mutex.release()

	def release(self, lock):
		self.__mutex.acquire()
		self.__counter -= 1
		if self.__counter == 0:
			lock.release()
		self.__mutex.release()

if __name__ == '__main__' :
	print ('test')
