#! /usr/bin/env python3

import threading
import time
import copy

#signal = release
#wait = acquire
class RWLock:	
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

class _LightSwitch:
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

class Reader(threading.Thread):
	def run(self):
		print (self, 'start')
		rwl.reader_acquire()
		print (self, 'acquired')
		time.sleep(5)
		print (self, 'finish')
		rwl.reader_release()
		
class Writer(threading.Thread):
	def run(self):
		print (self, 'start')
		rwl.writer_acquire()
		print (self, 'acquired')
		time.sleep(15)
		print (self, 'finish')
		rwl.writer_release()

if __name__ == '__main__' :
	rwl = RWLock()

	Reader().start()
	time.sleep(1)
	Reader().start()
	time.sleep(1)
	Reader().start()
	time.sleep(1)
	Writer().start()
	time.sleep(1)
	Reader().start()
	time.sleep(1)
	Writer().start()
	time.sleep(1)
	Reader().start()