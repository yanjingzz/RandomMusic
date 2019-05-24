
import random
from enum import Enum
import warnings


class Note(object):
	"""A musical note class"""
	class NEnum(Enum):
		Ab = 0
		A  = 1
		Bb = 2
		B  = 3
		C  = 4
		Db = 5
		D  = 6
		Eb = 7
		E  = 8
		F  = 9
		Gb = 10
		G  = 11
		
	N_NOTES = 12
	NAME = {
		NEnum.A: 'A', 
		NEnum.Bb: 'Bb/A#', 
		NEnum.B: 'B', 
		NEnum.C: 'C', 
		NEnum.Db: 'Db/C#', 
		NEnum.D: 'D',
		NEnum.Eb: 'Eb/D#', 
		NEnum.E: 'E', 
		NEnum.F: 'F', 
		NEnum.Gb: 'Gb/F#', 
		NEnum.G: 'G', 
		NEnum.Ab: 'Ab/G#'
		}

	LILY_NOTE = {
		NEnum.A: 'a', 
		NEnum.Bb: 'bf', 
		NEnum.B: 'b', 
		NEnum.C: 'c', 
		NEnum.Db: 'df', 
		NEnum.D: 'd',
		NEnum.Eb: 'ef', 
		NEnum.E: 'e', 
		NEnum.F: 'f', 
		NEnum.Gb: 'gf', 
		NEnum.G: 'g', 
		NEnum.Ab: 'af'
		}

	def __init__(self, note):
		super(Note, self).__init__()
		if isinstance(note, int):
			self.note = Note.NEnum(note)
		elif isinstance(note, Note.NEnum):
			self.note = note
		elif isinstance(note, str):
			self.note = Note.NEnum[note]
		elif isinstance(note, Note):
			self.note = note.note
		else:
			raise TypeError("Note __init__ unsupported type for '{}'".format(type(note)))
	
	@staticmethod
	def random():
		return Note(random.choice((list(Note.NEnum))))

	def __str__(self):
		return Note.NAME[self.note]

	def __repr__(self):
		return self.__str__()

	def __add__(self, other):
		if isinstance(other, int):
			return Note((self.note.value + other) % Note.N_NOTES)
		else:
			error_msg = "Unsupported operand type(s) for +: '{}' and '{}'".format(self.__class__, type(other))
			raise TypeError(error_msg)
	def __eq__(self, other):
		return self.note == other.note
	def __ne__(self, other):
		return not self.__eq__(other)

	def lily(self):
		return Note.LILY_NOTE[self.note]
		

class Quality(object):
	"""Chord Quality"""
	class QEnum(Enum):
		Maj = 0
		Min = 1
		Dom  = 2
		Sus  = 3
		HalfDim = 4
		Dim  = 5
		Aug = 6

	N_MAIN = 4
	N_ALL = 7

	FULL_NAME = {
		QEnum.Maj: 'major',  
		QEnum.Min: 'minor', 
		QEnum.Dom: 'dominant', 
		QEnum.Sus: 'suspended', 
		QEnum.HalfDim: 'half-diminished', 
		QEnum.Dim: 'diminished', 
		QEnum.Aug: 'augmented'}

	NAME = {
		QEnum.Maj: 'Maj',  
		QEnum.Min: 'min', 
		QEnum.Dom: 'dom', 
		QEnum.Sus: 'sus', 
		QEnum.HalfDim: 'half-dim', 
		QEnum.Dim: 'dim', 
		QEnum.Aug: 'aug'}

	INTERVALS = {
		QEnum.Maj: [0,4,7,11],  
		QEnum.Min: [0,3,7,10], 
		QEnum.Dom: [0,4,7,10], 
		QEnum.Sus: [0,5,7], 
		QEnum.HalfDim: [0,3,6,10], 
		QEnum.Dim: [0,3,6,9], 
		QEnum.Aug: [0,4,8]
		}

	LILY_MOD = {
		QEnum.Maj: 'maj7',  
		QEnum.Min: 'm7', 
		QEnum.Dom: '7', 
		QEnum.Sus: 'sus4', 
		QEnum.HalfDim: 'm7.5-', 
		QEnum.Dim: 'dim', 
		QEnum.Aug: 'aug'
		}

	def __init__(self, quality):
		super(Quality, self).__init__()
		if isinstance(quality, Quality.QEnum):
			self.quality = quality
		elif isinstance(quality, Quality):
			self.quality = quality.quality
		elif isinstance(quality,str):
			try:
				quality = quality[0].upper() + quality[1:].lower()
				self.quality = Quality.QEnum[quality]
			except KeyError as e:
				quality = quality.lower()
				for k, v in Quality.FULL_NAME.items():
					if quality == v:
						self.quality = k
						return
				raise RuntimeError("Quality name not found")
				

				
		else:
			raise TypeError("Quality __init__ unsupported type for '{}'".format(type(note)))
		
	def random(kind = 'main'):
		if kind == 'main':
			return Quality(random.choice(list(Quality.QEnum)[:Quality.N_MAIN]))
		else:
			return Quality(random.choice(list(Quality.QEnum)))
	
	def all_qualities(kind = 'main'):
		if kind == 'main':
			return list(Quality.QEnum)[:Quality.N_MAIN]
		else:
			return list(Quality.QEnum)

	def __str__(self):
		return Quality.NAME[self.quality]

	def intervals(self):
		return Quality.INTERVALS[self.quality]

	def __eq__(self, other):
		return self.quality == other.quality
	def __ne__(self, other):
		return not self.__eq__(other)

	def lily(self):
		return Quality.LILY_MOD[self.quality]

		

class Chord(object):
	"""A Chord class"""
	def __init__(self, root_or_name, quality = None):
		super(Chord, self).__init__()
		if quality:
			self.root = Note(root_or_name)
			self.quality = Quality(quality)
		else:
			if isinstance(root_or_name,str):
				l = root_or_name.split()
				if len(l) == 2:
					self.root = Note(l[0])
					self.quality = Quality(l[1])
				elif len(l) == 1:
					self.root = Note(root_or_name)
					self.quality = Quality("dom")
				else:
					raise RuntimeError("Chord name should be '<root> <quality>'")
			else:
				raise TypeError("name should be a string")


	def random(kind='main'):
		return Chord(Note.random(),Quality.random(kind))

	def notes(self):
		return [self.root+i for i in self.quality.intervals()]

	def __str__(self):
		return str(self.root) + ' ' + str(self.quality)

	def __repr__(self):
		return str(self)

	def __eq__(self, other):
		return self.quality == other.quality and self.note == other.note

	def __ne__(self, other):
		return not self.__eq__(other)

	def __contains__(self, item):
		if isinstance(item, Note):
			return item in self.notes()
		else:
			raise TypeError("in operand for Chord unsupported type for '{}'".format(type(item)))

	def lily_chord(self):
		return self.root.lily() + "1:" + self.quality.lily()

	def lily_notes(self):
		ret = "< "
		for n in self.notes():
			ret += n.lily() + " "
		ret += ">"
		return ret


class Scale(object):
	"""A Scale or mode"""
	class SEnum(Enum):
		Chromatic = 0
		Ionian = 1
		Major = 1
		Maj = 1
		Dorian = 2
		Phrygian = 3
		Lydian = 4
		Mixolidian = 5
		Aeolian = 6
		Minor = 6
		Min = 6
		Locrian = 7
		Penta = 8

	INTERVALS = {
		SEnum.Chromatic: [0,1,2,3,4,5,6,7,8,9,10,11],
		SEnum.Ionian: [0,2,4,5,7,9,11],
		SEnum.Dorian: [0,2,3,5,7,9,10],
		SEnum.Phrygian: [0,1,3,5,7,8,10],
		SEnum.Lydian: [0,2,4,6,7,9,11],
		SEnum.Mixolidian: [0,2,4,5,7,9,10],
		SEnum.Aeolian: [0,2,3,5,7,8,10],
		SEnum.Locrian: [0,1,3,5,6,8,10],
		SEnum.Penta: [0,2,4,7,9]
	}

			
	def __init__(self, root_or_name, scale = None):
		super(Scale, self).__init__()
		if scale:
			self.root = Note(root_or_name)
			self._setScale(scale)
		else:
			if isinstance(root_or_name,str):
				l = root_or_name.split()
				if len(l) == 2:
					self.root = Note(l[0])
					self._setScale(l[1])
				elif len(l) == 1:
					self.root = Note(root_or_name)
					self._setScale("Major")

				else:
					raise RuntimeError("Scale name should be '<root> <quality>'")
			else:
				raise TypeError("name should be a string")
		
	def _setScale(self, scale):
		if isinstance(scale, Scale.SEnum):
			self.scale = scale
		elif isinstance(scale, str):
			self.scale = Scale.SEnum[scale]
		else:
			raise TypeError("Note __init__ unsupported type for '{}' and '{}'".format(type(note)))

	def notes(self):
		intervals = Scale.INTERVALS[self.scale]
		return [self.root+i for i in intervals]

	def __str__(self):
		return str(self.root) + ' ' + str(self.scale.name)

	def __repr__(self):
		return self.__str__()

	def __contains__(self, item):
		if isinstance(item, Note):
			return item in self.notes()
		elif isinstance(item, Chord):
			return all(n in self.notes() for n in item.notes())
		else:
			raise TypeError("in operand for Chord unsupported type for '{}'".format(type(item)))

	def chords(self):
		ret = []
		for r in self.notes():
			chrs = [Chord(r,q) for q in Quality.QEnum]
			for c in chrs:
				ret.append(c) if c in self else ret
		return ret


class RandomMusic(object):

	def __init__(self, n_bars = 8, root_rep = False, 
			chord_rep = False, in_scale = None, quals = "main"):
		super(RandomMusic, self).__init__()
		self.n_bars = n_bars
		self.root_rep = root_rep
		self.chord_rep = chord_rep
		if in_scale == None:
			self.in_scale = Scale("C", "Chromatic")
		elif isinstance(in_scale,Scale):
			self.in_scale = in_scale
		else:
			msg = "in_scale needs to be of type Scale, not '{}'".format(type(in_scale))
			raise TypeError(msg)
		if isinstance(quals, str):
			self.quals = Quality.all_qualities(quals)
		elif isinstance(quals, list) and all(isinstance(quals, Quality) for q in quals):
			self.quals = quals
		else:
			msg = "quals needs to be a sting or a list of Quality, not '{}'".format(type(in_scale))
			raise TypeError(msg)
		

	def generate_chords(self):
		s = self.in_scale
		n = self.n_bars
		qs = self.quals
		if self.root_rep:
			all_chords = s.chords()
			filter(lambda c: c.quality in qs)
		else:
			all_chords = []
			for r in s.notes():
				chords = [Chord(r, q) for q in qs]
				chords = list(filter(lambda c: c in s, chords))
				if chords:
					all_chords.append(random.choice(chords))
			
		if self.chord_rep:
			ret = [random.choice(all_chords) for i in range(n)]
		else:
			if len(all_chords) < n:
				msg = "Not enough chords to generate {} bars,".format(n) \
					+ " generating {} bars instead".format(len(all_chords))
				warnings.warn(msg)
				random.shuffle(all_chords)
				ret = all_chords
			else:
				ret = random.sample(all_chords,n)
		self.chords = ret
		return ret

	def generate_melody(self):
		pass

	def generate(self):
		self.generate_chords()
		self.generate_melody()

	def lily(self):
		if not self.chords:
			raise RuntimeError("You need to generate the chords first")
		ret = """\\language "english"
\\header {
  title = "Random Generation"
}


\\score {
 <<
  \\tempo 4 = 120
  \\chords {

"""
		ret += " ".join([c.lily_chord() for c in self.chords])
		ret += """
  }

  \\relative c' {  
   \\numericTimeSignature
   \\time 4/4
    
"""
		ret += "\n   ".join([c.lily_notes() for c in self.chords])
		ret += """
  }
 >>

  \\layout {}
  \\midi {}
}
"""
		return ret



		


def main():
	r = RandomMusic()
	r.generate()
	print(r.lily())

if __name__ == '__main__':
	main()





