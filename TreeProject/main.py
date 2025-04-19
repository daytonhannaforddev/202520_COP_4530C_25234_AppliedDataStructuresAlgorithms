# Demonstrate Python Binary Tree implmenentation
# Using star dataset from:
# http://www.projectrho.com/public_html/starmaps/catalogues.php

import csv
import time

# Data on one star
class Star():
    def __init__( self, habhvg, name, mag, spectral, habit, dist):
        self.habhvg = habhvg
        self.display_name = name
        self.magnitude = mag
        self.spectral_class = spectral
        self.habitable = habit
        self.distance_parsecs = dist

    def print_me(self):
        print("display_name=" + self.display_name + ", magnitude =" + self.magnitude)
        print("habhvg="+ self.habhvg + ", spectral="+ self.spectral_class+ ", habitable="+ self.habitable)

# Wrap info for one star in a node suitable for placing in the tree
class TreeNode():
    def __init__(self, star ):
        self.left = None
        self.right = None
        self.star_info = star
        self.name = "N" + str(self.star_info.habhvg)
        self.key = star.display_name

    def print_key( self ):
        print( self.key)

    def print_me(self):
        print( "node name =" + self.name)

        if self.left is None:
            print( "left is None")
        else:
            print( "left child:", end="")
            self.left.print_me()

        if self.right is None:
            print("right is None")
        else:
            print( "right child:", end="")
            self.right.print_me()

        if self.star_info is None:
            print("value is None", end="")
        else:
            self.star_info.print_me()
#
# This is the tree into which we will insert the Star data
#
class Tree():
    def __init__(self, name):
        self.name = name
        self.node_num = 0
        self.node_list= []
        self.root = None

    """
    Zybook section 5.10
    BSTInsertRecursive(parent, nodeToInsert) {
       if (nodeToInsert⇢key < parent⇢key) {
          if (parent⇢left is null)
             parent⇢left = nodeToInsert
          else
             BSTInsertRecursive(parent⇢left, nodeToInsert)
       }
       else {
          if (parent⇢right is null)
             parent⇢right = nodeToInsert
          else
             BSTInsertRecursive(parent⇢right, nodeToInsert)
       }
    }
    """
    # Non-recursive wrapper to deal with adding first node in tree (becomes root)

    #
    # Your code for insert here...
    # Add the star object to a new TreeNode, using the 
    # star_info member of the TreeNode to hold the star
    # object and using the display_name member of star as
    # the key variable in the TreeNode
    #
    def insert( self, star):
        new_node = TreeNode(star)
        if self.root is None:
            self.root = new_node
            self.node_list.append(new_node)
            self.node_num += 1
            return
        current = self.root
        while True:
            if new_node.key < current.key:
                if current.left is None:
                    current.left = new_node
                    break
                else:
                    current = current.left
            else:
                if current.right is None:
                    current.right = new_node
                    break
                else:
                    current = current.right
        self.node_list.append(new_node)
        self.node_num += 1


    """
    Zybook section 5.7
    BSTPrintInorder(node) {
       if (node is null)
          return                     // "Ret"

       BSTPrintInorder(node⇢left)   // "L"  
       Print node                    // "Cur"
       BSTPrintInorder(node⇢right)  // "R"
    }
    """

    #
    # Your code to print the nodes in the tree here
    #
    # Star has a print_me() method that will dump some attributes
    # for you when called.
    #
    def preorder_print( self, root ):
        if root is None:
            return
        self.preorder_print(root.left)
        root.star_info.print_me()
        self.preorder_print(root.right)

    """
    ZyBook 5.12.2
    def search(self, desired_key):
        current_node = self.root
        while current_node is not None:
            # Return the node if the key matches.
            if current_node.key == desired_key:
                return current_node
                
            # Navigate to the left if the search key is
            # less than the node's key.
            elif desired_key < current_node.key:
                current_node = current_node.left
                
            # Navigate to the right if the search key is
            # greater than the node's key.
            else:
                current_node = current_node.right
      
        # The key was not found in the tree.
        return None
    """

    #
    # Your code to search the tree here
    #
    # Search for a node in the Tree whose key matches the
    # key ardument here
    def search( self, key):
        current_node = self.root
        while current_node is not None:

            if current_node.key == key:
                return current_node

            elif key < current_node.key:
                current_node = current_node.left

            else:
                current_node = current_node.right

        return None


# Utility functions
# from: https://www.techiedelight.com/c-program-print-binary-tree/
# This prints a text diagram showing the tree shape
class Trunk:
    def __init__(self, prev=None, str=None):
        self.prev = prev
        self.str = str

def showTrunks(p):
    if p is None:
        return
    showTrunks(p.prev)
    print(p.str, end='')


def printTree(root, prev, isLeft):
    if root is None:
        return

    prev_str = '	'
    trunk = Trunk(prev, prev_str)
    printTree(root.right, trunk, True)

    if prev is None:
        trunk.str = '———'
    elif isLeft:
        trunk.str = '.———'
        prev_str = '   |'
    else:
        trunk.str = '`———'
        prev.str = prev_str

    showTrunks(trunk)
    print(' ' + root.star_info.display_name)
    if prev:
        prev.str = prev_str
    trunk.str = '   |'
    printTree(root.left, trunk, False)

# 
# main starts here
#
def main():

    # Instantiate Binary Tree to hold the stars
    star_tree = Tree( "Star Catalog")

    with open('HabHYG.csv','r') as csvfile:
        lines = csv.reader(csvfile, delimiter=',')

        # skip header row
        next(csvfile)

        # get time in nanoseconds -- maybe OS-specific?
        # See https://docs.python.org/3/library/time.html
        t0 = time.perf_counter_ns()

        obs_processed = 0
        for row in lines:
            # habhvg, name, mag, spectral, habit, dist)
            this_star = Star(row[0], row[3], row[16], row[11], row[2], row[12] )
            star_tree.insert(this_star)
            obs_processed = obs_processed + 1

    t1 = time.perf_counter_ns() - t0
    print( "elapsed ms = " + str(t1 / 1000))

    print("obs_processed = " + str(obs_processed))

    # Your test and debug code here...
    printTree(star_tree.root, None, False)
    print()

if __name__ == "__main__":
    main()