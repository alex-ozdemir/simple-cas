#System of equations classes, begun 6 December 2013
#Alex Ozdemir
#aozdemir@hmc.edu

from equation import *
import string

class System(object):
    """An abstract class which handles inputing equations and solving"""
    def __init__(self):
        self.equations = []
        self.formulas = []
        self.knowns = []

    def deleteEquation(self,num):
        debug = True
        self.formulas = filter(lambda X: X.eq_num != num, self.formulas)
        for old_num in range(num + 1,len(self.equations)):
            for formula in self.formulas:
                formula.changeEqNum(self,old_num,old_num - 1)
        del self.equations[num]

    def addEquations(self, list_of_eqs):
        """parses every item in the list as an equation, which is adds"""
        for eq_str in list_of_eqs:
            self.equations.append(parse(eq_str))
            self.generateFormulas(self.equations[-1],len(self.equations) - 1)

    def addKnowns(self, list_of_k):
        """parses every item as a known"""
        for k in list_of_k:
            Variable(k[:k.index('=')])
            Numeral(int(k[k.index('=') + 1:]))
            self.knowns.append([k[:k.index('=')], int(k[k.index('=') + 1:])])
    
        
        
    def editEquations(self):
        while True:
            print "You have currently entered",len(self.equations),"equations:"
            for i in range(len(self.equations)):
                print " ",i+1,":",self.equations[i]
            print "Enter $done when you're done entering equations"
            print "Enter $d# to delete equation #. Ex: $d1"
            print "Otherwise just enter an equation"
            user_input = raw_input(" :> ")
            if user_input == '$done':
                print "Equations entered!"
                break
            elif user_input[:2] == '$d':
                try:
                    self.deleteEquation(int(user_input[2:]) - 1)
                except:
                    print "Couldn't understand the input."
            else:
                try:
                    self.equations.append(parse(user_input))
                    self.generateFormulas(self.equations[-1],len(self.equations) - 1)
                except:
                    print "Couldn't understand the input."

    def use(self):
        debug = False
        while True:
            print "You have currently entered",len(self.knowns),"knowns:"
            for i in range(len(self.knowns)):
                print " ",i+1,":",self.knowns[i][0],'=',self.knowns[i][1]
            print "Enter $done when you're done entering knowns, to solve for unknowns"
            print "Enter $d# to delete equation #. Ex: $d1"
            print "Enter $c to delete all knowns"
            print "Otherwise just enter a known in the format x = 17"
            user_input = raw_input(" :> ")
            user_input = ''.join(user_input.split())
            if user_input == '$done':
                print "knowns entered!"
                break
            elif user_input[:2] == '$d':
                try:
                    del self.knowns[int(user_input[2:]) - 1]
                except:
                    print "Couldn't understand the input."
            elif user_input == "$c":
                self.knowns = []
            else:
                try:
                    if debug: print "Variable: "+user_input[:user_input.index('=')]
                    Variable(user_input[:user_input.index('=')])
                    if debug: print "Numeral: "+user_input[user_input.index('=') + 1:]
                    Numeral(int(user_input[user_input.index('=') + 1:]))
                    self.knowns.append([user_input[:user_input.index('=')], int(user_input[user_input.index('=') + 1:])])
                except:
                    print "Couldn't understand the input."
        print "\nCalculating..."
        self.expandKnowns()
        print "\nNew knowns:"
        for i in range(len(self.knowns)):
            print " ",i+1,":",self.knowns[i][0],'=',self.knowns[i][1]
        

    def generateFormulas(self,equation,eq_num):
        variables = [var[0] for var in equation.findVariables()]
        var_set = set(variables)
        for var in var_set:
            if variables.count(var) == 1:
                self.formulas.append(Formula(equation,eq_num,var))

    def expandKnowns(self):
        debug = False
        success = False
        for formula in self.formulas:
            result = formula.evaluate(self.knowns)#Result in None if evaluation was impossible
            if result != None:
                success = True
                self.knowns.append([formula.out_var,result])
        if success:
            self.expandKnowns()
        
    

class Formula(object):
    """A class which holds a formula- and equation solved for one variable"""
    def __init__(self,equation,eq_num,variable):
        variables = equation.findVariables()
        eq_modifiable = equation.copy()
        
        self.eq_num = eq_num
        self.out_var = variable
        self.in_vars = set(filter(lambda X: X != variable, [X[0] for X in variables]))
        
        variable_occurances = [var[0] for var in variables].count(variable)
        if variable_occurances == 1:
            var = filter(lambda X: X[0] == variable, variables)[0]
            eq_modifiable.isolate(var[1])
            self.formula_string = str(eq_modifiable)[str(eq_modifiable).index('=') + 1:-1]

        self.equation = eq_modifiable
            
    def changeEqNum(self,old_num,new_num):
        if self.eq_num == old_num:
            self.eq_num == new_num

    def evaluate(self,knowns):
        """Returns None if evaluation given those knowns is impossible.
        otherwise returns the value of the output variable"""
        debug = False
        known_var_names = [var[0] for var in knowns]
        if all([variable in known_var_names for variable in self.in_vars]) and self.out_var not in known_var_names:
            success = True
            if debug: print self.equation
            eval_str = self.formula_string
            knowns.sort()
            knowns.reverse()
            for known in knowns:
                if debug: print known
                eval_str = eval_str.replace(known[0],str(known[1]))
                if debug: print eval_str
            return eval(eval_str)
        else:
            return None
    

    def __str__(self):
        return str(self.equation)
        
            
def test():
    optics = System()
    optics.addEquations(['1/i+1/o=1/f','-i/o=M',"h'/h=M"])
    optics.addKnowns(['i=15','f=10','h=5'])
    return optics
