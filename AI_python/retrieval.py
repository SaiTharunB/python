import FOON_class as FOON
import re
from collections import deque


def parse_foon_file(file):
    _file = open(file, 'r')
    functional_blocks = _file.read().split('//')
    func_list = []
    main_list = []

    for block in functional_blocks:
        func_list.append(block)
        inputs = []
        outputs = []
        input_output_list = []
        in_out = block.split('M')
        lines_in = in_out[0].splitlines()
        lines_out = in_out[-1].splitlines()
        inputs = parse_input_output(lines_in)
        outputs = parse_input_output(lines_out)

        input_output_list.append(inputs)
        input_output_list.append("M"+lines_out[0])
        input_output_list.append(outputs)
      
        main_list.append(input_output_list)
        input_output_list = []
        input_item_list = []
        output_item_list = []



    _file.close()
    return main_list

def parse_input_output(lines_in):
    inputs = []
    item = None
    for line in lines_in:
        if line.startswith("O"):
            # -- we have an Object already in consideration which we were appending states to:
            if item:
                inputs.append(item)

            # -- this is an Object node, get the Object identifier by splitting first instance of O
            objectParts = line.split("O")
            objectParts = objectParts[1].split("\t")

            # -- create a new object which is equal to the kitchenItem and add it to the list:
            item = FOON.Object(objectID=int(
                objectParts[0]), objectLabel=objectParts[1])

        elif line.startswith("S"):
            # -- get the Object's state identifier by splitting first instance of S
            stateParts = line.split("S")
            stateParts = stateParts[1].split("\t")
            stateParts = list(filter(None, stateParts))

            # -- check if this object is a container or has ingredients:
            container = None
            list_ingredients = []
            if len(stateParts) > 2:
                if '{' in stateParts[2]:
                    # NOTE: all ingredients are enclosed in curly brackets:
                    ingredients = [stateParts[2]]
                    ingredients = ingredients[0].split("{")
                    ingredients = ingredients[1].split("}")

                    # -- we then need to make sure that there are ingredients to be read.
                    if len(ingredients) > 0:
                        ingredients = ingredients[0].split(",")
                        for I in ingredients:
                            list_ingredients.append(I)
                elif '[' in stateParts[2]:
                    # NOTE: a container is enclosed in square brackets (e.g. in [bowl]):

                    container = stateParts[2].replace('[', '').replace(']', '')
                else:
                    print(' -- WARNING: possibly incorrect or unexpected extra entry in line ' +
                          str(lines_in.index(line)) + '? > ' + str(stateParts[2]))
                    pass

            item.addNewState(
                [int(stateParts[0]), stateParts[1], container])

            if list_ingredients:
                item.setIngredients(list_ingredients)
    

        else:
            pass
    inputs.append(item)
    inputs = list(filter(None, inputs))
    return inputs


def parse_file(file):
    _file = open(file, 'r')
    items = _file.read().splitlines()
    item = None
    item_list = []

    for line in items:
        if line.startswith("O"):
            # -- we have an Object already in consideration which we were appending states to:
            if item:
                item_list.append(item)

            # -- this is an Object node, get the Object identifier by splitting first instance of O
            objectParts = line.split("O")
            objectParts = objectParts[1].split("\t")

            # -- create a new object which is equal to the kitchenItem and add it to the list:
            item = FOON.Object(objectID=int(
                objectParts[0]), objectLabel=objectParts[1])

        elif line.startswith("S"):
            # -- get the Object's state identifier by splitting first instance of S
            stateParts = line.split("S")
            stateParts = stateParts[1].split("\t")
            stateParts = list(filter(None, stateParts))

            # -- check if this object is a container or has ingredients:
            container = None
            list_ingredients = []
            if len(stateParts) > 2:
                if '{' in stateParts[2]:
                    # NOTE: all ingredients are enclosed in curly brackets:
                    ingredients = [stateParts[2]]
                    ingredients = ingredients[0].split("{")
                    ingredients = ingredients[1].split("}")

                    # -- we then need to make sure that there are ingredients to be read.
                    if len(ingredients) > 0:
                        ingredients = ingredients[0].split(",")
                        for I in ingredients:
                            list_ingredients.append(I)
                elif '[' in stateParts[2]:
                    # NOTE: a container is enclosed in square brackets (e.g. in [bowl]):

                    container = stateParts[2].replace('[', '').replace(']', '')
                else:
                    print(' -- WARNING: possibly incorrect or unexpected extra entry in line ' +
                          str(items.index(line)) + '? > ' + str(stateParts[2]))
                    pass

            item.addNewState(
                [int(stateParts[0]), stateParts[1], container])

            if list_ingredients:
                item.setIngredients(list_ingredients)

        else:
            pass
    # endfor

    item_list.append(item)

    _file.close()  # -- Don't forget to close the file once we are done!
    return item_list
# enddef
def generate_hash(item):
    item_id=str(item.getObjectType()) 
    states_id=""
    for ids in item.getStatesList():
        states_id+=str(ids[0])
        if(ids[1] is not None):
            states_id+=ids[1]
        if(ids[2] is not None):
            states_id+=ids[2]
    item_id+=states_id
    # print(item_id)
    return item_id
def compare(item1,item2):
    item1_id=generate_hash(item1)
    item2_id=generate_hash(item2)
    return item1_id==item2_id
def node_in_kitchen(goal_node):
    kitchen_list=parse_file("kitchen.txt")
    flag=False
    for item in kitchen_list:
        if(compare(item,goal_node)):
            flag=True
            # item.printObject()
            # print("-------------------")
            # goal_node.printObject()
            # print("888888888888888888")
            break
    return flag
def heuristic_foon_search(blocks_list,goal_node):
    block_count=0
    found_flag=True
    blist={}
    for block in blocks_list:
                for item in block[2]:
                    found_flag=False
                    found_flag=compare(item,goal_node)
                    if(found_flag):
                        blist[block_count]=len(block[0])
                block_count+=1
    print(blist)
    return min_inputs(blist)



        
def foon_search(blocks_list,goal_node):
    block_count=0
    found_flag=True
    for block in blocks_list:
            if(found_flag):
                block_count+=1
                for item in block[2]:
                    found_flag=not compare(item,goal_node)
    # print(block_count)
    # block=blocks_list[block_count-1]
    # print(block)
    return block_count-1
def print_obj(item):
    string="O" + str(item.getObjectType()) + "\t" + item.getObjectLabel() 
    for x in range(len(item.getStatesList())):
        if "contains" in item.getStateLabel(x) or "ingredients" in item.getStateLabel(x):
                string+=str("\n"+
                    "S"
                    + str(item.getStateType(x))
                    + "\t"
                    + item.getStateLabel(x)
                    + "\t"
                    + item.getIngredientsText()
                )
        else:
            string+=str("\n"+
                    "S"
                    + str(item.getStateType(x))
                    + "\t"
                    + item.getStateLabel(x)
                    + (
                        str("\t " + "[" + str(item.getContainer(x)) + "]")
                        if item.getContainer(x)
                        else ""
                    )
            )
    return string+"\n"
def min_inputs(blist):
    minimum=1000000
    index=0   
    dict_index=0
    for key,value in blist.items():
        if(value<minimum):
            minimum=value
    for key,value in blist.items():
        if(minimum==value):
            return key
        dict_index+=1
        
def heuristic_search_block(blocks_list,goal_nodes):
    file_counter=1
    for goal_node in goal_nodes:
        q=deque()
        l=[]
        indexes=[]
        q.appendleft(goal_node)
        l.append(goal_node)
        file_name="search_heuristic"+str(file_counter)+".txt"
        f=open(file_name, 'w')
        while(len(q)>0):
            popped=q.pop()
            if(not node_in_kitchen(popped)):
                index=heuristic_foon_search(blocks_list,popped)
                
                if index not in indexes:
                    indexes.append(index)
                    for inputs in blocks_list[index][0]:
                        if inputs not in l:
                            q.appendleft(inputs)
                            l.append(inputs)
                    for i in blocks_list[index]:
                        # for j in i:
                        #     if not isinstance(j,str):
                        #         print_obj(j)
                        flag=True
                        for j in i:
                            if not isinstance(j,str):
                                f.write(print_obj(j))
                            else:
                                if(flag):
                                    f.write(i+"\n")
                                    flag=False
                    f.write("// \n")
            else:
                #  print("in kitchen")
                pass
                # print(item.getObjectType())
                # print(str(id(item)) + " "+str(id(goal_node)))
                # print(id(item))
        f.close()
        file_counter+=1

            

def search_block(blocks_list,goal_nodes):
    file_counter=1
    for goal_node in goal_nodes:
        q=deque()
        l=[]
        indexes=[]
        q.appendleft(goal_node)
        l.append(goal_node)
        # for i in blocks_list[71]:
        #     for j in i:
        #         if not isinstance(j,str):
        #             j.printObject()
        file_name="search"+str(file_counter)+".txt"
        f=open(file_name, 'w')
        while(len(q)>0):
            popped=q.pop()
            
            if(not node_in_kitchen(popped)):
                index=foon_search(blocks_list,popped)
                
                if index not in indexes:
                    indexes.append(index)
                    for inputs in blocks_list[index][0]:
                        if inputs not in l:
                            q.appendleft(inputs)
                            l.append(inputs)
                    for i in blocks_list[index]:
                        # for j in i:
                        #     if not isinstance(j,str):
                        #         print_obj(j)
                        flag=True
                        for j in i:
                            if not isinstance(j,str):
                                f.write(print_obj(j))
                            else:
                                if(flag):
                                    f.write(i+"\n")
                                    flag=False
                    f.write("// \n")
            else:
                #  print("in kitchen")
                pass
                # print(item.getObjectType())
                # print(str(id(item)) + " "+str(id(goal_node)))
                # print(id(item))
        f.close()
        file_counter+=1
            





if __name__ == '__main__':
    functional_blocks = []
    # kitchen_items = parse_file('kitchen.txt')
    #
    # for item in kitchen_items:
    #     item.printObject()
    #     print()

    goal_nodes = parse_file('goal_nodes.txt')
    
    # for node in goal_nodes:
    #     node.printObject()
    #     print()

    functional_blocks = parse_foon_file('FOON.txt')
    search_block(functional_blocks,goal_nodes)
    heuristic_search_block(functional_blocks,goal_nodes)
    # print(functional_blocks)
    # for node in functional_blocks:
    #     for k in node:
    #         for m in k:
    #             m.printObject()
    # q1=deque()
    # q1.appendleft(1)
    # q1.appendleft(2)
    # q1.appendleft(3)
    # print(q1.pop())
    # print(q1.pop())
    # print(q1.pop())

