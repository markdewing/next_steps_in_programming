#!/usr/local/bin/python
import sys
from types import *

# Tree and output functions for C++

# Copyright 2005 by Mark Dewing
# Version 0.01

c_indent_level = 0
in_for_args = 0

def change_indent_level(change):
  global c_indent_level
  c_indent_level += change 

def get_indent_string():
  global c_indent_level
  out = ""
  for i in range(0,c_indent_level):
    out += "    " 
  return out



class c_for:
  def __init__(self,start=None,end=None,incr=None):
    self.start = start
    self.end = end
    self.incr = incr
    self.body = []
  def get_string(self):
    global in_for_args
    in_for_args = 1
    out = get_indent_string() + "for ("
    if (self.start):
      out += self.start.get_string()
    out += ";"
    if (self.end):
      out += self.end.get_string() 
    out += ";"
    if (self.incr):
      out += self.incr.get_string() 
    out += ") {\n"
    in_for_args = 0
    change_indent_level(1)
    for expr in self.body:
      out += expr.get_string()
    change_indent_level(-1)
    out += get_indent_string() + "}\n"
    return out

class c_var:
  def __init__(self,name):
    self.name = name
  def get_string(self,need_paren=0):
    return self.name
    

class c_expr:
  C_OP_PLUS      = 1
  C_OP_MINUS     = 2
  C_OP_TIMES     = 3
  C_OP_DIVIDE    = 4
  C_OP_POST_INCR = 5
  C_OP_LE = 6
  def __init__(self,op,arg1=None,arg2=None,arg3=None):
    self.op = op
    self.arg1 = arg1
    self.arg2 = arg2
    self.arg3 = arg3
  def get_string(self,need_paren=0):
    out = ""
    arg1_str = ''

    might_need_paren = 0
    if (self.op == c_expr.C_OP_TIMES or 
        self.op == c_expr.C_OP_DIVIDE):
      might_need_paren = 1
    if (self.arg1):
      arg1_str = self.arg1.get_string(might_need_paren)
    arg2_str = ''
    if self.arg2:
       arg2_str = self.arg2.get_string(might_need_paren)

    if need_paren:
      out += '('
    if self.op == c_expr.C_OP_PLUS:
      out += arg1_str + ' + ' + arg2_str
    if self.op == c_expr.C_OP_MINUS:
      out += arg1_str + ' - ' + arg2_str
    elif self.op == c_expr.C_OP_TIMES:
      out += arg1_str + ' * ' + arg2_str
    elif self.op == c_expr.C_OP_DIVIDE:
      out += arg1_str + ' / ' + arg2_str
    elif self.op == c_expr.C_OP_POST_INCR:
      out += arg1_str + '++'
    elif self.op == c_expr.C_OP_LE:
      out += arg1_str + ' <= ' + arg2_str
    if need_paren:
      out += ')'
    
    return out

class c_return_stmt:
  def __init__(self,arg=None):
    self.arg = arg
  def get_string(self):
    out = get_indent_string()
    out += "return"
    if self.arg:
      out += ' ' + self.arg.get_string() 
    out += ";\n"
    return out
 


class c_assign_stmt:
  C_ASSIGN_EQUAL = 1
  C_ASSIGN_PLUS = 2
  def __init__(self,lhs=None,rhs=None,op=C_ASSIGN_EQUAL):
    self.lhs = lhs
    self.rhs = rhs
    self.op = op
  def get_string(self):
    global in_for_args
    out = ""
    if not(in_for_args):
      out += get_indent_string()
    if (self.lhs):
       out += self.lhs.get_string() 
       if self.op == c_assign_stmt.C_ASSIGN_EQUAL:
          out += " = "
       if self.op == c_assign_stmt.C_ASSIGN_PLUS:
          out += " += "
    out += self.rhs.get_string()
    if not(in_for_args):
      out += ";\n"
    return out

class c_arg:
  def __init__(self,arg_type,arg_name):
    self.arg_type = arg_type
    self.arg_name = arg_name
  def get_string(self):
    out = self.arg_type + " "
    try:
      out += self.arg_name.get_string()
    except AttributeError:
      out += self.arg_name
    return out

class c_decl(c_arg):
  def __init__(self,arg_type,arg_name,initializer=None):
    c_arg.__init__(self,arg_type,arg_name)
    self.init = initializer
  def get_string(self):
    out = get_indent_string() + c_arg.get_string(self) 
    if self.init:
       out += " = " + self.init.get_string()
    out += ";\n"
    return out

class c_function_call:
  def __init__(self,name):
    self.name = name
    self.arglist = []
  def get_string(self,need_paren=0):
    out = self.name + '('
    idx = len(self.arglist)
    for arg in self.arglist:
      out += arg.get_string()
      if (idx > 1):
        out += ','
      idx -= 1
    out += ')'
    return out
     

class c_function_def:
  def __init__(self,name):
    self.name = name
    self.arglist = []
    self.return_type = ""
    self.expr_list = []
  def __init__(self,return_type,name):
    self.name = name
    self.arglist = []
    self.return_type = return_type
    self.expr_list = []
  def get_string(self):
    out = self.return_type + " "
    out +=  self.name + "("
    idx = len(self.arglist)
    for arg in self.arglist:
       out += arg.get_string()
       if (idx > 1):
         out += ","
       idx -= 1
    out += "){\n"
    change_indent_level(1)
    for expr in self.expr_list:
      if expr:
        out += expr.get_string() 
    out += "}"
    change_indent_level(-1)
    return out


def main():

  c_tree1 = c_function_def("double","g")

  c_arg_g1 = c_arg("double","i")
  c_tree1.arglist.append(c_arg_g1)

  c_ret = c_return_stmt(c_expr(c_expr.C_OP_PLUS,c_var("i"),c_var("2")))
  c_tree1.expr_list.append(c_ret)

 
  c_tree = c_function_def("int","testing")

  c_arg1 = c_arg("int","a")
  c_arg2 = c_arg("double","b")


  c_tree.arglist.append(c_arg1)
  c_tree.arglist.append(c_arg2)

  c_decl1 = c_decl("double","sum")
  c_tree.expr_list.append(c_decl1)
  c_decl2 = c_decl("int","i")
  c_tree.expr_list.append(c_decl2)

 
  for_start = c_assign_stmt(c_var("i"),c_var("0"))
  for_end = c_expr(c_expr.C_OP_LE,c_var("i"),c_var("100"))
  for_inc = c_expr(c_expr.C_OP_POST_INCR,c_var("i"))
  c_for1 = c_for(for_start,for_end,for_inc)
  c_tree.expr_list.append(c_for1)

  g_func = c_function_call("g")
  g_func.arglist.append(c_var("i"))
  g_func.arglist.append(c_var("x"))
  for_body1 = c_assign_stmt(c_var("sum"),g_func,c_assign_stmt.C_ASSIGN_PLUS)
  c_for1.body.append(for_body1)

  print c_tree1.get_string()
  print c_tree.get_string()


if __name__ == '__main__':
  main()
