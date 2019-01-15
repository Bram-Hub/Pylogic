import sys, os, tkFileDialog, math, random
from Tkinter import Tk

import Literal


#does not check if lines used for reasoning are valid (add an "and proof[line].valid")

#false intro messes up sometimes with multiple nots (and thus not intro, too)

#needs line checking algorithm outside of just subproofs (loop backwards and keep track of indent, indent only moves left, ignore lines to right)

#no or elim



"""		#error checking
		for i, c in enumerate(line):
			if c == '(':
				paren += 1
			elif c == ')':
				paren -= 1
				#if paren < 0:

		if paren != 0:
			print "LINE", lnum, ": SYNTAX ERROR 01"
			print line
			return
		if incomplete:
			print "LINE", lnum, ": SYNTAX ERROR 02"
			print line
			return"""




root = Tk()
root.withdraw()


def readfile(pfile):
	global lines

	lines = pfile.readlines()#[l[:-1] for l in pfile.readlines()]

#	print lines


def interpret():
	#keep track of values

	proof = []

	#line by line values
	indent = 0
	last_indent = 0

	#error checking
	paren = 0
	incomplete = False


	for lnum, line in enumerate(lines):
		indent = 0

		#error checking?

		#parsing
		if line[-1] == '\n':
			line = line[:-1]

		while line[0] == '\t':
			indent += 1
			line = line[1:]

		line = line.split(' ')
		while '' in line:
			line.remove('')

		parts = []
		for i, part in enumerate(line):
			part = part.split('(')
			for x in xrange(len(part) - 1):
				part.insert(2 * x, '(')

			for j, p in enumerate(part):
				p = p.split(')')
				for x in xrange(len(p) - 1):
					p.insert(2 * len(p) + 1, ')')

				for l in p:
					if l != '':
						parts.append(l)

		print parts

		if parts[0] == '#':
			proof.append(Literal.Literal(parts[1:], 0, False))
		elif parts[0] == '-':
			proof.append(Literal.Literal(parts[1:], indent, False))
		elif parts[0] == 'STOP':
			break
		else:
			reason = parts[-3:-1] + parts[-1].split(',')
			proof.append(Literal.Literal(parts[:-4], indent, False))
			
			#deal with reason dashes
			sub = []
			if '-' in reason[-1]:
				sub = [int(x) for x in l.split('-')]

			ind = indent
			brk = False
			if reason[0] == "AND":
				if reason[1] == "INTRO":
					for l in reason[2:]:
						if not proof[int(l) - 1].andintro(proof[-1]):
							print "Invalid line", lnum
							brk = True
							break
					if not brk:
						proof[-1].valid = True
						print "VALID AND INTRO", lnum
				elif reason[1] == "ELIM":
					for l in reason[2:]:
						if not proof[int(l) - 1].andelim(proof[-1]):
							print "Invalid line", lnum
							brk = True
							break
					if not brk:
						proof[-1].valid = True
						print "VALID AND ELIM", lnum
			elif reason[0] == "OR":
				if reason[1] == "INTRO":
					for l in reason[2:]:
						if not proof[int(l) - 1].orintro(proof[-1]):
							print "Invalid line", lnum
							brk = True
							break
					if not brk:
						proof[-1].valid = True
						print "VALID OR INTRO", lnum
				elif reason[1] == "ELIM":
					for l in reason[2:]:
						if not proof[int(l) - 1].orelim(proof[-1]):
							print "Invalid line", lnum
							brk = True
							break
					if not brk:
						proof[-1].valid = True
						print "VALID OR ELIM", lnum
			elif reason[0] == "THEN":
				if reason[1] == "INTRO":
					part1 = False
					brk = False
					if proof[sub[0] - 1].thenintro(proof[-1], 0):
						part1 = True
					if part1:
						for ln in proof[sub[0] - 1 : sub[1]]:
							print "CHECK", ln
							if ln.indent == ind + 1:
								if ln.thenintro(proof[-1], 1):
									brk = True
									print "brk"
									break
							elif ln.indent < ind:
								print "not brk"
								break

					if not brk:
						print "Invalid line", lnum
					else:
						proof[-1].valid = True
						print "VALID THEN INTRO", lnum
				elif reason[1] == "ELIM":
					if not proof[int(reason[2]) - 1].thenelim(proof[int(reason[3]) - 1], proof[-1]):
						print "Invalid line", lnum
					else:
						proof[-1].valid = True
						print "VALID THEN ELIM", lnum
			elif reason[0] == "IFF":
				if reason[1] == "INTRO":
					if not proof[-1].iffintro(proof[int(reason[2]) - 1], proof[int(reason[3]) - 1]):
						print "Invalid line", lnum
					else:
						proof[-1].valid = True
						print "VALID IFF INTRO", lnum
				elif reason[1] == "ELIM":
					if not proof[int(reason[2]) - 1].iffelim(proof[int(reason[3]) - 1], proof[-1]):
						print "Invalid line", lnum
						brk = True
						break
					else:
						proof[-1].valid = True
						print "VALID IFF ELIM", lnum
			elif reason[0] == "NOT":
				if reason[1] == "INTRO":#copy then intro except leads to false (ln.equals("false")) and proof[-1] is negative of proof[sub[0] - 1]
					part1 = False
					brk = False
					if proof[sub[0] - 1].notintro(proof[-1]):
						part1 = True
					if part1:
						for ln in proof[sub[0] - 1 : sub[1]]:
							print "CHECK", ln
							if ln.indent == ind + 1:
								if ln.equals("false"):
									brk = True
									print "brk"
									break
							elif ln.indent < ind:
								print "not brk"
								break

					if not brk:
						print "Invalid line", lnum
					else:
						proof[-1].valid = True
						print "VALID NOT INTRO", lnum
				elif reason[1] == "ELIM":
					if not proof[int(reason[2]) - 1].notelim(proof[-1]):
						print "Invalid line", lnum
						brk = True
						break
					else:
						proof[-1].valid = True
						print "VALID FALSE ELIM", lnum
			elif reason[0] == "FALSE":
				if reason[1] == "INTRO":
					if not proof[int(reason[2]) - 1].falseintro(proof[int(reason[3]) - 1]):
						print "Invalid line", lnum
					if not brk:
						proof[-1].valid = True
						print "VALID FALSE INTRO", lnum
				elif reason[1] == "ELIM":
					if not proof[-1].falseelim(proof[int(reason[2]) - 1]):
						print "Invalid line", lnum
					else:
						proof[-1].valid = True
						print "VALID FALSE ELIM", lnum

		

	# print "prove"
	# print lines
	# for line in proof:
		# print line.type, line.terms


while 1:
	pfile = tkFileDialog.askopenfile(initialdir = "projects")#, filetypes = [("PYLOGIC PROOF", ".pyl")])
	if pfile is None:
		sys.exit()

	readfile(pfile)

	interpret()

