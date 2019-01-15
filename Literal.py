#notes

#not is a unary operator (needs own literal when seen, only takes one term (imaginary parentheses))

class Literal(object):
	def __init__(self, parts, indent, sub, neg = False):
		self.terms = []
		self.type = 0
		self.indent = indent
		self.subliteral = sub
		#self.assumption = False
		self.valid = False
		self.negative = neg

		paren = 0
		unaryop = 0
		innerlit = 0

		print "NEW LITERAL", parts, indent, sub, neg

		for x, a in enumerate(parts):
			if paren == 0:
				if a == '(':
					if unaryop == 0:
						paren = 1
						innerlit = x + 1
					else:
						unaryop += 1
				elif a == ')':
					if unaryop != 0:
						unaryop -= 1
						if unaryop == 1:
							self.terms.append(Literal(parts[innerlit:x], self.indent, True, True))
							unaryop = 0
							innerlit = 0
					else:
						ERROR
				elif unaryop == 0:
					if a == "not":
						if unaryop == 0:
							innerlit = x + 2
							unaryop = 1
					elif a == "and":
						if self.type != 0 and self.type != 1:
							ERROR
						if len(self.terms) == 0:
							ERROR
						self.type = 1
					elif a == "or":
						if self.type != 0 and self.type != 2:
							ERROR
						if len(self.terms) == 0:
							ERROR
						self.type = 2
					elif a == "false":
						self.terms.append("false")
					elif a == "then":
						if self.type != 0:
							ERROR
						if len(self.terms) == 0:
							ERROR
						self.type = 3
					elif a == "iff":
						if self.type != 0:
							ERROR
						if len(self.terms) == 0:
							ERROR
						self.type = 4
					elif a == ";":
						break
					else:
						self.terms.append(a)
			else:
				if a == '(':
					paren += 1
				elif a == ')':
					paren -= 1
					if paren == 0:
						self.terms.append(Literal(parts[innerlit:x], self.indent, True))

		if self.type == 0:
			if len(self.terms) > 1:
				ERROR
			elif len(self.terms) == 1 and not self.negative:
				if isinstance(self.terms[0], Literal):
					if self.terms[0].negative:
						self.terms = self.terms[0].terms
						self.negative = True
			else:
				pass
		elif len(self.terms) == 0:
			ERROR

		print self.terms, self.negative, self.type

	def contains(self, lit):
		print "CONTAINS", self.terms
		if isinstance(lit, str):
			print "lit str"
			for t in self.terms:
				print t
				if isinstance(t, str):
					if lit == t:
						return True
				else:
					if t.equals(lit):
						return True
		else:
			print lit.terms
			for t in self.terms:
				print t
				if isinstance(t, str):
					if lit.equals(t):
						return True
				else:
					if t.equals(lit):
						return True
		print "FAILS"
		return False

	def equals(self, lit):
		print "EQUALS", self.terms, lit
		if isinstance(lit, str):
			print "str", lit
			if len(self.terms) == 1 and self.type == 0 and not self.negative:
				print self.terms[0] == lit
				return self.terms[0] == lit
			print self.type
			return False
		elif self.type == lit.type and self.negative == lit.negative and len(self.terms) == len(lit.terms):
			print "lit lit", self.terms, lit.terms
			tcount = 0
			for t in self.terms:
				print t
				if not lit.contains(t):
					return False
				else:
					tcount += 1
			print tcount
			return len(self.terms) == tcount
		return False

	def andintro(self, lit):#self is a term in lit
		if lit.type != 1:
			return False

		return lit.contains(self)

	def andelim(self, lit):#lit is a term in self
		if self.type != 1:
			return False

		return self.contains(lit)

	def orintro(self, lit):#lit is type 2 and one of its terms is self's value
		if lit.type != 2:
			return False

		return lit.contains(self)

	def orelim(self, lit, part):#subproof something
		pass

	def thenintro(self, lit, part):#lit is assumption of current subproof?
		print "THEN", self.terms, lit.terms
		if lit.type != 3:
			return False
		return self.equals(lit.terms[part])

	def thenelim(self, lit1, lit2):#
		if self.type == 3:
			return lit1.equals(self.terms[0]) and lit2.equals(self.terms[1])
		return False

	def iffintro(self, lit1, lit2):#close to thenintro *2
		if self.type == 4 and lit1.type == 3 and lit2.type == 3:
			s1 = isinstance(self.terms[0], str)
			s2 = isinstance(self.terms[1], str)
			s3 = isinstance(lit1.terms[0], str)
			s4 = isinstance(lit1.terms[1], str)
			s5 = isinstance(lit2.terms[0], str)
			s6 = isinstance(lit2.terms[1], str)
			first = False
			r = False
			if not s1:
				if self.terms[0].equals(lit1.terms[0]):
					first = True
				elif not self.terms[0].equals(lit1.terms[1]):
					return False
			else:
				if not s3:
					if lit1.terms[0].equals(self.terms[0]):
						first = True
					elif not s4:
						if not lit1.terms[1].equals(self.terms[0]):
							return False
					elif self.terms[0] != lit1.terms[1]:
						return False
				else:
					if self.terms[0] == lit1.terms[0]:
						first = True
					elif not s4:
						if not lit1.terms[1].equals(self.terms[0]):
							return False
					elif self.terms[0] != lit1.terms[1]:
						return False

			if first:
				if not s1:
					if not self.terms[0].equals(lit2.terms[1]):
						return False
				elif not s6:
					if not lit2.terms[1].equals(self.terms[0]):
						return False
				elif self.terms[0] != lit2.terms[1]:
					return False
			else:
				if not s1:
					if not self.terms[0].equals(lit2.terms[0]):
						return False
				elif not s5:
					if not lit2.terms[0].equals(self.terms[0]):
						return False
				elif self.terms[0] != lit2.terms[0]:
					return False

			if first:
				if not s2:
					if not self.terms[1].equals(lit2.terms[1]):
						return False
				elif not s6:
					if not lit2.terms[1].equals(self.terms[1]):
						return False
				elif self.terms[0] != lit2.terms[1]:
					return False
			else:
				if not s2:
					if not self.terms[1].equals(lit2.terms[0]):
						return False
				elif not s5:
					if not lit2.terms[0].equals(self.terms[1]):
						return False
				elif self.terms[1] != lit2.terms[0]:
					return False

			if first:
				if not s2:
					if not self.terms[1].equals(lit1.terms[1]):
						return False
				elif not s4:
					if not lit1.terms[1].equals(self.terms[1]):
						return False
				elif self.terms[1] != lit1.terms[1]:
					return False
			else:
				if not s2:
					if not self.terms[1].equals(lit1.terms[0]):
						return False
				elif not s3:
					if not lit1.terms[0].equals(self.terms[1]):
						return False
				elif self.terms[1] != lit1.terms[0]:
					return False
			return True
		return False

	def iffelim(self, lit1, lit2):#cclose to thenelim
		if self.type == 4:
			return (lit1.equals(self.terms[0]) and lit2.equals(self.terms[1])) or (lit2.equals(self.terms[0]) and lit1.equals(self.terms[1]))
		return False

	def notintro(self, lit):#part 1 is same as false intro
		return self.falseintro(lit)

	def notelim(self, lit):
		print "NOT", self.terms, lit.terms
		if self.negative:
			if len(self.terms) != 1:
				return False
			if self.terms[0].negative: 
				if len(self.terms[0].terms) != 1:
					return False
				print self.terms[0].terms[0]
				return lit.equals(self.terms[0].terms[0])
		return False

	def falseintro(self, lit):#lit is negative self
		if self.negative != lit.negative:
			self.negative = lit.negative
			r = lit.equals(self)
			self.negative = not lit.negative
			return r
		return False

	def falseelim(self, lit):#lit is exactly false
		return len(lit.terms) == 1 and lit.terms[0] == "false"
