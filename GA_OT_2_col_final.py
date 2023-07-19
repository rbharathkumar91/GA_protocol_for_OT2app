#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
import time
from datetime import datetime

from opentrons import protocol_api
metadata = {
    'protocolName': 'Glycated albumin_BKR_p20_col_12_final',
    'author': 'Name <bkr@evosep.com>',
    'description': 'Glycated Albumin protocol using the OT-2',
    'apiLevel': '2.12'
}
def run(protocol):
    
    
    
    #homing 
    protocol.home()

    # labware
   
    
    
    Trypsinplate =protocol.load_labware('opentrons_96_pcr_adapter_nest_wellplate_100ul_pcr_full_skirt', location='5') 
    tiprack300_1 =protocol.load_labware('opentrons_96_tiprack_300ul', location='10')
    tiprack300_2 =protocol.load_labware('opentrons_96_tiprack_300ul', location='1')
    tiprack20_1 =protocol.load_labware('opentrons_96_tiprack_20ul', location='2')
    tiprack20_2 =protocol.load_labware('opentrons_96_tiprack_20ul', location='11')
    Plasmaplate = protocol.load_labware('grenier_96_wellplate_300ul', location='3')
    Dilutionplate = protocol.load_labware('grenier_96_wellplate_300ul', location='6')
    Reservoir = protocol.load_labware('homemade_4_reservoir_40000ul',location='9' )
    Digestionplate = protocol.load_labware('grenier_96_wellplate_300ul', location='7')    
   
    
    # pipettes
    left_pipette = protocol.load_instrument(
         'p300_multi_gen2', mount='left', tip_racks=[tiprack300_1,tiprack300_2])
    right_pipette = protocol.load_instrument(
         'p20_multi_gen2', mount='right', tip_racks=[tiprack20_1,tiprack20_2])
    
    left_pipette.flow_rate.aspirate = 80
    left_pipette.flow_rate.dispense = 80
    right_pipette.flow_rate.aspirate = 6
    right_pipette.flow_rate.dispense = 7.6
    left_pipette.default_speed = 300
    right_pipette.default_speed = 300
    
    
    #well bottom clearances
    left_pipette.well_bottom_clearance.aspirate = 3.3
    left_pipette.well_bottom_clearance.dispense = 3.7
    right_pipette.well_bottom_clearance.aspirate= 0.9
    right_pipette.well_bottom_clearance.dispense= 2
    
    #Column number
    col=12
    
    
    
    #Tris Formate reservoir to dilution plate
   
    
    left_pipette.starting_tip = tiprack300_1.well('A1')
    left_pipette.pick_up_tip()
    start_time=datetime.now()
    
    for i in range(col):
        left_pipette.transfer (300, Reservoir.columns_by_name()['1'], Dilutionplate.columns()[i], new_tip='never', mix_before= (1,250),blow_out=True,
    blowout_location='destination well')
    
    
    end_time=datetime.now()
    diff=end_time-start_time
    left_pipette.return_tip()   
    protocol.comment(f'The start time is  {start_time}')
    elapsed_time=diff.total_seconds()
    protocol.comment(f'The elapsed time is  {elapsed_time}')
    
    #Plasma plate to dilution plate
    start_time=time.time()
    protocol.comment(f'The start time is  {start_time}')
    right_pipette.starting_tip = tiprack20_1.well('A1')
    for i in range(col):
        right_pipette.transfer (2.5, Plasmaplate.columns()[i], Dilutionplate.columns()[i], new_tip='always', mix_before= (1,10), mix_after=(2,15),trash=True)
     
    
    end_time=time.time()
    protocol.comment(f'The end time is  {end_time}')
    
    
    #well bottom clearances
    left_pipette.well_bottom_clearance.aspirate = 3.1
    left_pipette.well_bottom_clearance.dispense = 2.8
    right_pipette.well_bottom_clearance.aspirate= 2.2
    right_pipette.well_bottom_clearance.dispense= 1.0

    #water reservoir to digestion plate
    
    left_pipette.starting_tip = tiprack300_1.well('A2')
    left_pipette.pick_up_tip()
    
    for i in range(col):
        left_pipette.transfer (27, Reservoir.columns_by_name()['2'], Digestionplate.columns()[i], new_tip='never', mix_before= (1,250),blow_out=True,
    blowout_location='destination well')
    left_pipette.return_tip() 
    
    
    
    
    #trypsin to digestion plate
    
    right_pipette.starting_tip = tiprack20_2.well('A1')
    
    for i in range(col):
        right_pipette.transfer (10, Trypsinplate.columns_by_name()['1'], Digestionplate.columns()[i],new_tip='always', mix_before= (1,15),blow_out=True,
    blowout_location='destination well',trash=False)
    
    
    #well bottom clearances
    left_pipette.well_bottom_clearance.aspirate = 3.3
    left_pipette.well_bottom_clearance.dispense = 2.8
    right_pipette.well_bottom_clearance.aspirate= 1.3
    right_pipette.well_bottom_clearance.dispense= 2  
    
    #Dilution plate to digestion plate
    start_time=time.time()
    protocol.comment(f'The start time is  {start_time}')
    left_pipette.starting_tip = tiprack300_2.well('A1')
   
    for i in range(col):
        left_pipette.transfer (20, Dilutionplate.columns()[i], Digestionplate.columns()[i], new_tip='always', mix_before= (2,180),blow_out=True,
    blowout_location='destination well',trash=False) 
    
    end_time=time.time()
    protocol.comment(f'The end time is  {end_time}')
    used_time_1=end_time-start_time
    protocol.comment(f'Dilution plate to digestion transfer time in seconds is {used_time_1}')
    
    #well bottom clearances
    left_pipette.well_bottom_clearance.aspirate = 3.3
    left_pipette.well_bottom_clearance.dispense = 3.7
    right_pipette.well_bottom_clearance.aspirate= 1.3
    right_pipette.well_bottom_clearance.dispense= 2 
    
    #ACN to digestion plate
    start_time=time.time()
    protocol.comment(f'The start time is  {start_time}')
    left_pipette.starting_tip = tiprack300_1.well('A3')
    left_pipette.pick_up_tip()
   
    for i in range(col):
        left_pipette.transfer (63,  Reservoir.columns_by_name()['3'], Digestionplate.columns()[i], new_tip='never', mix_before= (1,100),blow_out=True,
    blowout_location='destination well',air_gap=20)
    left_pipette.return_tip()
    
    end_time=time.time()
    protocol.comment(f'The end time is  {end_time}')
    used_time_2=end_time-start_time
    protocol.comment(f'Acetonitrile reservoir to digestion transfer time in seconds is {used_time_2}')
    
    #Mix everthing in digestion plate
    start_time=time.time()
    protocol.comment(f'The start time is  {start_time}')
    left_pipette.well_bottom_clearance.aspirate = 2.6
    left_pipette.well_bottom_clearance.dispense = 3.2
    
    left_pipette.reset_tipracks()
    left_pipette.starting_tip = tiprack300_2.well('A1')
    location=['A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12']
    
    for i in range(col):
        pos=location[i]
        left_pipette.pick_up_tip()
        left_pipette.mix (2, 90, Digestionplate[pos])
        left_pipette.blow_out(Digestionplate[pos])
        left_pipette.return_tip()

    end_time=time.time()
    protocol.comment(f'The end time is  {end_time}')
    used_time_3=end_time-start_time
    protocol.comment(f'Mixing of all contents in digestion plate took {used_time_3}')
    
    #homing the robot
  
    protocol.home()
    
    
    #pausing elapsed time
    total_used_time=used_time_1+used_time_2+used_time_3
    protocol.comment(f'Total used time is {total_used_time}')
    protocol.delay(seconds=4200-total_used_time)        
    
    #Quenching digestion
    left_pipette.well_bottom_clearance.aspirate = 3.3
    left_pipette.well_bottom_clearance.dispense = 3.7
    right_pipette.well_bottom_clearance.aspirate= 1.3
    right_pipette.well_bottom_clearance.dispense= 1.3
    
    
    left_pipette.starting_tip = tiprack300_1.well('A4')
    left_pipette.pick_up_tip()
    for i in range(col):
        left_pipette.transfer (25, Reservoir.columns_by_name()['4'], Digestionplate.columns()[i], new_tip='never', mix_before= (1,250))
    left_pipette.return_tip()  
    
    #Mix everthing in digestion plate
    left_pipette.well_bottom_clearance.aspirate = 2.6
    left_pipette.well_bottom_clearance.dispense = 3.2
    
    left_pipette.reset_tipracks()
    left_pipette.starting_tip = tiprack300_2.well('A1')
    location=['A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12']
    
    for i in range(col):
        pos=location[i]
        left_pipette.pick_up_tip()
        left_pipette.mix (2, 90, Digestionplate[pos])
        left_pipette.blow_out(Digestionplate[pos])
        left_pipette.return_tip()
    
    #homing the robot
    protocol.home()
    
    

