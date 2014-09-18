#CAS equation classes, begun 5 December 2013
#Alex Ozdemir
#aozdemir@hmc.edu

 

import string #for string constants
from exceptions import *
from math import log

keywords = ['log']


class Branch(object):
    """Wrapper class for equations and operations"""
    def __init__(self, children):
        self.children = children
        for child in self.children:
            child.setParent(self)
        
    def addChild(self, child):
        """Adds a child to an already existing parent"""
        self.children.append(child)
        self.children[-1].setParent(self)

    def getAddress(self,address):
        """Given an adress in the form of a list of indices
        (uppermost first), get the item and returns it"""
        if address == []:
            return self
        else:
            return self.children[address[0]].getAddress(address[1:])

    def setAddress(self, address, value):
        """Sets a certain address equal to a value"""
        if len(address) == 1:
            self.children[address[0]] = value
            self.children[address[0]].setParent(self)
            return True
        else:
            setAddress(self.chldren[address[0]], address[1:], value)
            

    def findVariables(self):
        """Finds the variables in an equations, and returns them
        as a list from variable name to location (list of indices)
        duplicates are possible"""
        results = []
        for node_num in range(len(self.children)):
            results += map( lambda X: [X[0], [node_num]+X[1]] , self.children[node_num].findVariables() )
        results = filter( lambda X: X[0] != '', results )
        return results

    def __eq__(self,other):
        return len(self.children) == len(other.children) and all([self.children[i] == other.children[i] for i in range(len(self.children))])

        
class Equation(Branch):
    def __init__(self, children = []):
        Branch.__init__(self, children)

    def copy(self):
        """Returns a [deep] copy of the equation"""
        return Equation([child.copy() for child in self.children])

    def isolate(self,address):
        debug = False
        if debug: print "Isolating",address,"in:\n",self
        if address[0] == 1:
            self.children.reverse()
            address[0] = 0
        elif address == [0]:
            return True
        if len(address) > 1:
            to_isolate = self.getAddress(address[0:2]).copy()
            right = self.children[1]
            adress_end, inv = self.children[0].getInverse(address[1])
            inv.setAddress(adress_end, right)
            #The get Inverse function puts a placeholder variable with name == '' where the other side goes
            self.setAddress([0],to_isolate)
            self.setAddress([1],inv)
            return self.isolate(address[0:1] + address[2:])
        
    def condenseK(self):
        """A method which combines constants the the equation."""
        result = self.children[0].condenseK() or self.children[1].condenseK()
        if result:
            result = result or self.condenseK()
        return result
            

    def __str__(self):
        return '{' + str(self.children[0])+" = "+str(self.children[1]) + '}'



class Operation(Branch):
    def __init__(self, parent, children = []):
        Branch.__init__(self,children)
        self.parent = parent

    def setParent(self, parent):
        """Sets the parent of an operation"""
        self.parent = parent

class Multiplication(Operation):
    def __init__(self, parent = None, children = []):
        """Creates an mutiplication object with an arbitrary number of children"""
        Operation.__init__(self, parent, children)

    def copy(self):
        """Returns a [deep] copy of the operation"""
        return Multiplication(None, [child.copy() for child in self.children])

    def getInverse(self,index):
        """Returns the structure which inverses this operations,
        preceded by the adress of there the thing to be inverted
        goes"""
        del self.children[index]
        return ([0], Multiplication(None, [Variable('')] + [Exponentiation(None, [child, Numeral(-1)]) for child in self.children]))

    def condenseK(self):
        change = False
        for child_num in range(len(self.children)):
            change = change or self.children[child_num].condenseK()
        constant = 1
        hard = []
        for child_num in range(len(self.children)):
            if type(self.children[child_num]) == Numeral:
                constant *= self.children[child_num].value
            elif type(hard):
                hard.append(self.children[child_num])
        if constant == 0:
            index = self.parent.children.index(self)
            self.parent.setAddress([index],Numeral(0))
            change = True
        else:
            if constant != 1 or len(hard) < 1:
                hard = [Numeral(constant)] + hard
            change = change or (len(hard) != len(self.children))
            if len(hard) >= 2:
                self.children = []
                for new_child in hard:
                    self.addChild(new_child)
            elif len(hard) == 1:
                index = self.parent.children.index(self)
                self.parent.setAddress([index],hard[0])
                change = True
        return change

    def __str__(self):
        result = '('
        for child in self.children:
            result += str(child) + ' * '
        result = result[:-3] + ')'
        return result

class Addition(Operation):
    def __init__(self, parent = None, children = []):
        """Creates an addition object with an arbitrary number of children"""
        Operation.__init__(self, parent, children)

    def copy(self):
        """Returns a [deep] copy of the operation"""
        return Addition(None, [child.copy() for child in self.children])

    def getInverse(self,index):
        """Returns the structure which inverses this operations,
        preceded by the adress of there the thing to be inverted
        goes"""
        del self.children[index]
        return ([0], Addition(None, [Variable('')] + [Multiplication(None, [Numeral(-1), child]) for child in self.children]))

    def condenseK(self):
        change = False
        for child_num in range(len(self.children)):
            change = change or self.children[child_num].condenseK()
        constant = 0
        hard = []
        for child_num in range(len(self.children)):
            if type(self.children[child_num]) == Numeral:
                constant += self.children[child_num].value
            else:
                hard.append(self.children[child_num])
        if constant != 0 or len(hard) == 0:
            hard.append(Numeral(constant))
        change = change or (len(hard) != len(self.children))
        if len(hard) >= 2:
            self.children = []
            for new_child in hard:
                self.addChild(new_child)
        elif len(hard) == 1:
            index = self.parent.children.index(self)
            self.parent.setAddress([index],hard[0])
            change = True
        return change
        
            
    
    def __str__(self):
        result = '('
        for child in self.children:
            result += str(child) + ' + '
        result = result[:-3] + ')'
        return result

class Exponentiation(Operation):
    def __init__(self, parent = None, children = []):
        """Creates an exponentiation object. The second child is the power"""
        if len(children) > 2:
            raise ValueError('Exponentiation ccan only take 2 arguements')
        Operation.__init__(self, parent, children)

    def copy(self):
        """Returns a [deep] copy of the operation"""
        return Exponentiation(None, [child.copy() for child in self.children])

    def getInverse(self, index):
        """Returns the structure which inverses this operations,
        preceded by the adress of there the thing to be inverted
        goes"""
        if index == 0:
            return ([0], Exponentiation(None, [Variable(''), Exponentiation(None, [self.children[1], Numeral(-1)])]))
        elif index == 1:
            return ([0], Logarithm(None, [Variable(''), self.children[0]]))
        else:
            return False

    def condenseK(self):
        change = False
        for child_num in range(len(self.children)):
            change = change or self.children[child_num].condenseK()
        if self.children[1] == Numeral(0):
            index = self.parent.children.index(self)
            self.parent.setAddress([index],Numeral(1))
        if all([type(x) == Numeral for x in self.children]):
            index = self.parent.children.index(self)
            self.parent.setAddress([index],Numeral(self.children[0] ** self.children[1]))
            

    def __str__(self):
        return '(' + str(self.children[0]) + ' ** ' + str(self.children[1]) + ')'
    

class Logarithm(Operation):
    def __init__(self, parent = None, children = []):
        """Creates a logarithm object. The second child is the base"""
        if len(children) > 2:
            raise ValueError('Logarithm ccan only take 2 arguements')
        Operation.__init__(self, parent, children)

    def copy(self):
        """Returns a [deep] copy of the operation"""
        return Logarithm(None, [child.copy() for child in self.children])

    def getInverse(self, address):
        """Returns the structure which inverses this operations,
        preceded by the adress of there the thing to be inverted
        goes"""
        if address == 0:
            return ([1],Exponentiation(None, [self.children[1], Variable('')]))
        elif address == 1:
            return ([1,0], Exponentiation(None, [self.children[0], Exponentiation(None, [Variable(''), Numeral(-1)])]))

    def condenseK(self):
        change = False
        for child_num in range(len(self.children)):
            change = change or self.children[child_num].condenseK()
        if all([type(x) == Numeral for x in self.children]):
            index = self.parent.children.index(self)
            self.parent.setAddress([index],Numeral(math.log(self.children[0],self.children[1])))

    def __str__(self):
        return '(log('+str(self.children[0])+','+str(self.children[1])+'))'

class Leaf(object):
    """Wrapper class for numerals and variables"""
    def __init__(self, parent):
        self.parent = parent

    def setParent(self, parent):
        self.parent = parent

    def condenseK(self):
        return False

    def getAddress(self, address):
        if address != []:
            raise TypeError('Cannot index variables or numerals:\n' + str(self))
        else:
            return self

class Numeral(Leaf):
    def __init__(self, value, parent = None):
        """Creates a numeral with the given parent and value"""
        if type(value) not in [int, long, float]:
            raise TypeError('Numeral can only take values which are numbers')
        Leaf.__init__(self, parent)
        self.value = value

    def copy(self):
        """Returns a [deep] copy of the numeral"""
        return Numeral(self.value)

    def findVariables(self):
        return [['',[]]]

    def __eq__(self, other):
        try:
            return self.value == other.value
        except:
            return False
    
    def __str__(self):
        return str(self.value)

class Variable(Leaf):
    def __init__(self, name, parent = None):
        """Creates a variable with the given parent and value"""
        if not all([x in string.ascii_letters + "_'" + string.digits for x in name]):
            raise ValueError('Variable names can only include letters, numbers, _ and \'')
        if not all([x not in name for x in keywords]):
            raise ValueError('Variable names cannot include keywords')
        Leaf.__init__(self, parent)
        self.name = name

    def copy(self):
        """Returns a [deep] copy of the variable"""
        return Variable(self.name)

    def findVariables(self):
        return [[self.name,[]]]

    def __eq__(self, other):
        try:
            return self.name == other.name
        except:
            return False

    def __str__(self):
        return self.name


def parse(expression):
    debug = False
    expression = ''.join(expression.split())
    #Checking if only valid characters are there
    if not all([ char in string.ascii_letters + string.digits + '\'().,_-+*=/' for char in expression]):
        raise ValueError('There are invalid characters!')
    #Checking if the open/close parentheses are of equal number
    if expression.count('(') != expression.count(')'):
        raise ValueError('There are different numbers of closing and openning parentheses')
    expression = stripParens(expression)
    #Replace minus with plus negative, and divide with times the reciprocal
    expression = replaceOperations(expression)
    if debug: print 'Expression:',expression
    #We're gonna record the positions of operators in the expression (if they're outside parentheses)
    #We need these variables to do that
    parenthesis_level = 0
    plus_positions = []
    times_positions = []
    log_positions = []
    exp_positions = []
    eq_positions = []
    comma_positions = []
    result = None
    for i in range(len(expression)):
        if expression[i] == '(':
            parenthesis_level += 1
        elif expression[i] == ')':
            parenthesis_level += -1
        
        if parenthesis_level == 0:   #If we're not inside any parens, record the position of
            if expression[i] == '+':    #plusses
                plus_positions.append(i)
            elif  expression[i] == '*' and expression[i - 1: i] != '*' and expression[i + 1: i + 2] != '*':   #times
                times_positions.append(i)
            elif expression[i: i + 2] == '**':   #exponents 
                exp_positions.append(i)
            elif expression[i: i + 4] == 'log(':   #logarithms
                log_positions.append(i)
            elif expression[i] == '=':   #equals
                eq_positions.append(i)
        elif parenthesis_level < 0:
            raise ValueError('There are mismatched parentheses')
        else:
            # then parenthesis_level > 0
            if expression[i] == '=':
                #If an equals is found in parens... derpderp
                raise ValueError('No equals permitted inside parens')
            if parenthesis_level == 1 and expression[i] == ',':
                comma_positions.append(i)
    #If any equals were found
    if eq_positions != []:
        if debug: print 'Equals sign found:',str(eq_positions)
        sub_expressions = expression.split('=')
        if len(eq_positions) > 1:
            raise ValueError('Equations can only have 1 equals sign!')
        return Equation(map(parse, sub_expressions))
    #Else, If any plusses were found outside parens
    elif plus_positions != []:
        if debug: print 'Plus sign found:',str(plus_positions)
        sub_expressions = []
        plus_positions.insert(0,-1)
        plus_positions.append(len(expression))
        if debug: print 'Plus boundaries found:',str(plus_positions)
        for i in range(len(plus_positions) - 1):
            sub_expressions.append(expression[plus_positions[i] + 1: plus_positions[i + 1]])
        if debug: print 'Sub Expressions found:',sub_expressions
        return Addition(None, map(parse, sub_expressions))
    #Else, If any exponents were found outside parens
    elif times_positions != []:
        sub_expressions = []
        times_positions.insert(0,-1)
        times_positions.append(len(expression))
        for i in range(len(times_positions) - 1):
            sub_expressions.append(expression[times_positions[i] + 1: times_positions[i + 1]])
        return Multiplication(None, map(parse, sub_expressions))
    #Else if it seems to be an exponential
    elif exp_positions != []:
        if len(exp_positions) > 1:
            raise ValueError('Unexpected exponential at position:\n' + expression[exp_positions[1]:])
        return Exponentiation(None, map(parse, [expression[:exp_positions[0]], expression[exp_positions[0] + 2:]]))
    elif log_positions != []:
        if debug: print 'Logarithm recognized:',expression
        if len(log_positions) > 1:
            raise ValueError('Unexpected logarithm at position:\n' + expression[log_positions[1]:])
        elif log_positions[0] != 0:
            raise ValueError('Unexpected logarithm at position:\n' + expression[log_positions[0]:])
        elif comma_positions == [] or len(comma_positions) > 1:
            raise ValueError('Logarithm takes 2 arguments:\n' + expression)
        elif expression[:4] == 'log(' and expression[-1] == ')':
            return Logarithm(None, map(parse, [expression[4:comma_positions[0]], expression[comma_positions[0] + 1:-1]]))
    #Else If the thing seems to be a number...
    elif all([x in '.-'+string.digits for x in expression]):
        try:
            if int(expression) == float(expression):
                return Numeral(int(expression))
            else:
                return Numeral(float(expression))
        except ValueError:
            raise ValueError('This doesn\'t seem to be a valid number:\n' + expression)
    #Or a variable
    elif expression[0] in '-_\''+string.ascii_letters:
        if expression[0] == '-':
            if '()*+\\/-' in expression[1:]:
                raise ValueError('Invalid variable name:\n' + expression)
            else:
                return Multiplication(None,[Numeral(-1),Variable(expression[1:])])
        else:
            if '()*+\\/-' in expression:
                raise ValueError('Invalid variable name:\n' + expression)
            else:
                return Variable(expression)
    else:
        raise ValueError('Could not parse this expression:\n' + expression)


def replaceOperations(expression):
    """Replaces subtration and division"""
    debug = False
    operations = ['log(', '*', '*', '/', '+', '(', ',', '-', '=']
    i = 1
    while i < len(expression):
        if debug: print 'index:',i,'\nstring:',expression
        if expression[i] == '-' and all([expression[i-len(op): i] != op for op in operations]):
            expression = expression[:i] + '+-1*' + expression[i + 1:]
            i += 3
        if expression[i] == '/' and all([expression[i-len(op): i] != op for op in operations]):
            expression = expression[:i] + '*' + expression[i + 1:]
            depth = 0
            j = i + 1
            if debug: print '  index:',j,'\n  string:',expression
            while j == i + 1 or depth != 0 or all([expression[j: j + len(op)] != op for op in operations]):
                if debug: print '  index:',j,'\n  string:',expression,'\n  depth:',depth
                for keyword in keywords:
                    if expression[j: j + len(keyword)] == keyword:
                        j += len(keyword)
                if j >= len(expression):
                    break
                if expression[j] == '(':
                    depth += 1
                elif expression[j] == ')':
                    depth += -1
                j += 1
            expression = expression[:j] + '**-1' + expression[j:]
                
        i += 1
    return expression

def stripParens(string):
    """Removes matching opening and closing parentheses"""
    if string[0] == '(' and string[-1] == ')':
        return stripParens(string[1:-1])
    else:
        return string
            

def testReplaceOperations():
    b = '1/2'
    print b,' -> ',replaceOperations(b)
    b = '1/(2+3)'
    print b,' -> ',replaceOperations(b)
    b = '1/log(20+(4*5))'
    print b,' -> ',replaceOperations(b)
    b = '1/log(20+(4*5-log(3,4)))'
    print b,' -> ',replaceOperations(b)
    b = '1/2/3'
    print b,' -> ',replaceOperations(b)
    b = '1-3/4'
    print b,' -> ',replaceOperations(b)
