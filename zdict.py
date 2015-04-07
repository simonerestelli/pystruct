###########################################################################
# Copyright 2014-2015 Simone Restelli
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###########################################################################
'''
Author: Simone Restelli
'''

import json
import zlib
import collections
import functools
from contextlib import contextmanager


class ZDict(collections.MutableMapping): #, json.JSONEncoder):
	'''This class can be in different states: normal dict, json string, compressed json string
	'''
	_level = None
	_len = None
	_zdata = None

	def __init__(self, *args, **kwargs):
		self._data = {}
		#super(ZDict, self).update(dict(*args, **kwargs))
		comp = kwargs.pop('compress', False)
		if comp:
			self.compress()
		self.update(dict(*args, **kwargs))

	def compress(self, level = None):
		'''Serialize to JSON, deflate the string and clear dict'''
		if not self.compressed:
			#print 'Compressing!'
			self._len = len(self._data)
			self._zdata = zlib.compress(json.dumps(self._data))
			self._data = None
			self._level = level

	def decompress(self):
		'''Returns to the uncompressed form. Discard compressed one'''
		if self.compressed:
			#print 'Decompressing!'
			self._data = json.loads(zlib.decompress(self._zdata))
			self._zdata = None
			self._len = None
		return self._data

	@contextmanager
	def _context(self):
		comp = self.compressed
		data = self.data
		yield data
		if comp:
			#print 'Compressing inline!'
			self._len = len(data)
			self._zdata = zlib.compress(json.dumps(data))

	@property
	def compressed(self):
		return self._zdata is not None

	@property
	def jsonString(self):
		if self.compressed:
			#print 'Decompressing inline JSON!'
			return zlib.decompress(self._zdata)
		return json.dumps(self._data)

	@property
	def data(self):
		if self.compressed:
			#print 'Decompressing inline!'
			return json.loads(zlib.decompress(self._zdata))
		return self._data

	def __getitem__(self, key):
		#self.decompress()
		#print 'GET'
		return self.data[key]

	def __setitem__(self, key, value):
		with self._context() as data:
			data[key] = value

	def __delitem__(self, key):
		with self._context() as data:
			del data[key]

	def __len__(self):
		return self._len if self._len is not None else len(self._data)

	def __iter__(self):
		return iter(self.data)
		#def _gen():
		#	keys = self.data.keys()
		#	for x in keys:
		#		print 'Y'
		#		yield x
		#return _gen()

	def __repr__(self):
		return repr(self.data)

	def update(self, other):
		with self._context() as data:
			data.update(other)

	#def default(self, o)

