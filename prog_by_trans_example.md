## Programming by Transformation
### Simple Python Example

Start with some Python code to open and close a file (call this V1)
````python
f = open("file.txt", "r")
c = f.read()
f.close()
````

Now add some exception handling (in case the file doesn't exist or is not readable) (call this V2)
````python
try:
    f = open("file.txt", "r")
    c = f.read()
    f.close()
except IOError as e:
    print('Unable to open file: %s' % str(e))
````

Sometime later, we learn about the context manager feature in Python, that will automatically close the file for us.  Modify V1 to get (call this V3)
````python
with open("file.txt", "r") as f:
    c = f.read()
````

The code with exception handling will look like (call this V4)
````python
try:
    with open("file.txt", "r") as f:
        c = f.read()
except:
    print('Unable to open file: %s' % str(e))
````

In traditional development, the history would look like V1 -> V2 (add exception handling) -> V4 (context manager and exception handling).

In the proposed scheme, the code would initially be stored as the flow V1 -> V2 (add exception handling).   The change to use a context manager would be made in the first node (change V1 to V3).  The final flow is then V3 -> V4.
History then looks like

1. V1 -> V2
2. V3 -> V4

Alternately, one could also add a node to make the flow V1 -> V3 (context manager) -> V4 (context manager and exception handling), but this doesn't seem as informative.  It's useful for learning the Python feature, but not as useful for understanding the program.

Ideally the transformation to add the exception handling could be specified in a generic way - label or identify the code that opens and processes the file, and then add the exception handling code around it.  Then the same transformation could be used for V1->V2 and V3->V4.

### Using Comby

The simple Python example above is easy to express in Comby syntax.
The match for the original code (V1)
````python
f = open("file.txt", "r")
c = f.read()
f.close()
````

is

```
:[[var]] = open(:[open_args])
:[body]
:[[var]].close()
```

The rewrite rule to get to V2 is
```
try:
  :[[var]] = open(:[open_args])
  :[body]
  :[[var]].close()
except:
   print("Unable to open file: %s"  % str(e))
```
This example could use ```:[body]``` for the match, but the rest is there to set it off from surrounding code.   This [link](https://bit.ly/2m7nCHU) should open this part of the example in the Comby live editor.

The match for V3
```python
with open("file.txt", "r") as f:
    c = f.read()
```
is
```
with open(:[open_args]) as :[[var]]:
:[body]
```

and the rewrite rule to get to V4 is
```
try:
  with open(:[open_args]) as :[[var]]:
    :[body]
except:
   print("Unable to open file: %s"  % str(e))
```

Recall the history would look like
1. V1 -> V2
2. V3 -> V4

The history for this change would include the base code change from V1 to V3 along with the change to the match and rewrite patterns.

The original example put the translation to using a context manager as part of history rather than part of the program transformation sequence.  If it were important to keep that transformation in the chain, the history could be
1. V1 -> V2   (add error handling)
2. V1 -> V3 -> V4   (use context manager, add error handling)

The transformation from V1->V3 is also easy to express in Comby.

