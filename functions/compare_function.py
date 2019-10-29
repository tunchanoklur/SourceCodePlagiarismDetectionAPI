#----Senior Project Prototype---------
from __future__ import print_function
import sys
import hashlib
import numpy as np
import pandas
import re
import os
from io import StringIO
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
            return " "
        else:
            return s
    pattern = re.compile(
        r'#include.*?$|#define.*?$|#undef.*?$|#ifdef.*?$|#ifndef.*?$|#if.*?$|#else.*?$|#elif.*?$|#endif.*?$|#error.*?$|#pragma.*?$|//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, replacer, text)

def file_reader(data):
    filelist = []
    for datafile in data:
        file_data = commentRemover(datafile['fileinfo'])
        print(file_data)
        filelist.append(FileInfo(datafile['filename'],file_data.replace('\r\n','\n')))
    return filelist

def categorize_binop(operator):
    if operator in ['*','%','/']:
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
    if node.__class__.__name__ is "BinaryOp":
        if node.op is not None:
            node.self_hash = hashlib.md5(categorize_binop(node.op).encode('utf-8')).hexdigest()
    else:
        node.self_hash = hashlib.md5(node.__class__.__name__.encode('utf-8')).hexdigest()
    node.recur_hash = node.self_hash
    for n in node.children():
        return_info = recursive_postordertraversal(n[1],level+1)
        node.recur_hash += return_info.return_hash
        node.weight += return_info.return_weight
    node.recur_hash = hashlib.md5(node.recur_hash.encode('utf-8')).hexdigest()
    return ReturnInfo(node.recur_hash,node.weight)

def compare_bfs(ast1,ast2,loc_list):
    similar_node = 0
    tree1 = ast1
    tree2 = ast2
    for node2_tuple in sorted(tree2.items(), key = lambda x: x[1].weight, reverse=True):
        node2 = node2_tuple[0]
        if node2 in tree1:
            if tree1[node2].weight == tree2[node2].weight:
                similar_node += recur_dic(node2,tree1,tree2,similar_node,loc_list,"first")
    return similar_node

def recur_dic(node,dic1,dic2,similar=0,loc_list=[],times="others"):
    if node in list(dic1):
        similar += dic1[node].times
        tmp = dic1[node]
        if tmp.loc is not None and dic2[node].loc is not None:
            loc_tuple = (tmp.loc,dic2[node].loc)
            if loc_tuple not in loc_list:
                loc_list.append(loc_tuple)
        for other in dic1[node].adj_list:
            similar = recur_dic(other, dic1, dic2, similar,loc_list)
        del dic1[node]
    if times == "first":
        return tmp.weight*tmp.times
    else:
        return similar

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
    return dic

def getsimscore(data_in):
    parser = c_parser.CParser()
    
    ast_dictionary = []
    filelist = file_reader(data_in)
    for file in filelist:
        file.ast = parser.parse(file.data, filename=file.name)
        recursive_postordertraversal(file.ast,0)
        ast_dictionary.append(generate_dic(file.ast))
    
    total_file = len(filelist)
    result_matrix = np.zeros((total_file, total_file))
    loc_matrix = np.empty((total_file, total_file),dtype=object)
    
    for i in range(total_file):
        tree1 =  filelist[i]
        for j in range(i+1,total_file):
            tmp_dic1 = [ast_dictionary[i].copy(),ast_dictionary[i].copy()]
            tmp_dic2 = [ast_dictionary[j].copy(),ast_dictionary[j].copy()]
            loc_matrix[i,j] = []
            loc_matrix[j,i] = []
            for k in range(2):
                if k==0:
                    result_matrix[i,j] += (compare_bfs(tmp_dic1[k],tmp_dic2[k],loc_matrix[i,j])/tree1.ast.weight)
                else:
                    result_matrix[i,j] += (compare_bfs(tmp_dic2[k],tmp_dic1[k],loc_matrix[j,i])/filelist[j].ast.weight)
            result_matrix[i,j] = round(result_matrix[i,j]*100*(1/2), 2)
    for i in range(total_file):
        for j in range(i+1):
            if i==j:
                result_matrix[i,j]=100
            else:
                result_matrix[i,j]=1000

    return {
        "score": result_matrix.tolist(),
        "loc": loc_matrix.tolist(),
        "filelist_name": [file.name for file in filelist],
        "filelist_data": [file.data for file in filelist]
    }

def getsimscore_CSV(data_in):
    parser = c_parser.CParser()
    
    ast_dictionary = []
    filelist = file_reader(data_in)
    for file in filelist:
        file.ast = parser.parse(file.data, filename=file.name)
        recursive_postordertraversal(file.ast,0)
        ast_dictionary.append(generate_dic(file.ast))
    
    total_file = len(filelist)
    result_matrix = np.zeros((total_file, total_file))
    loc_matrix = np.empty((total_file, total_file),dtype=object)
    
    for i in range(total_file):
        tree1 =  filelist[i]
        for j in range(i+1,total_file):
            tmp_dic1 = [ast_dictionary[i].copy(),ast_dictionary[i].copy()]
            tmp_dic2 = [ast_dictionary[j].copy(),ast_dictionary[j].copy()]
            loc_matrix[i,j] = []
            loc_matrix[j,i] = []
            for k in range(2):
                if k==0:
                    result_matrix[i,j] += (compare_bfs(tmp_dic1[k],tmp_dic2[k],loc_matrix[i,j])/tree1.ast.weight)
                else:
                    result_matrix[i,j] += (compare_bfs(tmp_dic2[k],tmp_dic1[k],loc_matrix[j,i])/filelist[j].ast.weight)
            result_matrix[i,j] = round(result_matrix[i,j]*100*(1/2), 2)
    for i in range(total_file):
        for j in range(i+1):
            if i==j:
                result_matrix[i,j]=100
            else:
                result_matrix[i,j]=None
                
    result_df = pandas.DataFrame(result_matrix, [file.name for file in filelist], [file.name for file in filelist])
    result_df.fillna("", inplace = True)
    stream = StringIO()
    result_df.to_csv(stream, index = True, header=True)
    
    return stream.getvalue()