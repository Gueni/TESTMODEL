
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

#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
class ParamProcess:
    def __init__(self):
        """Initialize the ParamProcess class with post-processing and simulation utilities."""
        self.postProcessing     =   dp.PP.Processing()
        self.simutil            =   dp.sutl.SimulationUtils()

    def MOSFETcaps(self,path,switch_name,type=""):
        """Extract and process MOSFET capacitance characteristics from simulation data.

        Args:
            path (str): Directory path containing the switch data files.
            switch_name (str): Name identifier for the switch.
            type (str): Suffix specifying the type of capacitance data.

        Returns:
            tuple: Contains five lists:
                - Cmos: Voltage and capacitance pairs
                - Qmos: Calculated charge values
                - Emos: Calculated energy values
                - Cmos_tr: Time-effective capacitance
                - Cmos_er: Energy-effective capacitance
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
        """Extract forward transfer characteristics (Vds vs Ids) for a MOSFET switch.

        Args:
            switchesTransferPath (str): Path to the transfer characteristics data.
            switch_name (str): Name identifier for the switch.

        Returns:
            tuple: Contains two lists:
                - Vdsvec: Drain-source voltage values
                - Idsvec: Corresponding drain-source current values at different gate voltages
        """
        Transfer        =   switchesTransferPath + switch_name +'_Transfer'
        Transfer_vec    =   self.postProcessing.extractArrays(Transfer)

        Vdsvec          =   Transfer_vec[0]

        Idsvec          =   dp.np.array(Transfer_vec[1:])
        Idsvec          =   ((dp.np.array(Idsvec)).T).tolist()

        return Vdsvec,Idsvec

    def MOSFETenergies(self,path,switch_name,type=""):
        """Process MOSFET energy loss data from simulation results.

        Args:
            path (str): Directory path containing the energy data.
            switch_name (str): Name identifier for the switch.
            type (str): Suffix specifying the type of energy data.

        Returns:
            tuple: Contains three elements:
                - current: List of current values
                - cat: MATLAB-style 3D array concatenation command string
                - Emos: 3D list of energy loss data
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

    def MOSFETrdson(self,path,switch_name,type=""):
        """Extract MOSFET on-resistance (Rds_on) characteristics.

        Args:
            path (str): Directory path containing the Rds_on data.
            switch_name (str): Name identifier for the switch.
            type (str): Suffix specifying the type of Rds_on data.

        Returns:
            tuple: Contains two lists:
                - Rvec: On-resistance values
                - Xvec: Corresponding independent variable values (typically voltage or current)
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
        """Extract diode voltage-current characteristics from simulation data.

        Args:
            DiodeVIPath (str): Path to the diode VI characteristics data.
            diode_name (str): Name identifier for the diode.

        Returns:
            tuple: Contains two lists:
                - Vvec: Voltage values across the diode
                - Ivec: Corresponding current values through the diode
        """
        Diode       =   DiodeVIPath + diode_name + '_VI'
        V_I         =   self.postProcessing.extractArrays(Diode)
        Vvec        =   (((dp.np.array(V_I[1:]))).T).tolist()
        Ivec        =   (dp.np.array(V_I[0])).tolist()

        return Vvec,Ivec

    def Mags_CoreLoss_Data(self,TrafoCoreLossesPath,trafo_name):
        """Process transformer core loss data from simulation results.

        Args:
            TrafoCoreLossesPath (str): Path to the core loss data files.
            trafo_name (str): Name identifier for the transformer.

        Returns:
            tuple: Contains three elements:
                - flux: Magnetic flux values in MegaWeber (MWb)
                - cat: MATLAB-style 3D array concatenation command string
                - loss: 3D list of core loss data in Watt/kg
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
        """Process frequency-dependent resistance data for magnetic components.

        Args:
            FreqResistancePath (str): Path to the frequency response data.
            mag_name (list): List of names identifying the magnetic components.

        Returns:
            tuple: Contains two lists:
                - Fvec: Frequency values in kHz
                - Rvec: Corresponding resistance values in mOhm
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
        """Process inductance vs. current characteristics for magnetic components.

        Args:
            InductanceCurrentPath (str): Path to the inductance data.
            mag_name (str): Name identifier for the magnetic component.

        Returns:
            tuple: Contains two lists:
                - Ivec: Current values in Amperes
                - Lvec: Corresponding inductance values in Henries
        """
        Mag         =   InductanceCurrentPath + mag_name
        L_I_Vec     =   self.postProcessing.extractArrays(Mag)

        Ivec        =   L_I_Vec[0]

        Lvec        =   dp.np.array(L_I_Vec[1:])
        Lvec        =   ((dp.np.array(Lvec)*1e-6).T).tolist()

        return Ivec,Lvec

    def linearDerating(self,X1,X2,Y1,Y2,Ymin,Ymax,X):
        """Calculate a linearly interpolated derating factor between two points.

        Args:
            X1 (float): Lower bound of the independent variable range.
            X2 (float): Upper bound of the independent variable range.
            Y1 (float): Derating factor at X1.
            Y2 (float): Derating factor at X2.
            Ymin (float): Minimum allowable derating factor.
            Ymax (float): Maximum allowable derating factor.
            X (float): Current value of independent variable.

        Returns:
            float: Interpolated derating factor, clamped between Ymin and Ymax.

        Raises:
            ValueError: If X1 equals X2, causing division by zero.
        """
        m   =   (Y2 - Y1)/(X2 - X1)
        b   =   Y1 - m*X1

        Y   =   m*X + b

        Y   =   min(Y,Ymax)
        Y   =   max(Y,Ymin)

        return Y

    def scaledList(self,arrayList,scale=1.0):
        """Scale all elements in a list of arrays by a constant factor.

        Args:
            arrayList (list): List of arrays to be scaled.
            scale (float, optional): Scaling factor. Defaults to 1.0.

        Returns:
            list: List of scaled arrays, transposed.

        Note:
            Handles both numpy arrays and regular lists within the input.
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
        """Calculate effective output capacitance (Coss) of a MOSFET.

        Args:
            switch (dict): Dictionary containing MOSFET capacitance characteristics.
            blockingVoltage (float): Voltage at which to evaluate Coss.
            time_energy (bool): Flag to select calculation method:
                - True: Time-effective capacitance (Qoss-based)
                - False: Energy-effective capacitance (Eoss-based)

        Returns:
            float: Effective output capacitance in Farads.
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
        """Calculate precharge current reference values for snubber circuit design.

        Args:
            V_snub (float): Snubber circuit voltage.
            V_LV_OP (float): Low-voltage operational voltage.
            Np (int): Primary winding turns.
            Ns (int): Secondary winding turns.
            fs (float): Switching frequency.
            Lfilter (float): Filter inductance.
            Lks (float): Secondary leakage inductance.
            Lkp (float): Primary leakage inductance.
            I_C_max (float): Maximum capacitor current.
            ILVmax (int): Maximum low-voltage current index.
            tonsnubmin (float): Minimum snubber turn-on time.
            Points (int): Number of calculation points.

        Returns:
            tuple: Contains three elements:
                - Vvec: Voltage vector
                - Ivec: Current reference vector
                - ton_snub_final: Final snubber turn-on time
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
        """Calculate parameters for DC-DC converter average model.

        Args:
            ModelVars (dict): Dictionary containing all model parameters.

        Returns:
            dict: Dictionary containing calculated average model parameters.
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

    def batteryParams(self,Path,Type):
        """_summary_

        Args:
            Path (_type_): _description_
            Type (_type_): _description_

        Returns:
            _type_: _description_
        """
        Battery                 =   Path + Type
        Data                    =   self.postProcessing.extractArrays(Battery)
        Data                    =   dp.np.array(Data)
        Data_T                  =   Data[1:].T

        current                 =   (dp.np.unique(Data[0])).tolist()

        temp_length             =   (Data[0].tolist()).count(Data[0][0])
        soc_length              =   len(Data)-1
        curr_length             =   len(current)
        curr_idx                =   dp.np.array(list(range(0,curr_length)))

        LuT_3D                  =   dp.np.empty((temp_length, curr_length, soc_length))
        cat                     =   'cat(3'
        for i in range(temp_length):
            indices             =   i*curr_length+curr_idx
            LuT_3D[:][:][i]     =   (Data_T[indices,:])
            cat                 =   cat  + ',' + 'LuT_3D' + '(:,:,' + str(i+1) + ')'
        cat                     =   cat  + ')'
        Param                   =   LuT_3D.tolist()

        return current,cat,Param

    def Battery_OCV(self,BatteryOCVPath,battery_state):
        """Extract battery open-circuit voltage (OCV) characteristics.

        Args:
            BatteryOCVPath (str): Path to the OCV data files.
            battery_state (str): Name identifier for the OCV data.

        Returns:
            tuple: Contains two elements:
                - OCV: Open-circuit voltage values
                - OCV_soc: Corresponding state-of-charge values
        """
        Battery      =   BatteryOCVPath + battery_state + '_OCV'
        Data         =   self.postProcessing.extractArrays(Battery)
        Data         =   dp.np.array(Data)

        OCV_soc      = dp.np.unique(Data[0]).tolist()
        OCV          =   dp.np.array(Data[1:])
        OCV          =   (OCV.T).tolist()

        return OCV, OCV_soc

    def LuT3D_Generator(self,fileName,Xscale=1,Zscale=1,Zoffset=0):
        """Generate a 3D lookup table from simulation data with scaling options.

        Args:
            fileName (str): Path to the input data file.
            Xscale (float, optional): Scaling factor for X-axis. Defaults to 1.
            Zscale (float, optional): Scaling factor for Z-values. Defaults to 1.
            Zoffset (float, optional): Offset for Z-values. Defaults to 0.

        Returns:
            tuple: Contains three elements:
                - X_axis: X-axis values
                - cat: MATLAB-style 3D array concatenation command string
                - LuT_3D: 3D list of scaled data
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
        """Generate a 2D lookup table from simulation data with scaling options.

        Args:
            fileName (str): Path to the input data file.
            Xscale (float, optional): Scaling factor for X-axis. Defaults to 1.
            Fscale (float, optional): Scaling factor for function values. Defaults to 1.

        Returns:
            tuple: Contains two lists:
                - Xvec: X-axis values
                - Fvec: Corresponding function values
        """
        inputFile   =   fileName
        F_X_Vec     =   self.postProcessing.extractArrays(inputFile)

        Xvec        =   (dp.np.array(F_X_Vec[0])*Xscale).tolist()

        Fvec        =   dp.np.array(F_X_Vec[1:])
        Fvec        =   ((dp.np.array(Fvec)*Fscale).T).tolist()

        return Xvec,Fvec

    def LuT1D_Generator(self,fileName,Xscale=1,Fscale=1):
        """Generate a 1D lookup table from simulation data with scaling options.

        Args:
            fileName (str): Path to the input data file.
            Xscale (float, optional): Scaling factor for X-axis. Defaults to 1.
            Fscale (float, optional): Scaling factor for function values. Defaults to 1.

        Returns:
            tuple: Contains two lists:
                - Xvec: X-axis values
                - Fvec: Corresponding function values
        """
        inputFile   =   fileName
        F_X_Vec     =   self.postProcessing.extractArrays(inputFile)

        Xvec        =   (dp.np.array(F_X_Vec[0])*Xscale).tolist()

        Fvec        =   dp.np.array(F_X_Vec[1])
        Fvec        =   (Fvec*Fscale).tolist()

        return Xvec,Fvec

    def limit_precision(self,nested_dict, precision):
        """Recursively limit the precision of numeric values in a nested dictionary.

        Args:
            nested_dict (dict): Dictionary to process (can be nested).
            precision (int): Number of significant digits to keep.

        Returns:
            dict: Dictionary with numeric values truncated to specified precision.

        Note:
            - Handles floats, integers, and numeric strings.
            - Preserves non-numeric values unchanged.
            - Maintains all dictionary structure and nesting.
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