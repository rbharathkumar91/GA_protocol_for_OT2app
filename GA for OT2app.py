#!/usr/bin/env python
# coding: utf-8

# In[7]:


import json

from opentrons import protocol_api
metadata = {
    'protocolName': 'Glycated albumin_BKR_p20',
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
    FAplate = protocol.load_labware('grenier_96_wellplate_300ul', location='8')
    
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
    
    
    
    #Tris Formate reservoir to dilution plate
    
    left_pipette.starting_tip = tiprack300_1.well('A1')
    left_pipette.pick_up_tip()
    for i in range(12):
        left_pipette.transfer (300, Reservoir.columns_by_name()['1'], Dilutionplate.columns()[i], new_tip='never', mix_before= (1,250),blow_out=True,
    blowout_location='destination well')
    left_pipette.return_tip()   
    
    
    
    #Plasma plate to dilution plate
    right_pipette.starting_tip = tiprack20_1.well('A1')
    for i in range(12):
        right_pipette.transfer (2.5, Plasmaplate.columns()[i], Dilutionplate.columns()[i], new_tip='always', mix_before= (1,10), mix_after=(2,15),trash=True)
     
    
    #well bottom clearances
    left_pipette.well_bottom_clearance.aspirate = 3.9
    left_pipette.well_bottom_clearance.dispense = 3.9
    right_pipette.well_bottom_clearance.aspirate= 4
    right_pipette.well_bottom_clearance.dispense= 1.3

    #water reservoir to digestion plate
    
    left_pipette.starting_tip = tiprack300_1.well('A2')
    left_pipette.pick_up_tip()
   
    left_pipette.distribute(27, Reservoir.columns_by_name()['2'], [Digestionplate.columns_by_name()[column] for column in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']],new_tip='never',trash=False)
    left_pipette.return_tip() 
    
    
    
    
    #trypsin to digestion plate
   
    right_pipette.starting_tip = tiprack20_2.well('A1')
    right_pipette.pick_up_tip()
    for i in range(12):
        right_pipette.transfer (10, Trypsinplate.columns_by_name()['1'], Digestionplate.columns()[i], new_tip='never', mix_before= (1,15),blow_out=True,
    blowout_location='destination well')
    right_pipette.return_tip() 
    
    #well bottom clearances
    left_pipette.well_bottom_clearance.aspirate = 3.3
    left_pipette.well_bottom_clearance.dispense = 3.9
    right_pipette.well_bottom_clearance.aspirate= 1.3
    right_pipette.well_bottom_clearance.dispense= 2  
    
    #Dilution plate to digestion plate
    
    left_pipette.starting_tip = tiprack300_2.well('A1')
   
    for i in range(12):
        left_pipette.transfer (20, Dilutionplate.columns()[i], Digestionplate.columns()[i], new_tip='always', mix_before= (2,180),air_gap=20,blow_out=True,
    blowout_location='destination well',trash=False) 
    
    #ACN to digestion plate
    
    left_pipette.starting_tip = tiprack300_1.well('A3')
    left_pipette.pick_up_tip()
   
    for i in range(12):
        left_pipette.transfer (63,  Reservoir.columns_by_name()['3'], Digestionplate.columns()[i], new_tip='never', mix_before= (1,100),blow_out=True,
    blowout_location='destination well',air_gap=20)
    left_pipette.return_tip()
    
    #Mix everthing in digestion plate
    left_pipette.well_bottom_clearance.aspirate = 3.3
    left_pipette.well_bottom_clearance.dispense = 3.6
    
    left_pipette.reset_tipracks()
    left_pipette.starting_tip = tiprack300_2.well('A1')
    location=['A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12']
    
    for i in location:
        left_pipette.pick_up_tip()
        left_pipette.mix (2, 90, Digestionplate[i])
        left_pipette.blow_out(Digestionplate[i])
        left_pipette.return_tip()
        

    #well bottom clearances
    left_pipette.well_bottom_clearance.aspirate = 3.9
    left_pipette.well_bottom_clearance.dispense = 3.9
    right_pipette.well_bottom_clearance.aspirate= 1.3
    right_pipette.well_bottom_clearance.dispense= 1.3
    
    #4% FA from reservoir to FA plate
    left_pipette.starting_tip = tiprack300_1.well('A4')
    left_pipette.pick_up_tip()
    for i in range(12):
        left_pipette.transfer (250, Reservoir.columns_by_name()['4'], FAplate.columns()[i], new_tip='never', mix_before= (1,250))
    left_pipette.return_tip()  
    
    
    
    
    
    
    #homing the robot
    protocol.home()
    
    
    #pausing for 54 min
    protocol.delay(minutes=54)        
    
    #well bottom clearances
    left_pipette.well_bottom_clearance.aspirate = 3.5
    left_pipette.well_bottom_clearance.dispense = 3.5
    right_pipette.well_bottom_clearance.aspirate= 1.3
    right_pipette.well_bottom_clearance.dispense= 2
    
    #Quenching the digestion
    left_pipette.reset_tipracks()
    left_pipette.starting_tip = tiprack300_2.well('A1')
   
    for i in range(12):
        left_pipette.transfer (20, FAplate.columns()[i], Digestionplate.columns()[i], new_tip='always', mix_before= (1,40), mix_after=(2,90),blow_out=True,
    blowout_location='destination well', trash=False)
      
        
    
    #homing the robot
    protocol.home()
    
    


# In[ ]:




