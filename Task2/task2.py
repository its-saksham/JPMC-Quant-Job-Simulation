from datetime import date
from typing import List, Tuple
from math import ceil

def commodity_storage(
    injections:List[Tuple],
    withdrawals: List[Tuple],
    del_V: float,
    V_max : float,
    S: float,
)->float:
    Owner_Rate=0.005
    Transport_cost =50000
    del_V =volume_rate
    C = Transport_cost+ Owner_Rate*del_V
    
    contracts = injections + withdrawals
    contracts= sorted(contracts, key=lambda x: x[0])
    start_date = contracts[0][0]
    end_date = contracts[-1][0]
    delta_T = end_date -start_date
    T_days = delta_T.days
    T_months = ceil(T_days/30)
    
    J_net =0.0
    I_net =0.0
    V=0.0
    
    for contract in contracts:
        date, price, contract_type = contract
        if contract_type=='inject':
            if V<= V_max +del_V:
                I_net+= price*del_V+C
                V+=del_V
            else:
                print(f'Skipping contract with date {date} as volume of {V} exceeds the maximum capacity of {V_max}.')
        
        elif contract_type=='withdraw':
            if V>=del_V:
                J_net +=price*del_V-C
                V-=del_V
            else:
                print(f'Skipping contract with date{date} as volume of {V} is too low.')
        
        print(f'We {contract_type} {del_V:.2f} MMBtu of natural gas  at ${price:.2f} on {date} with {V:.2f} MMBtu gas left in storage.\n')
        
    contract_value = J_net -I_net-S *T_months
    return contract_value
injections =[
    (date(2022,1,1),200,'inject'),
    (date(2022,2,1),21,'inject'),
    (date(2022,2,21),18.5,'inject'),
    (date(2022,4,1),22,'inject')
]
withdrawals =[
    (date(2022,1,27),139,'withdraw'),
    (date(2022,2,15),1449,'withdraw'),
    (date(2022,3,20),121,'withdraw'),
    (date(2022,6,1),50,'withdraw')
]
volume_rate = 100000
storage_cost_rate = 10000
max_storage_volume = 500000
result = commodity_storage(injections, withdrawals,volume_rate, max_storage_volume,storage_cost_rate)

print(f'The value of this contract is ${result:.2f}')