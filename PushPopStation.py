# Solution Code for PushPopStation Project
# Coder - ¥0d@the©0d@


def train_check(train_arriving:str, train_departing:str, mode=0):
    '''
    Function to check for validity of pop/push operation to get desired sequence.
    
    Input parameters are 2 strings (coach numbers separated by spaces in each string) representing train sequences, first being arriving train and then the departing train.
    There is a third parameter, passing arguments to which is optional (default is 0). 
    If nonzero argument is passed through the third parameter PUSH/POP sequence is also returned as a list in addition to the default return of validity.   
    '''
    train_arr = train_arriving.split() # pushed sequence
    train_dep = train_departing.split() # popped sequence
    # stack initliazation 
    train_stn = [] # this is our stack
    coaches_popped = 0 # count of coaches popped from station
    train_size = len(train_arr)
    coaches_in_station = 0
    top_coach_stn = None
    station_is_empty = True
    op_sequence = []
    for coach in train_arr:
        train_stn.append(coach) # stack PUSH 
        coaches_in_station += 1 
        op_sequence.append(f"PUSH: {coach}")
        top_coach_stn = coach # last item of our stack
        station_is_empty = False if coaches_in_station else True
        # checking if the top coach in station is the coach to be popped to the track
        while (not station_is_empty) and (coaches_popped < train_size) and (top_coach_stn == train_dep[coaches_popped]):
            coach_pop = train_stn.pop() # stack POP
            op_sequence.append(f"POP: {coach_pop}")
            coaches_popped += 1 
            coaches_in_station -= 1
            station_is_empty = False if coaches_in_station else True
            if not station_is_empty: 
                top_coach_stn = train_stn[-1] 
            if coaches_popped == train_size: 
                break
    # validity is 'True' if all coaches in the train are popped
    validity = (station_is_empty) and (coaches_popped == train_size)
    if mode==0:
        return validity
    else:
        return validity, op_sequence

def get_input_block():
    '''function to get user input block/(s)'''
    count_zero = 0
    user_input_data = []
    print("Enter the Sequence - input 0+\\n twice successively to quit")
    while count_zero < 2:
        user = input(":")
        user_input_data.append(user)
        size = len(user_input_data[-1])
        if  (size == 1 and int(user) == 0): 
            count_zero += 1
        elif  (size == 1 and int(user) != 0):
            train_size = int(user) 
            count_zero = 0
        else:
            train_sequence = user_input_data[-1].split(",")
            train_validity = all((int(coach) in range(1, train_size+1) and train_sequence.count(coach)==1) for coach in train_sequence)
            if train_validity:
                continue
            else:
                inv_user = user_input_data.pop()
                print(f"Invalid sequence {inv_user} - rejected and ignored")
    # rationlizing sequence data for subsequent input into file (removing commas from sequences)
    user_input_data = [item.replace(",", " ") for item in user_input_data]
    return user_input_data

def marshall_coaches(block:list):
    '''function for marshalling operation'''
    zero_flag = 0 # exit check, two consecutives zeroes will exit prog
    train_validity = None
    N = 0 # trainsize
    marshalling_list = []
    for train_seq in block:
        # conditions to check for train size, coach permutations and end of block
        if zero_flag==2:
            break
        elif train_seq.isnumeric() and int(train_seq)==0:
            zero_flag += 1
            train_validity = " " # space between two train sequence blocks
        elif train_seq.isnumeric() and int(train_seq)>0:
            N = int(train_seq) # size of train
            zero_flag = 0
            train_validity = " " # space between two train sequence blocks
            train_arriving = " ".join([str(x) for x in range(1, N+1)])
        else:
            train_validity = train_check(train_arriving, train_seq)
        # list updation    
        marshalling_list.append(train_validity)
    return marshalling_list

def show_block(anylist:list):
    '''function to display any list block'''
    for item in anylist:
        print(item)
    return

def update_input_file(a_list_of_string:list):
    '''function to write/update to the input file'''
    with open("train_input.txt", "r+") as myfile:
        chk_list = myfile.readlines()
        last_item = chk_list[-1]
        myfile.seek(myfile.tell()-len(last_item)-2)
        for item in a_list_of_string:
            myfile.write(item+"\n")
    return

def read_input_file():
    '''function to read input file'''
    with open("train_input.txt", "r+") as myfile:
        blocks = myfile.readlines()
    blocks = [item.strip() for item in blocks]
    return blocks

def update_output_file(validity_list: list):
    '''function for writing the marshalling validation to output file '''
    with open("train_output.txt", "w") as myfile:
        for item in validity_list:
            if item == True:
                myfile.write("YES\n")
            elif item == False:
                myfile.write("NO\n")
            else:
                myfile.write("\n")
    print("File operation completed !")
    return


def main():

    # OPTIONAL/ADDITIONAL
    # - user generated sequence input
    # sequence_block = get_input_block()  
    
    # OPTIONAL/ADDITIONAL
    # - user input updated to inputfile 
    # update_input_file(sequence_block)  
    
    # reading input file ("train_input.txt")
    sequence_block = read_input_file()

    # marshalling operation and validation
    marshalling_list = marshall_coaches(sequence_block)
    
    # writing validation results to the output file
    update_output_file(marshalling_list)

if __name__ == "__main__":
    main()


