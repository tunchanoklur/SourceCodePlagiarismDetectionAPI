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
    def __init__(self, times = 0, adj_list = [],weight = 0, loc = None):
        self.adj_list = adj_list
        self.times = times
        self.weight = weight
        if loc is None:
            self.loc = loc
        else:
            self.loc = [loc]

def commentRemover(text):
    def replacer(match):
        s = match.group(0)
        if s.startswith('/') or s.startswith('#'):
            return " " # note: a space and not an empty string
        else:
            return s
    pattern = re.compile(
        r'#include.*?$|#define.*?$|#undef.*?$|#ifdef.*?$|#ifndef.*?$|#if.*?$|#else.*?$|#elif.*?$|#endif.*?$|#error.*?$|#pragma.*?$|//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, replacer, text)

def file_reader(directory):
    filelist = []
    for filename in os.listdir(directory):
        if filename.endswith(".c"):
            path = (directory + '/' + filename)
            file = open(path,'r')
            #file = open(path,'r',encoding='unicode_escape')
            file_data = commentRemover(file.read())
            #file_data = remove_preprocessor_directive(file_data)
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

def categorize_binop(operator):
    if operator in ['*','%','/']: #multiplicative operators
        return "multiplicative"
    if operator in ['+','-']:
        return "additive"
    if operator in ['<<','>>']:
        return "shift"
    if operator in ['<','<=','>','>=']:
        return "relational"
    if operator in ['==','!=']:
        return "equality"
    if operator in ['&','|','^']:
        return "bitwise"
    if operator in ['&&','||']:
        return "logical"
    return "BinaryOp"
    
def recursive_postordertraversal(node,level):
    #hash own value and store
    #print_tab(level)
    if node.__class__.__name__ is "BinaryOp":
        if node.op is not None:
            node.self_hash = hashlib.md5(categorize_binop(node.op).encode('utf-8')).hexdigest()
            #print("BinaryOp",categorize_binop(node.op),node.op,node.self_hash)
    else:
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

def compare_bfs(ast1,ast2,loc_list):
    similar_node = 0
    tree1 = ast1
    tree2 = ast2
    for node2_tuple in sorted(tree2.items(), key = lambda x: x[1].weight, reverse=True):
        node2 = node2_tuple[0]
        #print(node2, node2_tuple[1].weight)
        if node2 in list(tree1):
            if tree1[node2].weight == tree2[node2].weight:
                #print("DUPLICATE NODE : ", node2,tree1[node2].weight,tree1[node2].times)
                similar_node += recur_dic(node2,tree1,tree2,similar_node,loc_list,"first")
                #print("CURRENT SIM: ",similar_node)
    return similar_node

def recur_dic(node,dic1,dic2,similar=0,loc_list=[],times="others"):
    if node in list(dic1):
        similar += dic1[node].times
        tmp = dic1[node]
        if tmp.loc is not None and dic2[node].loc is not None:
            loc_tuple = (tmp.loc,dic2[node].loc)
            if loc_tuple not in loc_list:
                loc_list.append(loc_tuple)
        #print("add weight for node ",node, "  similar: ", similar)
        for other in dic1[node].adj_list:
            similar = recur_dic(other, dic1, dic2, similar,loc_list)
        del dic1[node]
    if times == "first":
        return tmp.weight*tmp.times
    else:
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
            if tmp.coord is not None:
                dic[tmp.recur_hash] = DictInfo(1,[],tmp.weight,tmp.coord.line)
            else:
                dic[tmp.recur_hash] = DictInfo(1,[],tmp.weight)
        else:
            dic[tmp.recur_hash].times += 1
            if tmp.coord is not None:
                if dic[tmp.recur_hash].loc is not None and tmp.coord.line not in dic[tmp.recur_hash].loc:
                    dic[tmp.recur_hash].loc.append(tmp.coord.line)
                else:
                    dic[tmp.recur_hash].loc = [tmp.coord.line]
        for n in tmp.children():
            if n[1].__class__.__name__ not in ["IdentifierType","TypeDecl","Decl","ID","Constant"]:
                bfs_queue.append(n[1])
                dic[tmp.recur_hash].adj_list.append(n[1].recur_hash)
    #print(dic)
    #ast.show(showcoord=True)
    #print_dic(dic)
    return dic

def print_dic(ast_dictionary):
    for dic in ast_dictionary:
       print(dic,"\t", ast_dictionary[dic].weight)
       if isinstance(ast_dictionary[dic], list):
           for data in ast_dictionary[dic]:
               print("\t",data)
       else:
           print("\t",ast_dictionary[dic])

#main function
def getsimscore(directory):
    parser = c_parser.CParser()
    
    ast_dictionary = []
    filelist = file_reader(directory)
    for file in filelist:
        #print(file.name)
        file.ast = parser.parse(file.data, filename=file.name)
        recursive_postordertraversal(file.ast,0)
        ast_dictionary.append(generate_dic(file.ast))
    #print("COMPARE ",filelist[0].name," with ",filelist[6].name)
    #print("SIMILAR NODE: ",compare_bfs(ast_dictionary[0],ast_dictionary[6]))
    
    total_file = len(filelist)
    #print("Retrieved File: ",total_file)
    result_matrix = np.zeros((total_file, total_file))
    loc_matrix = np.empty((total_file, total_file),dtype=object)
    
    for i in range(total_file):
        tree1 = filelist[i]
        for j in range(total_file):
            tmp_dic1 = ast_dictionary[i].copy()
            tmp_dic2 = ast_dictionary[j].copy()
            #print(filelist[i].name,filelist[j].name,compare_bfs(tmp_dic1,tmp_dic2),"/",tree1.ast.weight)
            #print(filelist[i].name,filelist[j].name)
            #filelist[i].ast.show(showcoord=True)
            #filelist[j].ast.show(showcoord=True)
            loc_matrix[i,j] = []
            result_matrix[i,j] = (compare_bfs(tmp_dic1,tmp_dic2,loc_matrix[i,j])/tree1.ast.weight)*100
            result_matrix[i,j] = round(result_matrix[i,j], 2)
            #loc_matrix[i,j].sort()
            #print("Compare ",tree1.name, " with ", filelist[j].name, " got ", result_matrix[i,j],"% similarity ")
            #print(tree1.name,filelist[j].name)
            #filelist[i].ast.show(showcoord=True)
            #filelist[j].ast.show(showcoord=True)
            #print(loc_matrix[i,j])
            #input("Press Enter to continue...")
        
    for i in range(total_file):
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
    result_df.to_csv(directory+'/_evaluation_result.csv', index = True, header=True)
    #print(result_df.to_string())
    
    loc_df = pandas.DataFrame(loc_matrix, [file.name for file in filelist], [file.name for file in filelist])
    loc_df.fillna("", inplace = True) 
    loc_df.to_csv(directory+'/_loc_result.csv', index = True, header=True)
    #print(loc_df.to_string())


## loop through directory
    
directory = 'C:/Users/hitsu/Desktop/senior project/'
sub_dir = ['Prototype']
    
#directory = 'C:/Users/hitsu/Desktop/senior project/Code/'
#sub_dir = ['Homework Week 3_2_Adding two weights','Lab','Lab Assignment','LAB Function','Lab Week 12_ Structure','Lab week3','Pointer Labs','Project','Week 6Lab using Loop','Week 8_ String','Week4','Week5_ ครม หรม','Week11_ BlackJack']
#sub_dir = ['Lab 1']
    
#directory = 'C:/Users/hitsu/Desktop/senior project/CodeAjAui/'
#sub_dir = ['Age','Average','Average Score','Calculation','Circle','Count with Condition','DateTime','EGCO','Leap Year','Min-Max','Min-Max of N numbers','Multiplication','My Lovely Rat','Nested Loop','Numbers','Odd or Even','Prime Number','Repeated Odd _ Even Numbers','Shipping','Simple Calculator','Sum','Temperature Conversion','The Circle','Time']
#sub_dir = ['Add Matrix','ATM','Balloon','Fat','Find A Number','Number To Text']
import time
start_time = time.time()
for subdir in sub_dir:
    print(directory+subdir)
    getsimscore(directory+subdir)
    print("DONE")
print("--- %s seconds ---" % (time.time() - start_time))