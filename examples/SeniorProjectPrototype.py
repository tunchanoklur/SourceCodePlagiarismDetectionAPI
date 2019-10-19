#----Senior Project Prototype---------
from __future__ import print_function
import sys
import hashlib
import numpy as np
import pandas
import re
import os
sys.path.extend(['.', '..'])

from pycparser import c_parser, c_ast, c_generator

directory = 'C:/Users/hitsu/Desktop/senior project/Prototype'
#directory = 'C:/Users/hitsu/Desktop/senior project/Code'
#directory = directory + '/Lab 1'
class FileInfo:
    def __init__(self, name, data, ast = None):
        self.name = name
        self.data = data
        self.ast = ast
        
class ReturnInfo:
    def __init__(self, return_hash, return_weight = 0):
        self.return_hash = return_hash
        self.return_weight = return_weight
        
class DictInfo:
    def __init__(self, times = 0, adj_list = [],weight = 0):
        self.adj_list = adj_list
        self.times = times
        self.weight = weight
        
def removeComments(text):
    """ remove c-style comments.
        text: blob of text with comments (can include newlines)
        returns: text with comments removed
    """
    pattern = r"""
                            ##  --------- COMMENT ---------
           //.*?$           ##  Start of // .... comment
         |                  ##
           /\*              ##  Start of /* ... */ comment
           [^*]*\*+         ##  Non-* followed by 1-or-more *'s
           (                ##
             [^/*][^*]*\*+  ##
           )*               ##  0-or-more things which don't start with /
                            ##    but do end with '*'
           /                ##  End of /* ... */ comment
         |                  ##  -OR-  various things which aren't comments:
           (                ##
                            ##  ------ " ... " STRING ------
             "              ##  Start of " ... " string
             (              ##
               \\.          ##  Escaped char
             |              ##  -OR-
               [^"\\]       ##  Non "\ characters
             )*             ##
             "              ##  End of " ... " string
           |                ##  -OR-
                            ##
                            ##  ------ ' ... ' STRING ------
             '              ##  Start of ' ... ' string
             (              ##
               \\.          ##  Escaped char
             |              ##  -OR-
               [^'\\]       ##  Non '\ characters
             )*             ##
             '              ##  End of ' ... ' string
           |                ##  -OR-
                            ##
                            ##  ------ ANYTHING ELSE -------
             .              ##  Anything other char
             [^/"'\\]*      ##  Chars which doesn't start a comment, string
           )                ##    or escape
    """
    regex = re.compile(pattern, re.VERBOSE|re.MULTILINE|re.DOTALL)
    noncomments = [m.group(2) for m in regex.finditer(text) if m.group(2)]

    return "".join(noncomments)

def commentRemover(text):
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return " " # note: a space and not an empty string
        else:
            return s
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, replacer, text)

def file_reader():
    filelist = []
    for filename in os.listdir(directory):
        if filename.endswith(".c"):
            path = (directory + '/' + filename)
            file = open(path,'r')
            file_data = commentRemover(file.read())
            file_data = remove_preprocessor_directive(file_data)
            filelist.append(FileInfo(filename,file_data))
    return filelist

def remove_preprocessor_directive(code):
    preprocessor_directive=['#include','#define','#undef','#ifdef','#ifndef','#if','#else','#elif','#endif','#error','#pragma']
    codelist = code.split('\n')
    codelist = [line for line in codelist if not any(re.findall(r'|'.join(preprocessor_directive), line, re.IGNORECASE))]
    code = '\n'.join(codelist)
    return code

def print_tab(times):
    for i in range(times):
        print('\t', end = '')

def recursive_postordertraversal(node,level):
    #hash own value and store
    #print_tab(level)
    node.self_hash = hashlib.md5(node.__class__.__name__.encode('utf-8')).hexdigest()
    #print(node.__class__.__name__,node.self_hash)
    node.recur_hash = node.self_hash
    for n in node.children():
        return_info = recursive_postordertraversal(n[1],level+1)
        node.recur_hash += return_info.return_hash
        node.weight += return_info.return_weight
    #print_tab(level)
    node.recur_hash = hashlib.md5(node.recur_hash.encode('utf-8')).hexdigest()
    #print("recur_hash : ", node.recur_hash," weight : ", node.weight)
    return ReturnInfo(node.recur_hash,node.weight)

def compare_bfs(ast1,ast2):
    similar_node = 0
    tree1 = ast1
    tree2 = ast2
    for node2 in list(tree2):
        if node2 in list(tree1):
            if tree1[node2].weight == tree2[node2].weight:
                #print("DUPLICATE NODE : ", node2)
                similar_node = recur_dic(node2,tree1,similar_node)
                #print("CURRENT SIM: ",similar_node)
    return similar_node

def recur_dic(node,dic,similar=0):
    if node in list(dic):
        similar +=dic[node].times
        #print("add weight for node ",node, "  similar: ", similar)
        for other in dic[node].adj_list:
            similar = recur_dic(other, dic, similar)
        del dic[node]
    return similar
    
def bfs(bfs_queue,node_no):
    if len(bfs_queue)!=0:
        tmp = bfs_queue.pop(0)
        #print(tmp.__class__.__name__,node_no,matched[node_no])
        for n in tmp.children():
            bfs_queue.append(n[1])
        bfs(bfs_queue,node_no+1)

def generate_dic(ast):
    dic = {}
    bfs_queue = [ast]
    while len(bfs_queue) != 0:
        tmp = bfs_queue.pop(0)
        if tmp.recur_hash not in dic:
            dic[tmp.recur_hash] = DictInfo(1,[],tmp.weight)
        else:
            dic[tmp.recur_hash].times += 1
        for n in tmp.children():
            bfs_queue.append(n[1])
            dic[tmp.recur_hash].adj_list.append(n[1].recur_hash)
        
    return dic
def print_dic(ast_dictionary):
    for dic in ast_dictionary:
       print(dic)
       if isinstance(ast_dictionary[dic], list):
           for data in ast_dictionary[dic]:
               print("\t",data)
       else:
           print("\t",ast_dictionary[dic])
#main function
parser = c_parser.CParser()
generator = c_generator.CGenerator()

ast_dictionary = []
filelist = file_reader()
for file in filelist:
    print(file.name)
    file.ast = parser.parse(file.data, filename=file.name)
    recursive_postordertraversal(file.ast,0)
    ast_dictionary.append(generate_dic(file.ast))
#print("COMPARE ",filelist[0].name," with ",filelist[6].name)
#print("SIMILAR NODE: ",compare_bfs(ast_dictionary[0],ast_dictionary[6]))

total_file = len(filelist)
print("Retrieved File: ",total_file)
result_matrix = np.zeros((total_file, total_file))

for i in range(total_file):
    tree1 = filelist[i]
    for j in range(total_file):
        tmp_dic1 = ast_dictionary[i].copy()
        tmp_dic2 = ast_dictionary[j].copy()
        #print(filelist[i].name,filelist[j].name,compare_bfs(tmp_dic1,tmp_dic2),"/",tree1.ast.weight)
        result_matrix[i,j] = (compare_bfs(tmp_dic1,tmp_dic2)/tree1.ast.weight)*100
        result_matrix[i,j] = round(result_matrix[i,j], 2)
        #print("Compare ",tree1.name, " with ", filelist[j].name, " got ", result_matrix[i,j],"% similarity ")
        
for i in range(total_file):
    name1 = filelist[i].name
    #print(name1,"\t",end = '')
    for j in range(total_file):
        tmp = round((result_matrix[i,j] + result_matrix[j,i])/2, 2)
        result_matrix[i,j] = tmp
        result_matrix[j,i] = tmp
        #print(result_matrix[i,j],"\t",end = '')
        if i>j:
            result_matrix[i,j] = None
    #print("")
    
result_df = pandas.DataFrame(result_matrix, [file.name for file in filelist], [file.name for file in filelist])
result_df.fillna("", inplace = True) 
result_df.to_csv(directory+'/evaluation_result.csv', index = True, header=True)
print(result_df.to_string())

#bfs_queue_ast1 = [filelist[0].ast]
#print(filelist[0].name)
filelist[7].ast.show(showcoord=True)
#bfs_queue_ast2 = [filelist[2].ast]
#print(filelist[1].name)
print("-------------------------")
filelist[8].ast.show(showcoord=True)

#print("Total matched node:",compare_bfs(filelist[0].ast,filelist[2].ast))

#bfs_queue = [filelist[3].ast]
#print(filelist[3].name)
#filelist[0].ast.show(showcoord=True)
#filelist[2].ast.show(showcoord=True)
#print("-----------------------------------------------------")
#bfs(bfs_queue,0)
#print("--------------------------------------------------------------------------------------")
#bfs_queue = [filelist[4].ast]
#print(filelist[4].name)
#filelist[4].ast.show(showcoord=True)
#print("-----------------------------------------------------")
#bfs(bfs_queue,0)
#ast.show(showcoord=True)
