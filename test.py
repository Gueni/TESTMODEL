

# lambda for normal sweepmatrix and for sensitivity sweepmatrix with nominals
from collections import OrderedDict

to_dict = lambda Xs: OrderedDict((f"X{i+1}", v) for i, v in enumerate(Xs))

Xs = [[35,2,3,6,5],[45,50],[55,60],[65,70],[75,80],[85],[95],[0],[0],[0]]

result = to_dict(Xs)
print(result)

#-----------------------------------------------------------------------------
#