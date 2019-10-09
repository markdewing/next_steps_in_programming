#!/usr/local/bin/python 
import sys
from xml.dom import minidom, Node

# helper functions for reading/writing XML and MathML

# Copyright 2005 by Mark Dewing
# Version 0.01

# tree walking and node helper functions

def walkTree(node):
  if node.nodeType == Node.ELEMENT_NODE:
    yield node
    for child in node.childNodes:
      for n1 in walkTree(child):
        yield n1

def findElement(n,name):
  for node in walkTree(n):
    if node.nodeType == Node.ELEMENT_NODE:
      if node.nodeName == name:
        yield node

def iterateElementNodes(node_list):
  for n1 in node_list:
    if is_element_node(n1):
      yield n1

# get length of list defined by a generator
def get_len(list):
   idx = 0
   for n1 in list:
      idx += 1
   return idx

def getElementNode(node_list,index):
   idx = 0
   for n1 in iterateElementNodes(node_list):
     if (idx == index):
        return n1
     idx += 1
   return None
 

def showNode(node):
  if node.nodeType == Node.ELEMENT_NODE:
    print 'Element name: %s' % node.nodeName
  if node.nodeType == Node.TEXT_NODE:
    print 'Text name: %s' %  node.nodeValue

def is_element_node(node):
  if (node and node.nodeType == Node.ELEMENT_NODE):
     return 1
  else:
     return 0

def is_node_name(node,name):
   if is_element_node(node) and (node.nodeName == name):
     return 1
   else:
     return 0

# node creation helper functions
def createChildElement(doc,node,name):
  new_node = doc.createElement(name)
  node.appendChild(new_node)
  return new_node

def createTextElement(doc,name,text):
  new_node = doc.createElement(name)
  new_text = doc.createTextNode(text)
  new_node.appendChild(new_text)
  return new_node

def createChildTextElement(doc,node,name,text):
  new_node = createTextElement(doc,name,text)
  node.appendChild(new_node)
  return new_node

# math ml helper functions

def get_func_name(node):
  for n1 in node.childNodes:
    if is_node_name(n1,"ci"):
       return n1.childNodes[0].nodeValue

def get_lambda_node(node):
  for n1 in node.childNodes:
    if is_node_name(n1,"lambda"):
       return n1

def get_expr_node(node):
  for n1 in node.childNodes:
    if is_element_node(n1) and not(is_node_name(n1,"bvar")):
       return n1

def get_arg_list(node):
  for n1 in node.childNodes:
    if is_node_name(n1,"bvar"):
      for n2 in n1.childNodes:
        if is_node_name(n2,"ci"): 
          yield n2.childNodes[0].nodeValue

def get_apply_node(node):
  #print node.nodeName
  if not(is_node_name(node,"apply")):
     return 
  for n1 in node.childNodes: 
    if is_element_node(n1):
      return n1

def get_apply_op(node):
  return get_apply_node(node).nodeName

def get_apply_op_value(node):
  return get_apply_node(node).childNodes[0].nodeValue

def get_limit_nodes(node):
   for n1 in node.childNodes:
      if is_element_node(n1) and is_node_name(n1,"bvar"):
        bvar_node = n1
      if is_element_node(n1) and is_node_name(n1,"lowlimit"):
        lower_node = n1
      if is_element_node(n1) and is_node_name(n1,"uplimit"):
        up_node = n1
   return (bvar_node,lower_node,up_node)
      

