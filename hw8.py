import copy
from functools import total_ordering


class Monom:
    def __init__(self, power, coef=1):  # regular placement constructor as required.
        self.power = power
        self.coef = round(coef, 2)  # shows 2 digits after decimal point.
        self.next = None

    def __repr__(self):
        # next 5 lines are customizing the coef digits as required.
        coef_res = self.coef  # temp coef pointer.
        if self.coef % 1.0 == 0.0:  # in case coef has zeros after decimal point.
            coef_res = int(self.coef)  # delete the zeros and the decimal point.
        # next 6 lines are in case the coef is negative.
        if coef_res < 0:  # checks negativity.
            if self.power == 1:  # in case power is 1:
                return '({}X)'.format(coef_res)  # returns monom with parenthesis (without showing the power).
            if self.power == 0:  # in case power is 0:
                return '({})'.format(coef_res)  # returns monom with parenthesis (without showing X - he turned into 1).
            return '({}X^{})'.format(coef_res, self.power)  # returns monom with parenthesis.
        # next 6 lines are in case the coef is 1.
        if coef_res == 1:  # checks condition.
            if self.power == 1:  # in case power is 1:
                return 'X'  # returns monom (without showing the power and the coef).
            if self.power == 0:  # in case power is 0:
                return '{}'.format(coef_res)  # returns monom (without showing X - he turned into 1).
            return 'X^{}'.format(self.power)  # returns monom (without showing coef - he is 1).
        # next 2 lines are in case the coef is 0.
        if coef_res == 0:  # checks condition.
            return '0'  # if coef is 0, all the monom is 0.
        # next 7 lines are on any other case.
        if self.power == 1:  # in case power is 1:
            if coef_res == 0:  # in case coef is 0:
                return '{}'.format(coef_res)  # returns monom (without showing X - he turned into 1).
            return '{}X'.format(coef_res)  # returns monom (without showing the power).
        if self.power == 0: # in case power is 0:
            return '{}'.format(coef_res)  # returns monom (without showing X - he turned into 1).
        return '{}X^{}'.format(coef_res, self.power)  # if code reached here, it is a normal monom.

    def __mul__(self, other):  # multiplication.
        if isinstance(other, (int, float)):  # in case other is a number.
            return Monom(self.power, self.coef * other)  # multiply the coef with the number.
        if isinstance(other, Monom):  # in case other is a monom.
            return Monom(self.power + other.power, self.coef * other.coef)  # addd powers and multiply the coefs.

    def __rmul__(self, other):  # multiplication from right using regular mul.
        return self * other

    def derivative(self):
        return Monom(self.power - 1, self.coef * self.power)  # according to derivative rules.

    def integral(self):
        if self.power + 1 != 0:  # prevents divide by zero.
            return Monom(self.power + 1, self.coef / (self.power + 1))  # according to integral rules.
        return Monom(1,0)  # in case integral cause division by zero.


@total_ordering
class Polynomial:
    def __init__(self, l):
        if not isinstance(l, list):  # in case parameter is not a list.
            raise ValueError('Invalid polynomic initiation.')
        for tup in l:  # runs over items of the list.
            if not isinstance(tup, tuple) or len(tup) != 2 or not isinstance(tup[0], (int, float)) or not isinstance(tup[1], (int, float)):  # checks if all items are 2 long tuples filled with numbers only.
                raise ValueError('Invalid polynomic initiation.')
        self.head = None  # head pointer.
        for monom_tuple in l:  # runs over the tuples that represents the monoms.
            add_monom_to_sorted_polynomial(self, monom_tuple)  # uses the helping method below to enter the monoms to the polynomial.
        clean_zeros_from_polynomial(self)  # in case two monons created a monom with coef of 0 (zero number) we don't want to be exist (means nothing).

    def __repr__(self):
        result = 'P(X)='  # string that it is going to be filled with monom's __repr__.
        p = self.head  # pointer to the head of the polynomial.
        if p == None:  # in case polynomial is zero.
            return result + '0'
        while p != None:  # runs over polynomial's monoms.
            result += p.__repr__() + '+'  # adds the monom's __repr__.
            p = p.next  # jump to the next monom on the linked list.
        return result[:len(result) - 1]  # returns result without last char (extra plus).

    def rank(self):
        if self.head == None:  # in case polynomial is 0.
            return 0
        return self.head.power  # monoms already sorted from biggest power to the lowest.

    def calculate_value(self, x):
        result = 0  # number we gonna sum with each monom.
        p = self.head  # pointer to the head of the polynomial.
        while p != None:  # runs over polynomial's monoms.
            pow_temp_res = 1  # temp num used to sum calculates of x in current power.
            for pow in range(p.power):  # loops power times.
                pow_temp_res = x * pow_temp_res  # x in power calculation.
            result += p.coef * pow_temp_res  # multiply the result with the coef.
            p = p.next  # jump to the next monom on the linked list.
        return result

    def __neg__(self):
        result = Polynomial([])  # creates new empty polynomial.
        p = self.head  # pointer to the head of the polynomial.
        while p != None:  # runs over polynomial's monoms.
            add_monom_to_sorted_polynomial(result, (p.power, -p.coef))  # turn each monom into a tuple (with negative coef) and inserts it sorted to the new polynomial.
            p = p.next  # jump to the next monom on the linked list.
        return result

    def __add__(self, other):
        result = Polynomial([])  # creates new empty polynomial.
        self_p = self.head  # pointer to the head of the self polynomial.
        while self_p != None:  # runs over self polynomial's monoms.
            add_monom_to_sorted_polynomial(result, (self_p.power, self_p.coef))  # turn each monom into a tuple and inserts it sorted to the new polynomial.
            self_p = self_p.next  # jump to the next monom on the self linked list.
        other_p = other.head  # pointer to the head of the other polynomial.
        while other_p != None:  # runs over other polynomial's monoms.
            add_monom_to_sorted_polynomial(result, (other_p.power, other_p.coef))  # turn each monom into a tuple and inserts it sorted to the new polynomial.
            other_p = other_p.next  # jump to the next monom on the other linked list.
        clean_zeros_from_polynomial(result)  # cleans monoms that turned to 0 after the sum.
        return result

    def __sub__(self, other):
        return self + (-other)  # sums self and negative other.

    def __mul__(self, other):
        result = Polynomial([])  # creates new empty polynomial.
        if isinstance(other, (int, float)):  # checks if other is a number.
            self_p = self.head  # pointer to the head of the self polynomial.
            while self_p != None:  # runs over self polynomial's monoms.
                add_monom_to_sorted_polynomial(result, (self_p.power, self_p.coef * other))  # turn each monom into a tuple (with coef multiplied by other) and inserts it sorted to the new polynomial.
                self_p = self_p.next # jump to the next monom on the self linked list.
        else:  # in case other is a polynomial.
            other_p = other.head  # pointer to the head of the other polynomial.
            while other_p != None:  # runs over other polynomial's monoms.
                result += polinomial_monom_mul(self, other_p)  # uses the helping method below to multiply monom with polynomial and do it for all monoms.
                other_p = other_p.next  # jump to the next monom on the other linked list.
        return result

    def __rmul__(self, other):  # multiplication from right using regular mul.
        return self * other

    def derivative(self):
        result = Polynomial([])  # creates new empty polynomial.
        p = self.head  # pointer to the head of the self polynomial.
        while p != None:  # runs over self polynomial's monoms.
            add_monom_to_sorted_polynomial(result, (p.derivative().power, p.derivative().coef))  # derivates each monom and turns it into a tuple, then inserts it sorted to the new polynomial.
            p = p.next  # jump to the next monom on the self linked list.
        return result

    def integral(self, x=0):
        result = Polynomial([])  # creates new empty polynomial.
        self_p = self.head  # pointer to the head of the self polynomial.
        while self_p != None:  # runs over self polynomial's monoms.
            add_monom_to_sorted_polynomial(result, (self_p.integral().power, self_p.integral().coef))  # turn each monom to his integral and turns it into a tuple, then inserts it sorted to the new polynomial.
            self_p = self_p.next  # jump to the next monom on the self linked list.
        if x != 0:  # adds constant if its not a zero.
            result_p = result.head  # pointer to the head of the result polynomial.
            while result_p.next != None:  # runs over result polynomial's monoms until first from the end..
                result_p = result_p.next  # jump to the next monom on the result linked list.
            result_p.next = Monom(0, x)  # adds the constant monom to the result linked list.
        return result

    def __gt__(self, other):
        self_p = self.head  # pointer to the head of the self polynomial.
        other_p = other.head  # pointer to the head of the other polynomial.
        while self_p != None and other_p != None:  # checks if one of the polynomials reached to his end.
            if self_p.power != other_p.power or self_p.coef != other_p.coef:  # enters condition only if there's a different between the two polynomials in specific current monom (means we can tell who's bigger from this monom).
                if self_p.power > other_p.power or (self_p.power == other_p.power and self_p.coef > other_p.coef):  # self power is larger than other's power or powers and even but self coef is bigger then other's coef.
                    return True  # if so, it means self is bigger.
                return False  # if there's a difference in this specific current monom and self is not bigger, it means that he is smaller.
            else:  # if current monoms are equals.
                self_p = self_p.next  # jump to the next monom on the self linked list.
                other_p = other_p.next  # jump to the next monom on the other linked list.
        if self_p != None and other_p == None:  # if polynomials are equal but other polynomial reached to his end before self did, it means self is bigger.
            return True
        return False  # if all conditions of gt didn't return True yet, it means self is not greater than...

    def __eq__(self, other):
        self_p = self.head  # pointer to the head of the self polynomial.
        other_p = other.head  # pointer to the head of the other polynomial.
        while self_p != None and other_p != None:  # checks if one of the polynomials reached to his end.
            if self_p.power != other_p.power or self_p.coef != other_p.coef:  # checks if there is a difference between the two current monoms.
                return False  # if so, it means they are no equal.
            else:  # if current both monoms are equals, continue to next couple.
                self_p = self_p.next  # jump to the next monom on the self linked list.
                other_p = other_p.next  # jump to the next monom on the other linked list.
        if (self_p != None and other_p == None) or (self_p == None and other_p != None):  # if both polynomials are equal until some monom but one of them reached to his end before the other,
            return False  # it means they are not equal
        return True

def add_monom_to_sorted_polynomial(polynom, monom_tuple):  # helping method that gets monom tuple and inserts it sorted to a polynomial.
    monom = Monom(monom_tuple[0], monom_tuple[1])  # turn the tuple into a monom.
    if monom.coef == 0:  # in case monom equals 0:
        return  # no need to enter anything.
    if polynom.head == None:  # in case polynomial is empty:
        polynom.head = monom  # we enter the new monom as first.
        return  # getting out of the function.
    p = polynom.head  # pointer to the head of the polynomial.
    if monom.power > p.power:  # if new monom's power is greater than first polynomial's power:
        monom.next = p  # make new monom point the first monom of the polynomial.
        polynom.head = monom  # make the polynomial head point the new monom we just entered.
        return  # getting out of the function.
    if monom.power == p.power:  # in case new monom's power is equal to first monom's (of the polynomial) power.
        p.coef += monom.coef  # sum two monoms with same power (instead of entering new one with same power).
        return  # getting out of the function.
    else:  # in case new monom's power different from first monom's (of the polynomial) power.
        while p != None:  # runs over polynomial's monoms.
            if monom.power == p.power:  # checks whether new monom's power is equal to current polynomial's monom's power.
                p.coef += monom.coef  # sum coefs of two monoms with same power (instead of entering new one with same power).
                return # getting out of the function.
            if not p.next:  # if we made it to the last monom of the linked list:
                p.next = monom  # it means that new power is lower than all monoms of linked list and it should be added in the end.
                return  # getting out of the function.
            if monom.power < p.power and monom.power > p.next.power:  # if we reached a location where new power is smaller than left monom's power and bigger than right monom's power, it need to be added here.
                monom.next = p.next  # make new monom point the monom from right.
                p.next = monom  # make current monom point the new monom.
                return  # getting out of the function.
            else:  # if we reached until here, we didn't find a place where we can add the monom so we continue to next monom on linked list.
                p = p.next  # jump to the next monom on the linked list.
    return  # getting out of the function.

def clean_zeros_from_polynomial(polynom):  # helping method that removes monoms that are equals to zero (can happend by sum of monoms).
    if polynom.head == None:  # in case linked list is empty, we don't need to remove anything.
        return  # getting out of the function.
    cur = polynom.head  # pointer to current place of linked list.
    prev = None  # pointer that will be behind cur (None in the beginning).
    while cur != None and cur.coef == 0:  # locate sequence of zeros that are located in the beginning of the linked list.
        polynom.head = cur.next  # make linked list point the next monom after cur (garbage collector will delete cur).
        cur = polynom.head  # make cur point the first new linked list's monom.
    while cur != None:  # runs over what's left from polynomial's monoms (now empty or starts from monons that are not zero).
        while cur != None and cur.coef != 0:  # while monoms are not zeros:
            prev = cur  # make prev point cur monom.
            cur = cur.next  # make cur point cur's next monom.
        if cur == None:  # checks if we reached to end of linked list.
            return  # getting out of the function.
        # if we are here we reached a zero monom:
        prev.next = cur.next  # make prev point the next monom after cur (garbage collector will delete cur (zero)).
        cur = prev.next  # make cur point the monom after prev.
    return  # getting out of the function.

def polinomial_monom_mul(polynom, monom):  # helping method that multiply a monom with all the monoms of a polynomial.
    result = Polynomial([])  # creates new empty polynomial.
    p = polynom.head  # pointer to the head of the polynomial.
    while p != None:  # runs over polynomial's monoms.
        add_monom_to_sorted_polynomial(result, (p.power + monom.power, p.coef * monom.coef))  # make a new monom tuple with power as sum of powers and coef as multiplication of coefs and inserts it (as a monom) sorted to the new polynomial.
        p = p.next  # jump to the next monom on the linked list.
    return result


class BinTreeNode:
    def __init__(self, val):
        self.value = val
        self.left = self.right = None


class PolynomialBST:
    def __init__(self, head=None):
        self.head = head  # value of curernt node (a polynomial).
        self.left = self.right = None  # pointers to sons.

    def insert(self, polynomial):  # wrapper method that inserts a polynomial to the tree (sorted).
        def insert_rec(head, polynomial):  # called from wrapper, recursively inserts the polynomial to a the right place in the tree.
            if polynomial <= head.head:  # if polynomial is smaller or equal to current root's polynomial.
                if not head.left:  # if left son of current root is empty:
                    head.left = PolynomialBST(polynomial)  # insert polynomial in left son.
                else:  # if left son is not empty:
                    insert_rec(head.left, polynomial)  # call the recursion with the left son as a root.
            else:  # if polynomial is greater than current root's polynomial.
                if not head.right:  # if right son of current root is empty:
                    head.right = PolynomialBST(polynomial)  # insert polynomial in right son.
                else:  # if right son is not empty:
                    insert_rec(head.right, polynomial)  # call the recursion with the right son as a root.
            return  # getting out of the function.
        if not self.head:  # method starts from here, checks whether root is empty or not.
            self.head = polynomial  # if it does, inserts polynomial to root.
        else:  # in case root is not empty:
            insert_rec(self, polynomial)  # call recursion to find the right place to insert the polynomial.

    def in_order(self):  # wrapper method that returns a list with all the polynomials of the tree sorted from small to big.
        def in_order_rec(root):  # called from wrapper, recursively concatenating polynomial's lists in the right order.
            if not root:  # in case current root is empty:
                return []  # return empty list.
            return in_order_rec(root.left) + [root.head] + in_order_rec(root.right)  # concatenate the list of polynomials that are smaller than current root with current root polynomial and the list of polynomials that are greater than current root polynomial.
        if not self.head:  # method starts from here, checks whether root is empty or not.
            return []  # if it does, it returns empty list.
        else:  # in case root is not empty:
            return in_order_rec(self)  # call recursion to get the sorted polynomials list.

    def __add__(self, other):  # method that add two polynomial binary search trees.
        result = PolynomialBST()  # creates new empty PolynomialBST.
        for pol in self.in_order():  # runs over a sorted list of polynomials from first tree:
            result.insert(pol)  # inserts each polynomial to its specific place (sorted) in the the new list.
        for pol in other.in_order():  # runs over a sorted list of polynomials from second tree:
            result.insert(pol)  # inserts each polynomial to its specific place (sorted) in the the new list.
        return result