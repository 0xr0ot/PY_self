def state_dict(self, destination=None, prefix='', keep_vars=False):

	"""Returns a dictionary containing a whole state of the module.

	Both parameters and persistent buffers (e.g. running averages) are
	included. Keys are corresponding parameter and buffer names.

	When keep_vars is ``True``, it returns a Variable for each parameter
	(rather than a Tensor).

	Args:
		destination (dict, optional):
			if not None, the return dictionary is stored into destination.
			Default: None
		prefix (string, optional): Adds a prefix to the key (name) of every
			parameter and buffer in the result dictionary. Default: ''
		keep_vars (bool, optional): if ``True``, returns a Variable for each
			parameter. If ``False``, returns a Tensor for each parameter.
			Default: ``False``

	Returns:
		dict:
			a dictionary containing a whole state of the module

	Example:
		>>> module.state_dict().keys()
		['bias', 'weight']
	"""
	
	if destination is None:
		destination = OrderedDict()
	for name, param in self._parameters.items():
		if param is not None:
			destination[prefix + name] = param if keep_vars else param.data
	for name, buf in self._buffers.items():
		if buf is not None:
			destination[prefix + name] = buf
	for name, module in self._modules.items():
		if module is not None:
			module.state_dict(destination, prefix + name + '.', keep_vars=keep_vars)
	return destination
