simple-cas
==========

A [very basic] computer algebra system


This is an attempt of mine to make a rudimentary computer algebra system. It is very limited, but fully functional within it's capbilities. You can enter equations (and it will parse them). You can then enter known vairables, and there values. Then the system will analyze the equations/variables, and solve for all variable it can. The one (BIG) thing it cannot do is solve equations for variables which occur multiple times in the equations. Consequently, it cannot combine equations either.

This area of CS (referred to as 'Symbolic Algebra') is very deep, and I'm extremely interested in learning more about it in the future.

To run the program, download (and unzip as necessary) the source, and run:

python main.py



Included below is an example interaction:


You have currently entered 0 equations:

Enter $done when you're done entering equations

Enter $d# to delete equation #. Ex: $d1

Otherwise just enter an equation

 :> (2*x + 3*y)/z = 12
 
You have currently entered 1 equations:

  1 : {(((2 * x) + (3 * y)) * (z ** -1)) = 12}
  
Enter $done when you're done entering equations

Enter $d# to delete equation #. Ex: $d1

Otherwise just enter an equation

 :> 2*x**2 = d
 
You have currently entered 2 equations:

  1 : {(((2 * x) + (3 * y)) * (z ** -1)) = 12}
  
  2 : {(2 * (x ** 2)) = d}
  
Enter $done when you're done entering equations

Enter $d# to delete equation #. Ex: $d1

Otherwise just enter an equation

 :> j=k
 
You have currently entered 3 equations:

  1 : {(((2 * x) + (3 * y)) * (z ** -1)) = 12}
  
  2 : {(2 * (x ** 2)) = d}
  
  3 : {j = k}
  
Enter $done when you're done entering equations

Enter $d# to delete equation #. Ex: $d1

Otherwise just enter an equation

 :> $done
 
Equations entered!

You have currently entered 0 knowns:

Enter $done when you're done entering knowns, to solve for unknowns

Enter $d# to delete equation #. Ex: $d1

Enter $c to delete all knowns

Otherwise just enter a known in the format x = 17

 :> y = 6
 
You have currently entered 1 knowns:

  1 : y = 6
  
Enter $done when you're done entering knowns, to solve for unknowns

Enter $d# to delete equation #. Ex: $d1

Enter $c to delete all knowns

Otherwise just enter a known in the format x = 17

 :> z = 3
 
You have currently entered 2 knowns:

  1 : y = 6
  
  2 : z = 3
  
Enter $done when you're done entering knowns, to solve for unknowns

Enter $d# to delete equation #. Ex: $d1

Enter $c to delete all knowns

Otherwise just enter a known in the format x = 17

 :> $done
 
knowns entered!


Calculating...


New knowns:

  1 : z = 3
  
  2 : y = 6
  
  3 : x = 9.0
  
  4 : d = 162.0
  
Type 'new' to continue.

Type anything else to quit.
