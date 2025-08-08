#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
#?                            ____   _    ____      _    __  __   ____  ____   ___   ____ _____ ____ ____ ___ _   _  ____
#?                           |  _ \ / \  |  _ \    / \  |  \/  | |  _ \|  _ \ / _ \ / ___| ____/ ___/ ___|_ _| \ | |/ ___|
#?                           | |_) / _ \ | |_) |  / _ \ | |\/| | | |_) | |_) | | | | |   |  _| \___ \___ \| ||  \| | |  _
#?                           |  __/ ___ \|  _ <  / ___ \| |  | | |  __/|  _ <| |_| | |___| |___ ___) |__) | || |\  | |_| |
#?                           |_| /_/   \_\_| \_\/_/   \_\_|  |_| |_|   |_| \_\\___/ \____|_____|____/____/___|_| \_|\____|
#?
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------

import os,sys
sys.path.insert(1,os.getcwd() + '/Script/assets')
import Dependencies as dp

class ParamProcess:
    def __init__(self):
        """Initialize the ParamProcess class with essential post-processing and simulation utilities.
        
        The constructor sets up two key components:
        - postProcessing: An instance of Processing class from Dependencies for data extraction and manipulation
        - simutil: An instance of SimulationUtils from Dependencies for simulation-related operations
        
        These components are used throughout the class methods for various parameter processing tasks.
        """
        self.postProcessing     =   dp.PP.Processing()
        self.simutil            =   dp.sutl.SimulationUtils()

    def MOSFETcaps(self,path,switch_name,type):
        """Process MOSFET capacitance characteristics from simulation data to extract key parameters.
        
        This method:
        1. Reads MOSFET capacitance vs voltage data from specified file
        2. Calculates charge (Qoss) by integrating capacitance over voltage
        3. Computes energy (Eoss) by integrating (V*C) over voltage
        4. Derives time-effective (Coss_tr) and energy-effective (Coss_er) capacitances
        5. Returns comprehensive capacitance characterization data
        
        Args:
            path (str): Directory path containing the switch characterization files
            switch_name (str): Identifier for the specific MOSFET switch
            type (str): Suffix indicating capacitance type ('Coss', 'Ciss', 'Crss')
            
        Returns:
            tuple: Five processed data arrays:
                - Cmos: [Vds, C] original capacitance vs voltage
                - Qmos: Integrated charge vs voltage
                - Emos: Integrated energy vs voltage
                - Cmos_tr: Time-effective capacitance (Qoss/ΔV)
                - Cmos_er: Energy-effective capacitance (2Eoss/ΔV²)
                
        Note:
            All capacitance values are converted to Farads (×1e-12)
            Charge values are in Coulombs (×1e-12)
            Energy values are in Joules (×1e-12)
        """
        switch 	    =	path + switch_name + type

        Cmos	    =	self.postProcessing.extractArrays(switch)
        Vds_Cmos    =   [Cmos[0], (dp.np.multiply(dp.np.array(Cmos[0]),dp.np.array(Cmos[1]))).tolist()]

        Qmos	    =	[]
        Emos        =   []

        for i in range(len(Cmos[0])):
            idx                 =   self.postProcessing.get_index(Cmos,Cmos[0][i],0)
            capacity            =   (dp.np.array(Cmos)[:,0:idx+1]).tolist()
            charge              =   float(dp.np.trapz(capacity[1], x = capacity[0]))
            Qmos.append(dp.np.around(charge,3))

            idx                 =   self.postProcessing.get_index(Vds_Cmos,Vds_Cmos[0][i],0)
            capacityVoltage     =   (dp.np.array(Vds_Cmos)[:,0:idx+1]).tolist()
            energy              =   float(dp.np.trapz(capacityVoltage[1], x = capacityVoltage[0]))
            Emos.append(dp.np.around(energy,3))

        Cmos[1]     =   dp.np.array(Cmos[1])*1e-12
        Cmos        =   dp.np.array(Cmos)
        Qmos        =   dp.np.array(Qmos)*1e-12
        Emos        =   dp.np.array(Emos)*1e-12

        Cmos_tr     =   (Qmos[1:]/(Cmos[0][1:]-Cmos[0][0])).tolist()
        Cmos_er     =   (2*Emos[1:]/(Cmos[0][1:]**2-Cmos[0][0]**2)).tolist()
        Cmos_tr.insert(0,0)
        Cmos_er.insert(0,0)

        Cmos        =   Cmos.tolist()
        Qmos        =   Qmos.tolist()
        Emos        =   Emos.tolist()

        return Cmos,Qmos,Emos,Cmos_tr,Cmos_er

    def Forward_Transfer_data(self,switchesTransferPath,switch_name):
        """Extract and format MOSFET forward transfer characteristics (Vds vs Ids at various Vgs).
        
        Processes raw simulation data to:
        1. Extract drain-source voltage (Vds) sweep points
        2. Organize drain current (Ids) measurements for each gate voltage (Vgs)
        3. Transpose data for easier access to Ids vs Vds at fixed Vgs
        
        Args:
            switchesTransferPath (str): Path to transfer characteristics data files
            switch_name (str): Identifier for the specific MOSFET
            
        Returns:
            tuple: Two arrays:
                - Vdsvec: List of drain-source voltage points
                - Idsvec: 2D list where each sublist contains Ids values for a fixed Vgs
        """
        Transfer        =   switchesTransferPath + switch_name +'_Transfer'
        Transfer_vec    =   self.postProcessing.extractArrays(Transfer)

        Vdsvec          =   Transfer_vec[0]

        Idsvec          =   dp.np.array(Transfer_vec[1:])
        Idsvec          =   ((dp.np.array(Idsvec)).T).tolist()

        return Vdsvec,Idsvec

    def MOSFETenergies(self,path,switch_name,type):
        """Process MOSFET switching energy loss data into 3D lookup table format.
        
        Organizes energy loss data (Eon/Eoff) into a 3D structure indexed by:
        1. Voltage (Vds)
        2. Current (Ids)
        3. Gate voltage (Vgs)
        
        Creates MATLAB-compatible concatenation command for easy data import.
        
        Args:
            path (str): Directory containing energy loss data files
            switch_name (str): MOSFET identifier
            type (str): Energy type ('Eon' or 'Eoff')
            
        Returns:
            tuple: Three elements:
                - current: List of current values (Ids)
                - cat: MATLAB concatenation command string for 3D array
                - Emos: 3D energy loss data [Vds][Ids][Vgs]
                
        Note:
            Energy values are converted from µJ to J (×1e-6)
        """
        switch 	    =	path + switch_name +type
        EmosData    =   self.postProcessing.extractArrays(switch)
        EmosData    =   dp.np.array(EmosData)
        EmosData_T  =   EmosData[1:].T

        current     =   (dp.np.unique(EmosData[0])).tolist()

        volt_length =   (EmosData[0].tolist()).count(EmosData[0][0])
        gate_length =   len(EmosData)-1
        curr_length =   len(current)
        curr_idx    =   dp.np.array(list(range(0,curr_length)))

        LuT_3D      =   dp.np.empty((volt_length,curr_length,gate_length))
        cat                 =   'cat(3'
        for i in range(volt_length):
            indices             =   i*curr_length+curr_idx
            LuT_3D[:][:][i]     =   (EmosData_T[indices,:] - EmosData_T[0][0])*1e-6
            cat                 =   cat  + ',' + 'LuT_3D' + '(:,:,' + str(i+1) + ')'
        cat                     =   cat  + ')'
        Emos                    =   LuT_3D.tolist()

        return current,cat,Emos

    def MOSFETrdson(self,path,switch_name,type):
        """Process MOSFET on-resistance (Rds_on) characterization data.
        
        Extracts and formats Rds_on vs:
        1. Drain current (Ids)
        2. Gate voltage (Vgs)
        3. Temperature (Tj)
        
        Args:
            path (str): Directory containing Rds_on data files
            switch_name (str): MOSFET identifier
            type (str): Data type identifier
            
        Returns:
            tuple: Two arrays:
                - Rvec: 2D list of Rds_on values (rows: conditions, columns: sweeps)
                - Xvec: Corresponding independent variable values
        """
        Switch      =   path + switch_name + type
        R_X_Vec     =   self.postProcessing.extractArrays(Switch)
        R_X_Types   =   len(R_X_Vec)

        Rvec        =   []
        Xvec        =   []
        for i in range(R_X_Types//2):
            Xvec.append(R_X_Vec[i*2])
            Rvec.append(R_X_Vec[i*2+1])

        Rvec        =   ((dp.np.array(Rvec)).T).tolist()
        Xvec        =   ((dp.np.array(Xvec)).T).tolist()

        return Rvec,Xvec

    def DiodeVI_data(self,DiodeVIPath,diode_name):
        """Process diode forward IV characteristics from simulation data.
        
        Extracts and formats:
        1. Forward voltage (Vf) vs current (If) characteristics
        2. Multiple curves for different temperatures if available
        
        Args:
            DiodeVIPath (str): Path to diode IV data files
            diode_name (str): Diode identifier
            
        Returns:
            tuple: Two arrays:
                - Vvec: 2D list of voltage points (rows: temperatures, columns: current points)
                - Ivec: List of current sweep points
        """
        Diode       =   DiodeVIPath + diode_name + '_VI'
        V_I         =   self.postProcessing.extractArrays(Diode)
        Vvec        =   (((dp.np.array(V_I[1:]))).T).tolist()
        Ivec        =   (dp.np.array(V_I[0])).tolist()

        return Vvec,Ivec

    def Mags_CoreLoss_Data(self,TrafoCoreLossesPath,trafo_name):
        """Process transformer core loss data into 3D lookup table format.
        
        Organizes core loss data by:
        1. Temperature
        2. Magnetic flux density (B)
        3. Frequency
        
        Creates MATLAB-compatible concatenation command.
        
        Args:
            TrafoCoreLossesPath (str): Path to core loss data files
            trafo_name (str): Transformer identifier
            
        Returns:
            tuple: Three elements:
                - flux: List of flux density values (converted to MWb)
                - cat: MATLAB concatenation command
                - loss: 3D core loss data [temp][flux][freq]
        """
        Trafo       =   TrafoCoreLossesPath + trafo_name
        coreData    =   self.postProcessing.extractArrays(Trafo)
        coreData    =   dp.np.array(coreData)
        coreData_T  =   coreData[1:].T

        flux        =   ((dp.np.unique(coreData[0]))*1.0e-6/2.0).tolist()

        temp_length         =   (coreData[0].tolist()).count(coreData[0][0])
        voltage_length      =   len(coreData)-1
        flux_length         =   len(flux)
        flux_idx            =   dp.np.array(list(range(0,flux_length)))

        LuT_3D              =   dp.np.empty((temp_length,flux_length,voltage_length))
        cat                 =   'cat(3'
        for i in range(temp_length):
            indices             =   i*flux_length+flux_idx
            LuT_3D[:][:][i]     =   coreData_T[indices,:]
            cat                 =   cat  + ',' + 'LuT_3D' + '(:,:,' + str(i+1) + ')'
        cat                     =   cat  + ')'
        loss                    =   LuT_3D.tolist()

        return flux,cat,loss

    def Mags_FreqRes_Data(self,FreqResistancePath,mag_name):
        """Process frequency-dependent winding resistance data for magnetics.
        
        Extracts AC resistance vs frequency for:
        1. Multiple windings
        2. Multiple temperatures (if available)
        
        Args:
            FreqResistancePath (str): Path to frequency response data
            mag_name (list): List of winding identifiers
            
        Returns:
            tuple: Two arrays:
                - Fvec: Frequency points (converted to kHz)
                - Rvec: AC resistance values (converted to mΩ)
        """
        Rvec = []
        Fvec = []

        for i in range(len(mag_name)):
            Winding = FreqResistancePath + mag_name[i]
            R_F = self.postProcessing.extractArrays(Winding)

            R = ((dp.np.array(R_F[1:])) * 1e-3).tolist()
            F = ((dp.np.array(R_F[0])) * 1e3).tolist()

            Rvec.append(R)
            Fvec.append(F)

        return Fvec, Rvec

    def Mags_LI_Data(self,InductanceCurrentPath,mag_name):
        """Process inductance vs DC bias current characteristics.
        
        Extracts and formats:
        1. Inductance vs current curves
        2. Multiple curves for different temperatures if available
        
        Args:
            InductanceCurrentPath (str): Path to L-I data files
            mag_name (str): Magnetic component identifier
            
        Returns:
            tuple: Two arrays:
                - Ivec: DC current sweep points
                - Lvec: Inductance values (converted to Henry)
        """
        Mag         =   InductanceCurrentPath + mag_name
        L_I_Vec     =   self.postProcessing.extractArrays(Mag)

        Ivec        =   L_I_Vec[0]

        Lvec        =   dp.np.array(L_I_Vec[1:])
        Lvec        =   ((dp.np.array(Lvec)*1e-6).T).tolist()

        return Ivec,Lvec

    def linearDerating(self,X1,X2,Y1,Y2,Ymin,Ymax,X):
        """Calculate linearly interpolated derating factor with clamping.
        
        Implements:
        y = mX + b between (X1,Y1) and (X2,Y2)
        Clamped to [Ymin,Ymax] range
        
        Args:
            X1,X2: Independent variable range endpoints
            Y1,Y2: Dependent variable values at X1,X2
            Ymin,Ymax: Output clamping limits
            X: Evaluation point
            
        Returns:
            float: Interpolated and clamped derating factor
            
        Raises:
            ValueError: If X1 == X2 (division by zero)
        """
        m   =   (Y2 - Y1)/(X2 - X1)
        b   =   Y1 - m*X1

        Y   =   m*X + b

        Y   =   min(Y,Ymax)
        Y   =   max(Y,Ymin)

        return Y

    def scaledList(self,arrayList,scale=1.0):
        """Scale numerical values in nested list structure.
        
        Applies uniform scaling factor to all elements while preserving structure.
        Handles both regular lists and numpy arrays.
        
        Args:
            arrayList: Nested list/array structure containing numerical values
            scale: Multiplicative scaling factor (default=1.0)
            
        Returns:
            list: Scaled array with original structure, transposed
        """
        arrayList   =   ((dp.np.array(arrayList))).tolist()

        for i in range(len(arrayList)):
            if (isinstance(arrayList[i], (dp.np.ndarray))):
                tempList        =   (arrayList[i]*scale).tolist()
                arrayList[i]    =   tempList
            else:
                arrayList[i]    =   (dp.np.array(arrayList[i])*scale).tolist()

        arrayList = ((dp.np.array(arrayList)).T).tolist()
        return arrayList

    def getCoss(self,switch,blockingVoltage,time_energy):
        """Calculate effective output capacitance (Coss) at specified voltage.
        
        Computes either:
        1. Time-effective Coss (Qoss/ΔV) if time_energy=True
        2. Energy-effective Coss (2Eoss/ΔV²) if time_energy=False
        
        Args:
            switch (dict): MOSFET characteristics dictionary
            blockingVoltage (float): Evaluation voltage
            time_energy (bool): Calculation method selector
            
        Returns:
            float: Effective capacitance in Farads (rounded to 2 decimal places)
        """
        voltageVector   =   switch['Coss']['Vvec']
        CossVector      =   switch['Coss']['Cvec']
        QossVector      =   switch['Coss']['Qoss']
        EossVector      =   switch['Coss']['Eoss']

        Coss        =   [voltageVector, CossVector]
        Coss_idx    =   self.simutil.postProcessing.get_index(Coss,blockingVoltage,0)

        if (time_energy):
            Qoss        =   QossVector[Coss_idx]
            Coss_eff    =   Qoss/(Coss[0][Coss_idx]-Coss[0][0])
        else:
            Eoss        =   EossVector[Coss_idx]
            Coss_eff    =   2*Eoss/(Coss[0][Coss_idx]**2-Coss[0][0]**2)

        Coss_eff     =   round(Coss_eff*1e12, 2)*1e-12
        return Coss_eff

    def PrechargeILVref(self,V_snub,V_LV_OP,Np,Ns,fs,Lfilter,Lks,Lkp,I_C_max,ILVmax,tonsnubmin,Points):
        """Calculate precharge current reference for snubber circuit design.
        
        Determines maximum safe precharge current considering:
        1. Transformer turns ratio (Np/Ns)
        2. Leakage inductances
        3. Filter inductance
        4. Snubber capacitor current limits
        5. Minimum snubber turn-on time
        
        Args:
            V_snub: Snubber circuit voltage
            V_LV_OP: Low-side operating voltage
            Np,Ns: Primary/secondary turns
            fs: Switching frequency
            Lfilter: Output filter inductance
            Lks,Lkp: Secondary/primary leakage inductances
            I_C_max: Maximum capacitor current
            ILVmax: Maximum current index
            tonsnubmin: Minimum snubber on-time
            Points: Number of calculation points
            
        Returns:
            tuple: Three elements:
                - Vvec: Voltage vector
                - Ivec: Current reference vector
                - ton_snub_final: Final snubber on-time
        """
        ntr             =   Np/Ns
        L_leak_lv       =   (Lks+Lkp)/(ntr**2)
        Vvec            =   list(dp.np.linspace(0,V_LV_OP*ntr,Points))
        Ivec            =   dp.copy.deepcopy(Vvec)

        for V_HV in Vvec:
            for ILV in range(ILVmax+1):
                Duty        =   (V_snub-V_LV_OP)/(V_snub-V_HV/ntr)
                toff        =   (1-Duty)/(2*fs)
                ton_snub    =   pow(2*L_leak_lv*ILV*toff/(V_snub-V_HV/ntr),0.5)
                dI_LV       =   (V_snub-V_LV_OP)*toff/Lfilter
                ILV_peak    =   ILV + dI_LV/2
                Ipeak_snub  =   (V_snub-V_HV/ntr)*ton_snub/L_leak_lv
                IC_snub_P   =   pow((2*fs*((ILV_peak*ILV_peak*toff) + ((V_snub-V_LV_OP)*(V_snub-V_LV_OP)*pow(toff,3)/(3*Lfilter*Lfilter)) - (ILV_peak*(V_snub-V_LV_OP)*toff*toff/Lfilter))),0.5)
                IC_snub_N   =   Ipeak_snub* pow((2*fs*ton_snub/3),0.5)
                IC_snub_RMS =   pow((IC_snub_P*IC_snub_P)+(IC_snub_N*IC_snub_N),0.5)

                if(IC_snub_RMS < I_C_max):
                    Iref1   =    ILV

            if(V_HV == 0):
                if(ton_snub < tonsnubmin):
                    ton_snub_final  =   tonsnubmin
                else:
                    ton_snub_final  =   ton_snub
            Ivec[Vvec.index(V_HV)]  =   Iref1

        Vvec                        =   (dp.np.array(Vvec).astype(int)).tolist()
        return Vvec,Ivec,ton_snub_final

    def dcdcAverageModelCalculate(self,ModelVars):
        """Calculate parameters for DC-DC converter averaged model.
        
        Processes component characteristics to derive:
        1. Equivalent resistances
        2. Transformer parameters
        3. Snubber network values
        4. Small-signal model coefficients
        
        Args:
            ModelVars (dict): Complete converter parameter dictionary
            
        Returns:
            dict: Averaged model parameters including:
                - Resistances (Rds_on, Rp, Rs, etc.)
                - Inductances (Lk, Lf)
                - Switching parameters (d, Fs, Ts)
                - Snubber networks (Csnub, Rsnub)
                - Small-signal matrices (Ap2, A_dL, etc.)
        """
        Rds_on 				=	ModelVars['DCDC_Rail1']['LeftLeg_1']['Transistor']['Rds_on']/ModelVars['DCDC_Rail1']['LeftLeg_1']['nParallel']
        Rds_ons 			=	ModelVars['DCDC_Rail1']['Rectifier_1']['Transistor']['Rds_on']/ModelVars['DCDC_Rail1']['LeftLeg_1']['nParallel']
        N_Tr 				=	ModelVars['DCDC_Rail1']['Trafo']['Np']/ModelVars['DCDC_Rail1']['Trafo']['Ns']
        Lk 					=	ModelVars['DCDC_Rail1']['Trafo']['Lkp'] + ModelVars['DCDC_Rail1']['Trafo']['Lks']*N_Tr**2
        Lf					=	ModelVars['DCDC_Rail1']['Lf']['L']
        DCR 				=	ModelVars['DCDC_Rail1']['Lf']['R']
        d 					=	N_Tr*ModelVars['Common']['Control']['Targets']['Vout']/ModelVars['DCDC_Rail1']['Control']['Inputs']['Vin']
        Tdead 				=	ModelVars['Common']['PWM']['Deadtimes_Rail_1']['S1']
        Fs 					=	ModelVars['Common']['MCU']['f_s']
        Ts 					=	ModelVars['Common']['MCU']['T_s']
        Csnub 				=	ModelVars['DCDC_Rail1']['LeftLeg_1']['Coss']['C']
        Rsnub 				=	ModelVars['DCDC_Rail1']['LeftLeg_1']['Coss']['R']
        Csnubs 				=	ModelVars['DCDC_Rail1']['Rectifier_1']['Coss']['C']
        Rsnubs 				=	ModelVars['DCDC_Rail1']['Rectifier_1']['Coss']['R']

        Rp 					=	2*Rds_on
        Rs 					=	2*Rds_ons
        Rs2 				=	Rs + DCR

        DCDC_Average		=	{
							'Rds_on' 				:	Rds_on 																							,
							'Rds_ons' 				:	Rds_ons																							,
							'R_ss' 					:	0																								,
							'N_Tr' 					:	N_Tr																							,
							'Lk' 					:	max(2e-6,Lk)																					,
							'Lf'					:	Lf																								,
							'DCR' 					:	DCR																								,
							'd' 					:	d																							    ,
							'Tdead' 				:	Tdead 																							,
							'Fs' 					:	Fs 																								,
							'Ts'					:	Ts																								,
                            'Csnub' 				:	Csnub																							,
							'Rsnub' 				:	Rsnub																							,
							'Csnubs'				:	Csnubs																							,
							'Rsnubs'				:	Rsnubs																							,

							'Rp' 					:	Rp 																								,
							'Rs' 					:	Rs 																								,
							'Rs2' 					:	Rs2																								,


							'Ap2' 					:	-(N_Tr/2*2*Rds_ons + 2*Rds_on )/Lk																,
							'A_dL' 					:	Rp																								,
							'B_dL' 					:	Rs2 + Rp/N_Tr**2																				,
							'C_dL' 					:	(Lf + Lk/N_Tr**2)*Lk/N_Tr																		,
							'D_dL' 					:	Lf + Lk/N_Tr**2																					,

							'R_d' 					:	Rs*(0.5 + d/2 - Tdead*Fs) + DCR																	,
							'R_eq' 					:	Rs*(0.5 + d/2 - Tdead*Fs) + DCR																	,

							'Vd'					:	ModelVars['DCDC_Rail1']['Rectifier_1']['BodyDiode']['Vf']
						}

        return DCDC_Average

    def Battery_Rs(self,RsdataPath,Rs_state):
        """Process battery series resistance (Rs) vs SOC/temperature/current.
        
        Organizes data into 3D lookup table indexed by:
        1. Temperature
        2. Current
        3. State of Charge (SOC)
        
        Args:
            RsdataPath: Path to Rs data files
            Rs_state: Battery state identifier
            
        Returns:
            tuple: Three elements:
                - current: Current sweep points
                - cat: MATLAB concatenation command
                - Rs: 3D resistance data [temp][current][SOC]
        """
        Battery                 =   RsdataPath + Rs_state + '_Rs'
        RsData                  =   self.postProcessing.extractArrays(Battery)
        RsData                  =   dp.np.array(RsData)
        RsData_T                =   RsData[1:].T

        current                 =   (dp.np.unique(RsData[0])).tolist()

        temp_length             =   (RsData[0].tolist()).count(RsData[0][0])
        soc_length              =   len(RsData)-1
        curr_length             =   len(current)
        curr_idx                =   dp.np.array(list(range(0,curr_length)))

        LuT_3D                  =   dp.np.empty((temp_length, curr_length, soc_length))
        cat                     =   'cat(3'
        for i in range(temp_length):
            indices             =   i*curr_length+curr_idx
            LuT_3D[:][:][i]     =   (RsData_T[indices,:])
            cat                 =   cat  + ',' + 'LuT_3D' + '(:,:,' + str(i+1) + ')'
        cat                     =   cat  + ')'
        Rs                      =   LuT_3D.tolist()

        return current, cat, Rs

    def Battery_R1(self,R1dataPath,R1_state):
        """Process battery first RC branch resistance (R1) vs SOC/temperature/current.
        
        Organizes data into 3D lookup table similar to Battery_Rs method.
        
        Args:
            R1dataPath: Path to R1 data files
            R1_state: Battery state identifier
            
        Returns:
            tuple: Three elements:
                - current: Current sweep points
                - cat: MATLAB concatenation command
                - R1: 3D resistance data [temp][current][SOC]
        """
        Battery                 =   R1dataPath + R1_state + '_R1'
        R1Data                  =   self.postProcessing.extractArrays(Battery)
        R1Data                  =   dp.np.array(R1Data)
        R1Data_T                =   R1Data[1:].T

        current                 =   (dp.np.unique(R1Data[0])).tolist()

        temp_length             =   (R1Data[0].tolist()).count(R1Data[0][0])
        soc_length              =   len(R1Data)-1
        curr_length             =   len(current)
        curr_idx                =   dp.np.array(list(range(0,curr_length)))

        LuT_3D                  =   dp.np.empty((temp_length, curr_length, soc_length))
        cat                     =   'cat(3'
        for i in range(temp_length):
            indices             =   i*curr_length+curr_idx
            LuT_3D[:][:][i]     =   (R1Data_T[indices,:])
            cat                 =   cat  + ',' + 'LuT_3D' + '(:,:,' + str(i+1) + ')'
        cat                     =   cat  + ')'
        R1                      =   LuT_3D.tolist()

        return current, cat, R1

    def Battery_C1(self,C1dataPath,C1_state):
        """Process battery first RC branch capacitance (C1) vs SOC/temperature/current.
        
        Organizes data into 3D lookup table similar to Battery_Rs method.
        
        Args:
            C1dataPath: Path to C1 data files
            C1_state: Battery state identifier
            
        Returns:
            tuple: Three elements:
                - current: Current sweep points
                - cat: MATLAB concatenation command
                - C1: 3D capacitance data [temp][current][SOC]
        """
        Battery                 =   C1dataPath + C1_state + '_C1'
        C1Data                  =   self.postProcessing.extractArrays(Battery)
        C1Data                  =   dp.np.array(C1Data)
        C1Data_T                =   C1Data[1:].T

        current                 =   (dp.np.unique(C1Data[0])).tolist()

        temp_length             =   (C1Data[0].tolist()).count(C1Data[0][0])
        soc_length              =   len(C1Data)-1
        curr_length             =   len(current)
        curr_idx                =   dp.np.array(list(range(0,curr_length)))

        LuT_3D                  =   dp.np.empty((temp_length, curr_length, soc_length))
        cat                     =   'cat(3'
        for i in range(temp_length):
            indices             =   i*curr_length+curr_idx
            LuT_3D[:][:][i]     =   (C1Data_T[indices,:])
            cat                 =   cat  + ',' + 'LuT_3D' + '(:,:,' + str(i+1) + ')'
        cat                     =   cat  + ')'
        C1                      =   LuT_3D.tolist()

        return current, cat, C1

    def Battery_R2(self,R2dataPath,R2_state):
        """Process battery second RC branch resistance (R2) vs SOC/temperature/current.
        
        Organizes data into 3D lookup table similar to Battery_Rs method.
        
        Args:
            R2dataPath: Path to R2 data files
            R2_state: Battery state identifier
            
        Returns:
            tuple: Three elements:
                - current: Current sweep points
                - cat: MATLAB concatenation command
                - R2: 3D resistance data [temp][current][SOC]
        """
        Battery                 =   R2dataPath + R2_state + '_R2'
        R2Data                  =   self.postProcessing.extractArrays(Battery)
        R2Data                  =   dp.np.array(R2Data)
        R2Data_T                =   R2Data[1:].T

        current                 =   (dp.np.unique(R2Data[0])).tolist()

        temp_length             =   (R2Data[0].tolist()).count(R2Data[0][0])
        soc_length              =   len(R2Data)-1
        curr_length             =   len(current)
        curr_idx                =   dp.np.array(list(range(0,curr_length)))

        LuT_3D                  =   dp.np.empty((temp_length, curr_length, soc_length))
        cat                     =   'cat(3'
        for i in range(temp_length):
            indices             =   i*curr_length+curr_idx
            LuT_3D[:][:][i]     =   (R2Data_T[indices,:])
            cat                 =   cat  + ',' + 'LuT_3D' + '(:,:,' + str(i+1) + ')'
        cat                     =   cat  + ')'
        R2                      =   LuT_3D.tolist()

        return current, cat, R2

    def Battery_C2(self,C2dataPath,C2_state):
        """Process battery second RC branch capacitance (C2) vs SOC/temperature/current.
        
        Organizes data into 3D lookup table similar to Battery_Rs method.
        
        Args:
            C2dataPath: Path to C2 data files
            C2_state: Battery state identifier
            
        Returns:
            tuple: Three elements:
                - current: Current sweep points
                - cat: MATLAB concatenation command
                - C2: 3D capacitance data [temp][current][SOC]
        """
        Battery                 =   C2dataPath + C2_state + '_C2'
        C2Data                  =   self.postProcessing.extractArrays(Battery)
        C2Data                  =   dp.np.array(C2Data)
        C2Data_T                =   C2Data[1:].T

        current                 =   (dp.np.unique(C2Data[0])).tolist()

        temp_length             =   (C2Data[0].tolist()).count(C2Data[0][0])
        soc_length              =   len(C2Data)-1
        curr_length             =   len(current)
        curr_idx                =   dp.np.array(list(range(0,curr_length)))

        LuT_3D                  =   dp.np.empty((temp_length, curr_length, soc_length))
        cat                     =   'cat(3'
        for i in range(temp_length):
            indices             =   i*curr_length+curr_idx
            LuT_3D[:][:][i]     =   (C2Data_T[indices,:])
            cat                 =   cat  + ',' + 'LuT_3D' + '(:,:,' + str(i+1) + ')'
        cat                     =   cat  + ')'
        C2                      =   LuT_3D.tolist()

        return current, cat, C2

    def Battery_OCV(self,BatteryOCVPath,battery_state):
        """Process battery open-circuit voltage (OCV) vs SOC characteristics.
        
        Extracts OCV measurements at:
        1. Multiple SOC points
        2. Multiple temperatures if available
        
        Args:
            BatteryOCVPath: Path to OCV data files
            battery_state: Battery identifier
            
        Returns:
            tuple: Two elements:
                - OCV: OCV values (rows: temperatures, columns: SOC points)
                - OCV_soc: SOC vector
        """
        Battery      =   BatteryOCVPath + battery_state + '_OCV'
        Data         =   self.postProcessing.extractArrays(Battery)
        Data         =   dp.np.array(Data)

        OCV_soc      = dp.np.unique(Data[0]).tolist()
        OCV          =   dp.np.array(Data[1:])
        OCV          =   (OCV.T).tolist()

        return OCV, OCV_soc

    def LuT3D_Generator(self,fileName,Xscale=1,Zscale=1,Zoffset=0):
        """Generate 3D lookup table from data file with scaling options.
        
        Processes generic 3D data with:
        1. X-axis scaling
        2. Z-value scaling
        3. Z-offset adjustment
        
        Creates MATLAB-compatible concatenation command.
        
        Args:
            fileName: Input data file path
            Xscale: X-axis multiplier (default=1)
            Zscale: Z-value multiplier (default=1)
            Zoffset: Z-value offset (default=0)
            
        Returns:
            tuple: Three elements:
                - X_axis: Scaled X-axis values
                - cat: MATLAB concatenation command
                - LuT_3D: Scaled 3D data array
        """
        inputFile   =   fileName
        Data        =   self.postProcessing.extractArrays(inputFile)
        Data        =   dp.np.array(Data)
        Data_T      =   Data[1:].T

        X_axis      =   ((dp.np.unique(Data[0]))*Xscale).tolist()

        Z_length    =   (Data[0].tolist()).count(Data[0][0])
        Y_length    =   len(Data)-1
        X_length    =   len(X_axis)
        X_idx       =   dp.np.array(list(range(0,X_length)))

        LuT_3D      =   dp.np.empty((Z_length,X_length,Y_length))
        cat         =   'cat(3'
        for i in range(Z_length):
            indices             =   i*X_length+X_idx
            LuT_3D[:][:][i]     =   (Data_T[indices,:] - Data[0][0]*Zoffset)*Zscale
            cat                 =   cat  + ',' + 'LuT_3D' + '(:,:,' + str(i+1) + ')'
        cat                     =   cat  + ')'
        LuT_3D                  =   LuT_3D.tolist()

        return X_axis,cat,LuT_3D

    def LuT2D_Generator(self,fileName,Xscale=1,Fscale=1):
        """Generate 2D lookup table from data file with scaling options.
        
        Processes generic 2D data with:
        1. X-axis scaling
        2. Function value scaling
        
        Args:
            fileName: Input data file path
            Xscale: X-axis multiplier (default=1)
            Fscale: Function value multiplier (default=1)
            
        Returns:
            tuple: Two elements:
                - Xvec: Scaled X-axis values
                - Fvec: Scaled function values
        """
        inputFile   =   fileName
        F_X_Vec     =   self.postProcessing.extractArrays(inputFile)

        Xvec        =   (dp.np.array(F_X_Vec[0])*Xscale).tolist()

        Fvec        =   dp.np.array(F_X_Vec[1:])
        Fvec        =   ((dp.np.array(Fvec)*Fscale).T).tolist()

        return Xvec,Fvec

    def LuT1D_Generator(self,fileName,Xscale=1,Fscale=1):
        """Generate 1D lookup table from data file with scaling options.
        
        Processes generic 1D data with:
        1. X-axis scaling
        2. Function value scaling
        
        Args:
            fileName: Input data file path
            Xscale: X-axis multiplier (default=1)
            Fscale: Function value multiplier (default=1)
            
        Returns:
            tuple: Two elements:
                - Xvec: Scaled X-axis values
                - Fvec: Scaled function values
        """
        inputFile   =   fileName
        F_X_Vec     =   self.postProcessing.extractArrays(inputFile)

        Xvec        =   (dp.np.array(F_X_Vec[0])*Xscale).tolist()

        Fvec        =   dp.np.array(F_X_Vec[1])
        Fvec        =   (Fvec*Fscale).tolist()

        return Xvec,Fvec

    def limit_precision(self,nested_dict, precision):
        """Recursively limit numerical precision in nested dictionary.
        
        Processes all numerical values (int, float, numeric strings) to specified
        significant digits while preserving data structure.
        
        Args:
            nested_dict: Input dictionary (may contain nested dicts/lists)
            precision: Number of significant digits to retain
            
        Returns:
            dict: Processed dictionary with limited precision values
        """
        def truncate_value(value):
            if isinstance(value, float):
                return float(f"{value:.{precision}g}")                # Handle floats with the specified precision without losing small values
            elif isinstance(value, (int, complex)):                   # Handle other numeric types
                return value
            elif isinstance(value, str):
                try:
                                                                      # Check if string can be converted to a float
                    float_value = float(value)
                    return f"{float_value:.{precision}g}"
                except ValueError:
                    return value                                      # Return original if not convertible
            return value                                              # Non-numeric values are returned as-is

        def traverse(obj):
            if isinstance(obj, dict):
                return {key: traverse(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [traverse(item) for item in obj]
            elif isinstance(obj, tuple):
                return tuple(traverse(item) for item in obj)
            elif isinstance(obj, set):
                return {traverse(item) for item in obj}
            else:
                return truncate_value(obj)

        return traverse(nested_dict)