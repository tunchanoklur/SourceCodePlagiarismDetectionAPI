# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 13:44:18 2019

@author: hitsu
"""
from __future__ import print_function
import sys
import hashlib
# This is not required if you've installed pycparser into
# your site-packages/ with setup.py
#
sys.path.extend(['.', '..'])

from pycparser import parse_file, c_parser, c_generator

class ReturnInfo:
    def __init__(self, return_hash, return_weight = 0):
        self.return_hash = return_hash
        self.return_weight = return_weight
        
def translate_to_c(filename):
    """ Simply use the c_generator module to emit a parsed AST.
    """
    import subprocess
    
    subprocess.call(['gcc','-nostdinc', '-E', r'-I..\utils\fake_libc_include',  filename, '-o', 'test_preprocess.c'])
    #ast = parse_file('test_preprocess.c')
    parser = c_parser.CParser()
    file = open(filename,'r')
    file_data = file.read()
    ast = parser.parse(file_data, filename)
    
    #ast = parse_file(filename, use_cpp = True, cpp_path = 'C:\\Users\\hitsu\\Anaconda3\\Library\\mingw-w64\\bin\\gcc.exe')
#    ast = parse_file(filename, use_cpp=True,
#            cpp_path='C:\\Users\\hitsu\\Anaconda3\\Library\\mingw-w64\\bin\\gcc.exe',
#            cpp_args=['-nostdinc','-E', r'-IC:\Users\hitsu\Desktop\senior project\pycparser-master\utils\fake_libc_include'])
    ast.show(showcoord=True)
    print("AST TYPE:",type(ast))
    #generator = c_generator.CGenerator()
    #print(generator.visit(ast))
    postordertraversal(ast)
    recursive_postordertraversal(ast,0)

#------------------------------------------------------------------------------
def postordertraversal(node):
    print(len(node.children()))
    #hash own value and store
    #loop through all children
        #recursively call this function for all child node
    #concatenate its hash and child hashes and hash again
def recursive_postordertraversal(node,level):
    #hash own value and store
    node.self_hash = hashlib.md5(node.__class__.__name__.encode('utf-8')).hexdigest()
    #print(node.__class__.__name__,node.self_hash)
    node.recur_hash = node.self_hash
    for n in node.children():
        return_info = recursive_postordertraversal(n[1],level+1)
        node.recur_hash += return_info.return_hash
        node.weight += return_info.return_weight
    node.recur_hash = hashlib.md5(node.recur_hash.encode('utf-8')).hexdigest()
    #print("recur_hash : ", node.recur_hash," weight : ", node.weight)
    return ReturnInfo(node.recur_hash,node.weight)    
#------------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) > 1:
        translate_to_c(sys.argv[1]) #read from argument in run->configuration per file->command line options
    else:
        print("Please provide a filename as argument")
