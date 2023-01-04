# XY file template, format as following:
#Array type
#   i=   0        1       2       3       4       5     ...    n
#j       |        |       |       |       |       |     ...    |
#0      0_0      0_1     0_2     0_3     0_4      0_5   ...   0_n
#1      1_       1_1     1_2     1_3     1_4      1_5   ...   1_n
#2      2_       2_2     2_2     2_3     2_4      2_5   ...   2_n
#3      3_       3_2     3_2     3_3
#4      4_       4_2     4_2
#5      5_       5_2     5_2
#9      ...       ...    ...
#10     n_        n_1    n_2     n_3                    ...  n_n


# Pad# is concated by row value and i index (column index)
# Pad Name is value of cell(i,j)

# Actualy, it's similar below:
"""
        1	    2	    3	        4	        5	        6	        7	    8	    9	        10	        11
1_	VSSHV	VDDHV	PZT<0>	        PZT<1>	    PZT<2>	    PZT<3>	    VDDHV	PZT<4>	    PZT<5>	    PZT<6>	    PZT<7>
2_	VSSHV	VDDHV	PZT<32>	        ZT<33>	    PZT<34>	    PZT<35>	    VDDHV	PZT<36>	    PZT<37>	    PZT<38>	    PZT<39>
3_	VSSHV	VDDHV	PZT<64>	        PZT<65>	    PZT<66>	    PZT<67>	    VDDHV	PZT<68>	    PZT<69>	    PZT<70>	    PZT<71>
4_	VSSHV	VDDHV	PZT<96>	        PZT<97>	    PZT<98>	    PZT<99>	    VDDHV	PZT<100>	PZT<101>	PZT<102>	PZT<103>
5_	VSSHV	VDDHV	PZT<128>        PZT<129>    PZT<130>	    PZT<131>	    VDDHV	PZT<132>	PZT<133>	PZT<134>	PZT<135>
6_	VSSHV	VDDHV	PZT<160>        PZT<161>    PZT<162>	    PZT<163>	    VDDHV	PZT<164>	PZT<165>	PZT<166>	PZT<167>
7_	VSSHV	VDDHV	PZT<192>        PZT<193>    PZT<194>	    PZT<195>	    VDDHV	PZT<196>	PZT<197>	PZT<198>	PZT<199>

"""
# Pad number is "1_1" and pad name is "VSSHV"

# How to change revision for numeric type
"""
ij_num          = 00 --> 99
ji_letter       = A --> Z and AA --> ZZ
"""

# How to calulate min pitch
"""
X = [0,1,2,3,4,5] 
Y = [0,1,2,3,4,5]
N = 6
Points = [
        [0,0],  P0
        [1,1],  P1
        [2,2],  P2
        [3,3],  P3
        [4,4],  P4
        [5,5],  P5
     i=0,j=i+j+1  i=0, j=j+i+1     i=0,j=2+1=4
loop i=0:        P0P1    P0P2            P0P3            P0P4   P0P5     -->list1-->min1
                i=1, j=2        
loop 1:         P1P2            P1P3            P1P4   P1P5     -->list1-->min2
loop 2:                         P2P3            P2P4   P2P5     -->list1-->min3
loop 3:                                         P3P4   P3P5   
loop 4:                                                P4P5     --->list1-->min4

list2 = (min1, min2, min3, min4)


"""

P = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]
N = 23992                         
g = 8                        
n = 23992//g = 2999            
n_rest = 23992%g = 0         
------------
g = 0 to 7
i = 0 to 2998
group0: P[0] --> P[1]  -->n = 2   i =   0  1   (g*n)+i = i
group1: P[2] --> P[3]  -->n = 2         2  3   (g*n)+i = (1*2) + i



group_rest: P[12] n_rest = 2   i = 0  1  (g*2 + n_rest)+i


exam: groups = 3, this mean there are 3 lists
distance  list1 to list2, list3

DISTANCE               groups_i   to   group_i+1
loop i = 0:  
                        P0              P0
                        P0              P1
                        ...             ...
                        P0              Pn

loop i = 1:             P1              P0
                        P1              P1
                        ...             ...
                        P1              Pn_2

loop n_1 = 1:           Pn_1            P0
                        Pn_1            P1
                        ...             ...
                        Pn_1            Pn_2      

example:        groups = 3 (0,1,2)
                list(i) to list(j = i + 1 to i = groups-1)

loop1, i=0:     list(0) to list(1, 2)
                P0_0    to P1_0

loop2, i=1:     list(1) to list(2)