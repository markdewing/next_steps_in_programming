#!/usr/local/bin/python 

import sys
from xml.dom import minidom, Node
from mathml import *
from lang_c import *
import re

# Copyright 2005 by Mark Dewing
# Version 0.01

# Converts content MathML to various forms
#  1. Text (somewhat TeX-like) 
#  2. Presentation MathML
#  3. C++


# Input is file.xml, presentation MathML is in file.xhtml
#  C++ is in file.cpp


# The functions handle_expr and handle_declare output the text format
# The functions handle_expr_ml and handle_declare_ml output the presentation
#  MathML
# The functions handle_expr_cpp2 and handle_declare_cpp2 output C++
# (those with the _cpp suffix were an earlier version that output C++ 
#  source directly.)

func_list = {}

# transformation functions

def handle_expr(node,need_paren=0):
  out_str = ""
  skip = 1
  nterm = 0
  need_term = 0
  might_need_paren = 0
  if is_node_name(node,"apply"):
    op = get_apply_op(node)
    if (op == "plus"): 
       op_str = "+"
       need_term = 1
    if (op == "minus"): 
       op_str = "-"
       need_term = 1
    if (op == "times"): 
       op_str = "*"
       might_need_paren = 1
    if (op == "divide"): 
       op_str = "/"
       might_need_paren = 1
    if (op == "power"): 
       op_str = "^"
       might_need_paren = 1
    if (op == "sum"): 
       skip = 7
       out_str += "sum"
       (bvar,low_limit,up_limit) = get_limit_nodes(node)
       out_str += "_{" + handle_expr(bvar.childNodes[0])[0]
       out_str += "=" + handle_expr(low_limit.childNodes[0])[0]
       out_str += "}^"
       for n2 in up_limit.childNodes:
         if is_element_node(n2):
           (tmp_str,nt) = handle_expr(n2)
           if (nt > 1):
              out_str += "{" + tmp_str + "}"
           else:
             out_str += tmp_str
         
       out_str += " "
    if (op == "ci"): 
       func_name = get_apply_op_value(node)
       out_str += func_name + "("
       skip = len(node.childNodes)
       tmp_str = ""
       for n2 in node.childNodes[2:]:
         if is_element_node(n2): 
           if (tmp_str):
             out_str += tmp_str
             out_str += ","
           tmp_str = handle_expr(n2)[0]
       out_str += tmp_str + ")"
   
    next_str = ""
    if (need_paren):
      out_str += "("
    for n1 in node.childNodes[skip:]:
      if is_element_node(n1): 
         if need_term:
           nterm+=1
         if (next_str != ""):
           out_str += next_str
           out_str += op_str
         next_str = handle_expr(n1,might_need_paren)[0]
    out_str += next_str
    if (need_paren):
      out_str += ")"
    return (out_str,nterm)
  if is_node_name(node,"ci"):
    return  (node.childNodes[0].nodeValue,0)
  if is_node_name(node,"cn"):
    return  (node.childNodes[0].nodeValue,0)
     
  return ""

def handle_expr_cpp(node):
  out_str = ""
  skip = 1
  if is_node_name(node,"apply"):
    op = get_apply_op(node)
    if (op == "plus"): 
       op_str = "+"
    if (op == "minus"): 
       op_str = "-"
    if (op == "times"): 
       op_str = "*"
    if (op == "divide"): 
       op_str = "/"
    if (op == "power"): 
       op_str = "^"
    if (op == "sum"): 
       skip = 7
       #out_str += "sum"
       out_str += "double sum;\n"
       (bvar,low_limit,up_limit) = get_limit_nodes(node)
       bvar_str = handle_expr_cpp(bvar.childNodes[0])
       low_str = handle_expr_cpp(low_limit.childNodes[0])
       up_str = handle_expr_cpp(up_limit.childNodes[1])
       out_str += "int " + bvar_str + ";\n"
       out_str += "for (" + bvar_str + " = " + low_str + ";"
       out_str += bvar_str + "<=" + up_str + ";" 
       out_str += bvar_str + "++) {\n"
       out_str += "sum += "
      

       #out_str += "_{" + handle_expr(bvar.childNodes[0]) 
       #out_str += "=" + handle_expr(low_limit.childNodes[0])
       #out_str += "}^" + handle_expr(up_limit.childNodes[0])
       #out_str += " "
   
    next_str = ""
    for n1 in node.childNodes[skip:]:
      if is_element_node(n1): 
         if (next_str != ""):
           out_str += next_str
           out_str += op_str
         next_str = handle_expr_cpp(n1)[0]
    out_str += next_str
    if (op == "sum"):
       out_str += ";\n}\n return sum;"
       
    return (out_str,op)
  if is_node_name(node,"ci"):
    return  node.childNodes[0].nodeValue
  if is_node_name(node,"cn"):
    return  node.childNodes[0].nodeValue
     
  return ""


def handle_expr_cpp2(node):
  if is_node_name(node,"apply"):
    op = get_apply_op(node)
    op_type = None
    if (op == "plus"): 
      op_type = c_expr.C_OP_PLUS
    if (op == "minus"): 
      op_type = c_expr.C_OP_MINUS
    if (op == "times"): 
      op_type = c_expr.C_OP_TIMES
    if (op == "divide"): 
      op_type = c_expr.C_OP_DIVIDE
    if (op == "power"):
      pow_body = []
      n1 = getElementNode(node.childNodes,1)
      (pow_body1,pow_ret1) = handle_expr_cpp2(n1)
      n2 = getElementNode(node.childNodes,2)
      (pow_body2,pow_ret2) = handle_expr_cpp2(n2)
      pow_func = c_function_call("pow") 
      if pow_body1:
        for pw1 in pow_body1:
          pow_body.append(pw1)
      if pow_body2:
        for pw2 in pow_body2:
          pow_body.append(pw2)

      pow_func.arglist.append(pow_ret1)
      pow_func.arglist.append(pow_ret2)
      return (pow_body,pow_func)
    if (op == "sum"):
      body_list = []
      tmp_decl = c_decl("double","sum",c_var("0.0"))
      body_list.append(tmp_decl)
      (bvar,low_limit,up_limit) = get_limit_nodes(node)
      bvar_expr = handle_expr_cpp2(bvar.childNodes[0])[1]
      low_expr = handle_expr_cpp2(low_limit.childNodes[0])[1]
      #up_expr = handle_expr_cpp2(up_limit.childNodes[0])[1]
      up_expr = None
      for up1 in up_limit.childNodes:
        if is_element_node(up1):
          up_expr = handle_expr_cpp2(up1)[1]
      bvar_decl = c_decl("int",bvar_expr)
      body_list.append(bvar_decl)
      for_start = c_assign_stmt(bvar_expr,low_expr)
      for_end = c_expr(c_expr.C_OP_LE,bvar_expr,up_expr)
      for_inc = c_expr(c_expr.C_OP_POST_INCR,bvar_expr)
      for_expr = c_for(for_start,for_end,for_inc)

     
      body_list.append(for_expr)
      n3 = getElementNode(node.childNodes,4)
      (body_body,body_ret) = handle_expr_cpp2(n3)

      for_body1 = c_assign_stmt(c_var("sum"),body_ret,c_assign_stmt.C_ASSIGN_PLUS)
      if body_body:
        for b1 in body_body:
          for_expr.body.append(b1)
      for_expr.body.append(for_body1)
      return (body_list,c_var("sum"))
    if (op == "ci"): 
       func_name = get_apply_op_value(node)
       func_call = c_function_call(func_name)
       for arg1 in iterateElementNodes(node.childNodes[2:]):
         (body_arg,ret_arg) = handle_expr_cpp2(arg1)
         func_call.arglist.append(ret_arg)
       return (None,func_call)

    n1 = getElementNode(node.childNodes,1)
    (body,ret) = handle_expr_cpp2(n1)
    n2 = getElementNode(node.childNodes,2)
    (body2,ret2) = handle_expr_cpp2(n2)
    body_list = []
    if body:
      for b1 in body:
        body_list.append(b1)
    if body2:
      for b2 in body2:
        body_list.append(b2)
    return (body_list,c_expr(op_type,ret,ret2))
  if is_node_name(node,"ci"):
    return  (None,c_var(node.childNodes[0].nodeValue))
  if is_node_name(node,"cn"):
    return  (None,c_var(node.childNodes[0].nodeValue))
  return (None,None)

def handle_expr_ml(node,doc,out_node,need_paren=0):
  skip = 1
  might_need_paren = 0
  if is_node_name(node,"apply"):
    op = get_apply_op(node)
    if (op == "plus"): 
       op_str = "+"
    if (op == "minus"): 
       op_str = "-"
    if (op == "times"): 
       op_str = ""
       might_need_paren = 1
    if (op == "divide"): 
       op_str = ""
       might_need_paren = 1
       skip = 5
       frac_node = createChildElement(doc,out_node,"mfrac") 
       num_node = createChildElement(doc,frac_node,"mrow")
       denom_node = createChildElement(doc,frac_node,"mrow")
       node1 = getElementNode(node.childNodes,1)
       node2 = getElementNode(node.childNodes,2)
       handle_expr_ml(node1,doc,num_node,might_need_paren)
       handle_expr_ml(node2,doc,denom_node,might_need_paren)
       might_need_paren = 0
    if (op == "power"):
       op_str = ""
       might_need_paren = 1
       skip = 5
       node1 = getElementNode(node.childNodes,1)
       node2 = getElementNode(node.childNodes,2)
       sup_node = createChildElement(doc,out_node,"msup") 
       handle_expr_ml(node1,doc,sup_node,might_need_paren)
       handle_expr_ml(node2,doc,sup_node,might_need_paren)
       
    if (op == "sum"): 
       op_str = "my_ampersand;Sum;"
       skip = 7
       need_paren = 0
       sum_node = createChildElement(doc,out_node,"munderover")
       createChildTextElement(doc,sum_node,"mo",op_str)
       (bvar,low_limit,up_limit) = get_limit_nodes(node)
       lower_node = createChildElement(doc,sum_node,"mrow")
       handle_expr_ml(bvar.childNodes[0],doc,lower_node)
       createChildTextElement(doc,lower_node,"mo","=")
       handle_expr_ml(low_limit.childNodes[0],doc,lower_node)
       upper_node = createChildElement(doc,sum_node,"mrow")
       for n2 in iterateElementNodes(up_limit.childNodes):
         handle_expr_ml(n2,doc,upper_node)


    if (op == "ci"):
       func_name = get_apply_op_value(node)
       global func_list
       is_index_func = 0
       if func_list.has_key(func_name):
         is_index_func = func_list[func_name]

       if is_index_func:
         msub_node = createChildElement(doc,out_node,"msub")
         createChildTextElement(doc,msub_node,"mi",func_name)
       else:
         createChildTextElement(doc,out_node,"mi",func_name)
       skip = len(node.childNodes)
       #fence_node = createChildElement(doc,out_node,"mfenced")
       if is_index_func:
         fence_node = createChildElement(doc,msub_node,"mrow")
       else:
         fence_node = createChildElement(doc,out_node,"mrow")
         createChildTextElement(doc,fence_node,"mo","(")
       len1 = get_len(iterateElementNodes(node.childNodes[2:]))
       idx1 = 0
       for n2 in iterateElementNodes(node.childNodes[2:]):
         handle_expr_ml(n2,doc,fence_node)
         idx1 += 1
         if (idx1 < len1):
           createChildTextElement(doc,fence_node,"mo",",")
       if not(is_index_func):
         createChildTextElement(doc,fence_node,"mo",")")
   
    len1 = get_len(iterateElementNodes(node.childNodes[skip:]))
    if (need_paren and len1 > 0):
      createChildTextElement(doc,out_node,"mo","(")
      
    prev_node = None
    for n1 in node.childNodes[skip:]:
      if is_element_node(n1): 
         #showNode(n1)
         if (prev_node != None):
           handle_expr_ml(prev_node,doc,out_node,might_need_paren)
           if (op_str != ""):
             createChildTextElement(doc,out_node,"mo",op_str)
         prev_node = n1
    handle_expr_ml(prev_node,doc,out_node,might_need_paren)
    if (need_paren and len1 > 0):
      createChildTextElement(doc,out_node,"mo",")")
    return 
  if is_node_name(node,"ci"):
    new_node = createChildTextElement(doc,out_node,"mi",node.childNodes[0].nodeValue)
    return  
  if is_node_name(node,"cn"):
    new_node = createChildTextElement(doc,out_node,"mn",node.childNodes[0].nodeValue)
    return 
     
  return ""
   


def handle_declare(node):
  out =  get_func_name(node) 
  len1 = get_len(get_arg_list(get_lambda_node(node)))
  if (len1 > 0):
    out += "("
  idx = 0
  for a in get_arg_list(get_lambda_node(node)):
    out += a 
    idx += 1
    if (idx < len1):
      out += ","
  #out = out[0:-1] 
  if (len1 > 0):
    out += ")" 
  out += " = "
  out += handle_expr(get_expr_node(get_lambda_node(node)))[0]
  print out

def handle_declare_cpp(node):
  out =  "double " + get_func_name(node) + "("
  for a in get_arg_list(get_lambda_node(node)):
    out += "double  " + a + ","
  #out = out[0:-1] + ") {\n return "
  out = out[0:-1] + ") {\n "
  (tmp_out,op) = handle_expr_cpp(get_expr_node(get_lambda_node(node)))
  if (op != "sum"):
     out += 'return ' + tmp_out
  else:
     out += tmp_out
  out += ";\n}";
  print out

def handle_declare_cpp2(node):
  is_constant = 0
  constant_attr = node.getAttribute("constant")
  if constant_attr and constant_attr == "true":
    is_constant = 1
  inp_attr = node.getAttribute("input")
  input_type = "double"
  if inp_attr:
    input_type = inp_attr
  c_tree = c_function_def("double",get_func_name(node))
  for a in get_arg_list(get_lambda_node(node)):
    c_arg1 = c_arg(input_type,a)
    c_tree.arglist.append(c_arg1)
  (cexpr,cret) = handle_expr_cpp2(get_expr_node(get_lambda_node(node)))
  if cexpr:
    for expr in cexpr:
      c_tree.expr_list.append(expr)
  if cret:
    ret = c_return_stmt(cret)
    c_tree.expr_list.append(ret)
  if is_constant:
     output_attr = node.getAttribute("output")
     output_type = "double"
     if output_attr:
       output_type = output_attr
     cconst = c_decl(output_type,get_func_name(node),cret)
     if not(cexpr):
       cexpr = []
     cexpr.append(cconst)
     out_str = ""
     for e1 in cexpr:
       out_str += e1.get_string()
     return out_str
  out_str = c_tree.get_string()
  return out_str

def handle_declare_ml(doc,out_node,node):
  is_constant = 0
  constant_attr = node.getAttribute("constant")
  if constant_attr and constant_attr == "true":
    is_constant = 1

  is_index_func = 0
  index_attr = node.getAttribute("index")
  if index_attr and index_attr == "true":
    is_index_func = 1
  
  #math_node = .createElement("math")
  #doc.appendChild(math_node)
  math_node = createChildElement(doc,out_node,"math")
  a_str = "http://www.w3.org/1998/Math/MathML"
  math_node.attributes['xmlns'] = a_str
  # next line, make big math
  math_node.attributes['mode'] = "display"
  mrow_node = createChildElement(doc,math_node,"mrow")

  if is_index_func:
    msub_node = createChildElement(doc,mrow_node,"msub")
    createChildTextElement(doc,msub_node,"mi",get_func_name(node))
    msubrow_node = createChildElement(doc,msub_node,"mrow")
  else:
    createChildTextElement(doc,mrow_node,"mi",get_func_name(node))

  global func_list
  func_list[get_func_name(node)] = is_index_func

  if not(is_constant):
    arg_list = get_arg_list(get_lambda_node(node))
    len1 = get_len(arg_list)
    if (len1 > 0):
      if is_index_func:
        for a in get_arg_list(get_lambda_node(node)):
          createChildTextElement(doc,msubrow_node,"mi",a)
      else:
        fence_node = createChildElement(doc,mrow_node,"mfenced")
        for a in get_arg_list(get_lambda_node(node)):
          createChildTextElement(doc,fence_node,"mi",a)

  createChildTextElement(doc,mrow_node,"mo","=")
    
  handle_expr_ml(get_expr_node(get_lambda_node(node)),doc,mrow_node)
  


def main():
  file_in = sys.argv[1]
  doc = minidom.parse(file_in)
  node = doc.documentElement

  cpp_out = re.sub("\.xml$",".cpp",file_in)
  do_cpp_output = 0
  if cpp_out != file_in:
    do_cpp_output = 1
    cpp_output = open(cpp_out,"w")
 
  doc_out = minidom.Document()
  doc_type = minidom.DocumentType("html")
  doc_type.publicId = "-//W3C//DTD XHTML 1.1 plus MathML 2.0//EN"
  doc_type.systemId = "http://www.w3.org/TR/MathML2/dtd/xhtml-math11-f.dtd"
  doc_out.appendChild(doc_type)
  html_node = createChildElement(doc,doc_out,"html")
 
  html_node.attributes['xmlns'] = "http://www.w3.org/1999/xhtml"
  html_node.attributes['xmlns:math'] = "http://www.w3.org/1998/Math/MathML"
  body_node = createChildElement(doc,html_node,"body")

  #iterate over all the nodes
  for n in walkTree(node):
        if n.nodeType == Node.ELEMENT_NODE and n.nodeName == "math":
          for n3 in n.childNodes:
            if n3.nodeType == Node.ELEMENT_NODE and n3.nodeName == "declare":
              print handle_declare(n3) 
              handle_declare_ml(doc,body_node,n3) 
              if do_cpp_output:
                cpp_str = handle_declare_cpp2(n3)
                cpp_str += '\n'
                cpp_output.write(cpp_str)
            else:
              if n3.nodeType == Node.ELEMENT_NODE and n3.nodeName == "comment":
                body_node.appendChild(n3)
        else:
          if n.nodeType == Node.ELEMENT_NODE and n.nodeName == "comment":
            body_node.appendChild(n)
        
      
     

  # pick out just the math/declare nodes
  #for n in findElement(node,"math"):
  #  for n2 in findElement(n,"declare"):
  #    print handle_declare(n2) 
  #    handle_declare_ml(doc,body_node,n2) 
  #    #handle_declare_cpp(n2)
  #    if do_cpp_output:
  #      cpp_str = handle_declare_cpp2(n2)
  #      cpp_str += '\n'
  #      cpp_output.write(cpp_str)

  #print doc_out.toxml()
  #print doc_out.toprettyxml()
  s = doc_out.toprettyxml()
  #s = doc_out.toxml()
  s = s.replace("my_ampersand;","&")

  xhtml_out = re.sub("\.xml$",".xhtml",file_in)
  if xhtml_out != file_in:
      output = open(xhtml_out,"w")
      output.write(s)
      output.close()

  if do_cpp_output:
      cpp_output.close()

   
  #print s
 

if __name__ == '__main__':
  main()
