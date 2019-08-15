#!/usr/bin/env python3
import random
import copy
import argparse
import os
import sys

class Celular:

	def __init__(self, size, rand):
		self.size = size
		self.state = list()
		self.rule = [0 for x in range(8)]
		for i in range(size):
			if rand:
				self.state.append(random.randint(0,1))
			else:
				self.state.append(0)
		if not rand:
			self.state[size//2] = 1

	def setRule(self,n):
		a = format(n,"08b")
		for i in range(1,9):
			self.rule[-i] = int(a[i-1])

	def applyRule(self):
		newstate = copy.copy(self.state)
		for i in range(self.size):
			t = self.state[i-1] * 4 + 2 * self.state[i] + self.state[(i+1)%self.size]
			newstate[i] = self.rule[t]
		self.state = newstate

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Celular automata emulator")
	parser.add_argument("-s", "--size", help='Size of the automata (width of the image in pixel)', default="50")
	parser.add_argument("-g", "--generations", help="Number of generations to run (height of the image in pixel)", default="50")
	parser.add_argument("-r", "--rule", help="Rule to apply (0 .. 255)", default="30")
	parser.add_argument("-o", "--out", help="Outputfile", default="out.pbm")
	parser.add_argument("-rand", action ='store_true', help = "If set initialize a random first generation")
	args = vars(parser.parse_args())
	height = int(args["generations"])
	width = int(args["size"])
	c = Celular(width, args["rand"])
	c.setRule(int(args["rule"]))
	f = open(args["out"], "w")
	f.write("P1\n")
	f.write("{0} {1}\n".format(width, height))
	for i in range(height):
		f.write("{}\n".format("".join("1 " if x else "0 " for x in c.state)))
		c.applyRule()
	f.close()
