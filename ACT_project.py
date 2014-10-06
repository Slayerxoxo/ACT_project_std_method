#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
:Authors:
	John Smith

:Date:
	2014/10/6
"""

import sys
import os
import codecs


if __name__ == "__main__":
	if len(sys.argv) > 4:
		for arg in [1, 2, 3, 4]:
			if not os.path.isfile(sys.argv[arg]):
				raise SystemExit, "[ERROR] " + sys.argv[arg] + ": file not found !"
	else:
		raise SystemExit, "[ERROR] "+sys.argv[0]+" expected at least 4 arguments !"

	#TODO write your script here.
