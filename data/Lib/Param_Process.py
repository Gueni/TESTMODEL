
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

        """
        Initialize the ParamProcess class with post-processing and simulation utilities.
        
        """

        self.postProcessing     =   dp.PP.Processing()
        self.simutil            =   dp.sutl.SimulationUtils()

    def MOSFETcaps(self, path, switch_name, type=""):
        """
        Calculate MOSFET capacitance, charge, and energy from CSV  files.

        This function reads capacitance data (C-V curves) from CSV files provided by
        datasheets or suppliers and computes:
            - Capacitance (Cmos)
            - Integrated charge (Qmos)
            - Stored energy (Emos)
            - Differential capacitances derived from charge (Cmos_tr)
            - Differential capacitances derived from energy (Cmos_er)

        Formulas used:
            - Charge from capacitance: 
                Q(V) = ∫ C(V) dV    (trapezoidal integration using numpy.trapz)
            - Energy from capacitance:
                E(V) = ∫ C(V) * V dV ≈ ∫ Q(V) dV
            - Differential capacitance from charge:
                C_tr = ΔQ / ΔV
            - Differential capacitance from energy:
                C_er = 2 * ΔE / Δ(V^2)

        Args:
            path (str)        : Folder path to CSV datasheet
            switch_name (str) : MOSFET switch file name
            type (str, optional): Optional suffix for file type. Default is empty.

        Returns:
            tuple: (Cmos, Qmos, Emos, Cmos_tr, Cmos_er)
                - Cmos      : Capacitance array [V, C] in Farads
                - Qmos      : Integrated charge array in Coulombs
                - Emos      : Integrated energy array in Joules
                - Cmos_tr   : Differential capacitance derived from charge
                - Cmos_er   : Differential capacitance derived from energy

        Libraries used:
            - numpy.trapz() for numerical integration, which approximates the area under the curve using the trapezoidal rule.  
              [numpy.trapz() docs]: https://numpy.org/doc/1.25/reference/generated/numpy.trapz.html  
        """

        # Construct full path to CSV
        switch      = path + switch_name + type
        
        # Extract capacitance arrays [V, C] from CSV
        Cmos        = self.postProcessing.extractArrays(switch)

        # Calculate C*V product for energy integration
        Vds_Cmos    = [Cmos[0], (dp.np.multiply(dp.np.array(Cmos[0]), dp.np.array(Cmos[1]))).tolist()]

        # Initialize lists for charge and energy
        Qmos        = []
        Emos        = []

        # Integrate capacitance and energy using trapezoidal rule
        for i in range(len(Cmos[0])):

            # Charge calculation Q = ∫ C(V) dV
            idx             = self.postProcessing.get_index(Cmos, Cmos[0][i], 0)
            capacity        = (dp.np.array(Cmos)[:, 0:idx+1]).tolist()
            charge          = float(dp.np.trapz(capacity[1], x=capacity[0]))
            Qmos.append(dp.np.around(charge, 3))

            # Energy calculation E = ∫ V * C(V) dV ≈ ∫ Q(V) dV
            idx             = self.postProcessing.get_index(Vds_Cmos, Vds_Cmos[0][i], 0)
            capacityVoltage = (dp.np.array(Vds_Cmos)[:, 0:idx+1]).tolist()
            energy          = float(dp.np.trapz(capacityVoltage[1], x=capacityVoltage[0]))
            Emos.append(dp.np.around(energy, 3))

        # Convert to SI units (Farads, Coulombs, Joules)
        Cmos[1]             = dp.np.array(Cmos[1]) * 1e-12
        Cmos                = dp.np.array(Cmos)
        Qmos                = dp.np.array(Qmos) * 1e-12
        Emos                = dp.np.array(Emos) * 1e-12
        
        # Compute differential capacitances
        # Cmos_tr from charge: C = ΔQ / ΔV
        # Cmos_er from energy: C = 2 * ΔE / Δ(V^2)
        Cmos_tr             = (Qmos[1:] / (Cmos[0][1:] - Cmos[0][0])).tolist()
        Cmos_er             = (2 * Emos[1:] / (Cmos[0][1:]**2 - Cmos[0][0]**2)).tolist()

        # Insert zero for first point to match array length
        Cmos_tr.insert(0, 0)
        Cmos_er.insert(0, 0)

        # Convert arrays to lists for output
        Cmos                = Cmos.tolist()
        Qmos                = Qmos.tolist()
        Emos                = Emos.tolist()
        
        return Cmos, Qmos, Emos, Cmos_tr, Cmos_er

    def Forward_Transfer_data(self, switchesTransferPath, switch_name):
        """
        Extract forward transfer characteristics (Vds vs Ids) for a MOSFET switch.

        This function reads the MOSFET transfer characteristics from a CSV file
        (Vds vs Ids at different gate voltages), converts the extracted data
        into NumPy arrays for processing, and returns it as lists.

        Args:
            switchesTransferPath (str): Path to the folder containing transfer characteristics data.
            switch_name (str): Name identifier for the MOSFET switch.

        Returns:
            tuple: Two lists:
                - Vdsvec: Drain-source voltage values (V)
                - Idsvec: Corresponding drain-source current values (A) 
                        at different gate voltages; each row corresponds to a Vds point.

        Notes:
            - CSV files are expected to be structured with the first column as Vds and
            subsequent columns as Ids for different gate voltages.
            - Uses NumPy for array manipulation: https://numpy.org/doc/stable/
        """

        # Construct full file path
        Transfer        = switchesTransferPath + switch_name + '_Transfer'

        # Extract CSV data as arrays
        Transfer_vec    = self.postProcessing.extractArrays(Transfer)
        
        # Extract Vds vector (first row)
        Vdsvec          = Transfer_vec[0]
        
        # Extract Ids matrix and transpose so each row corresponds to Vds
        Idsvec          = dp.np.array(Transfer_vec[1:])
        Idsvec          = (dp.np.array(Idsvec)).T.tolist()

        return Vdsvec, Idsvec

    def MOSFETenergies(self, path, switch_name, type=""):
        """
        This function reads MOSFET energy loss data from CSV ,
        reshapes it into a 3D array corresponding to voltage, current, and gate voltage,
        and applies unit conversion to Joules. It also generates a MATLAB-style
        3D array concatenation command string for visualization or further processing.

        Args:
            path (str): Directory path containing the energy data file.
            switch_name (str): Name identifier for the MOSFET switch.
            type (str, optional): Suffix specifying the type of energy data. Default is "".

        Returns:
            tuple: Contains three elements:
                - current (list): Unique current values (A) present in the dataset.
                - cat (str): MATLAB-style 3D concatenation string representing LuT_3D.
                - Emos (list): 3D list of energy loss data (Joules), shaped as 
                            [voltage, current, gate voltage].

        Notes:
            - EmosData[0] corresponds to voltage values, EmosData[1:] to energy losses.
            - Data reshaped into 3D using NumPy for efficient slicing.
            - Energy values are converted from µJ to Joules using 1e-6 factor.
            - NumPy library is used for array manipulation: https://numpy.org/doc/stable/

        Math:
            Energy conversion: E [J] = (EmosData_T - EmosData_T[0,0]) * 1e-6
            3D reshaping: LuT_3D[i,j,k] corresponds to:
                i = voltage index
                j = current index
                k = gate voltage index
        """

        # Construct full file path
        switch      = path + switch_name + type
        
        # Extract energy data arrays
        EmosData    = self.postProcessing.extractArrays(switch)
        EmosData    = dp.np.array(EmosData)

        # Transpose to prepare for slicing
        EmosData_T  = EmosData[1:].T

        # Identify unique currents and dimensions
        current     = dp.np.unique(EmosData[0]).tolist()
        volt_length = (EmosData[0].tolist()).count(EmosData[0][0])
        gate_length = len(EmosData) - 1
        curr_length = len(current)
        curr_idx    = dp.np.array(list(range(0, curr_length)))

        # Initialize 3D energy array and MATLAB-style concatenation string
        LuT_3D      = dp.np.empty((volt_length, curr_length, gate_length))
        cat         = 'cat(3'

        # Populate 3D array and build concatenation string
        for i in range(volt_length):
            indices         = i * curr_length + curr_idx
            LuT_3D[:, :, i] = (EmosData_T[indices, :] - EmosData_T[0][0]) * 1e-6  # Convert µJ -> J
            cat             = cat + ',' + 'LuT_3D' + '(:,:,' + str(i + 1) + ')'

        cat         = cat + ')'

        # Convert 3D array to list for output
        Emos        = LuT_3D.tolist()

        return current, cat, Emos

    def MOSFETrdson(self, path, switch_name, type=""):
        """

        This function reads Rds_on data from datasheets or supplier files,
        separates the independent variable (voltage or current) and
        the corresponding on-resistance values, and returns them as lists.

        Args:
            path (str): Directory path containing the Rds_on data file.
            switch_name (str): Name identifier for the MOSFET switch.
            type (str, optional): Suffix specifying the type of Rds_on data. Default is "".

        Returns:
            tuple: Two lists:
                - Rvec: On-resistance values (Ohms)
                - Xvec: Corresponding independent variable values 
                        (typically voltage or current).

        Notes:
            - CSV files are expected to have alternating columns of independent variables and Rds_on values.
            - Uses NumPy for array manipulation: https://numpy.org/doc/stable/

        Example:
            Xvec[i] corresponds to the independent variable (V or I) for the i-th dataset,
            Rvec[i] contains the corresponding Rds_on values.
        """
        
        # Construct full file path
        Switch      = path + switch_name + type
        
        # Extract Rds_on and independent variable arrays
        R_X_Vec     = self.postProcessing.extractArrays(Switch)
        R_X_Types   = len(R_X_Vec)
        
        # Separate independent variable (X) and resistance (R) vectors
        Rvec        = []
        Xvec        = []
        for i in range(R_X_Types // 2):
            Xvec.append(R_X_Vec[i * 2])
            Rvec.append(R_X_Vec[i * 2 + 1])

        # Transpose arrays so each row corresponds to a dataset
        Rvec        = (dp.np.array(Rvec)).T.tolist()
        Xvec        = (dp.np.array(Xvec)).T.tolist()

        return Rvec, Xvec

    def DiodeVI_data(self, DiodeVIPath, diode_name):
        """

        This function reads diode V-I data from a CSV file ,
        separates voltage and current values, and returns them as lists suitable for plotting
        or further analysis.

        Args:
            DiodeVIPath (str): Path to the folder containing diode VI characteristics data.
            diode_name (str): Name identifier for the diode.

        Returns:
            tuple: Two lists:
                - Vvec: Voltage values across the diode (V)
                - Ivec: Corresponding current values through the diode (A)

        Notes:
            - CSV files are expected to have the first row/column as current and subsequent rows/columns as voltage points.
            - Uses NumPy for array manipulation: https://numpy.org/doc/stable/

        Example:
            Vvec[i] corresponds to the voltage across the diode at the i-th data point,
            Ivec[i] is the corresponding current through the diode.
        """
        
        # Construct full file path
        Diode   = DiodeVIPath + diode_name + '_VI'

        # Extract V-I data arrays
        V_I     = self.postProcessing.extractArrays(Diode)

        # Separate voltage and current vectors
        Vvec    = (dp.np.array(V_I[1:])).T.tolist()  # Voltage array, transposed
        Ivec    = dp.np.array(V_I[0]).tolist()       # Current array

        return Vvec, Ivec

    def Mags_CoreLoss_Data(self, TrafoCoreLossesPath, trafo_name):
        """

        This function reads core loss data for a transformer, reshapes it into a
        3D array representing temperature, flux, and voltage, and generates a
        MATLAB-style concatenation string for visualization or further processing.

        Args:
            TrafoCoreLossesPath (str): Path to the folder containing core loss data files.
            trafo_name (str): Name identifier for the transformer.

        Returns:
            tuple: Contains three elements:
                - flux (list): Magnetic flux values in MegaWeber (MWb)
                - cat (str): MATLAB-style 3D concatenation string representing LuT_3D
                - loss (list): 3D list of core loss data (W/kg), shaped as 
                            [temperature, flux, voltage]

        Notes:
            - CSV files are expected to have the first column as flux data and
            subsequent columns as core loss values at different voltages/temperatures.
            - Flux values are converted from Weber to MegaWeber using 1e-6 factor.
            - Uses NumPy for array manipulation: https://numpy.org/doc/stable/

        Math:
            3D reshaping: LuT_3D[i,j,k] corresponds to:
                i = temperature index
                j = flux index
                k = voltage index
        """

        # Construct full file path
        Trafo           = TrafoCoreLossesPath + trafo_name

        # Extract core loss data
        coreData        = self.postProcessing.extractArrays(Trafo)
        coreData        = dp.np.array(coreData)

        # Transpose to prepare for slicing
        coreData_T      = coreData[1:].T

        # Extract unique flux values and convert to MWb
        flux            = (dp.np.unique(coreData[0]) * 1.0e-6 / 2.0).tolist()

        # Determine dimensions for 3D array
        temp_length     = (coreData[0].tolist()).count(coreData[0][0])
        voltage_length  = len(coreData) - 1
        flux_length     = len(flux)
        flux_idx        = dp.np.array(list(range(0, flux_length)))
        
        # Initialize 3D array and MATLAB-style concatenation string
        LuT_3D          = dp.np.empty((temp_length, flux_length, voltage_length))
        cat             = 'cat(3)'

        # Populate 3D array and build concatenation string
        cat = 'cat(3'

        for i in range(temp_length):

            indices         = i * flux_length + flux_idx
            LuT_3D[:, :, i] = coreData_T[indices, :]
            cat             = cat + ',' + 'LuT_3D' + '(:,:,' + str(i + 1) + ')'

        cat             = cat + ')'

        # Convert 3D array to list for output
        loss            = LuT_3D.tolist()

        return flux, cat, loss

    def Mags_FreqRes_Data(self, FreqResistancePath, mag_name):
        """

        This function reads resistance vs frequency data for one or more magnetic components
        (e.g., inductors, transformers) from CSV files, converts units to mOhm and kHz, 
        and returns them as lists suitable for plotting or further analysis.

        Args:
            FreqResistancePath (str): Path to the folder containing frequency response data files.
            mag_name (list): List of names identifying the magnetic components.

        Returns:
            tuple: Two lists:
                - Fvec: Frequency values in kHz for each component
                - Rvec: Corresponding resistance values in mOhm for each component

        Notes:
            - CSV files are expected to have the first column as frequency and subsequent columns as resistance values.
            - Uses NumPy for array manipulation: https://numpy.org/doc/stable/
            - Unit conversions:
                - Resistance: Ohms -> mOhm (*1e3)
                - Frequency: Hz -> kHz (*1e-3)

        Example:
            Fvec[i] and Rvec[i] contain the frequency and resistance arrays for the i-th magnetic component.
        """

        # Initialize lists for resistance and frequency vectors
        Rvec            = []
        Fvec            = []
        
        # Loop through each magnetic component
        for i in range(len(mag_name)):
            # Construct full file path for the component
            Winding     = FreqResistancePath + mag_name[i]
            
            # Extract frequency-resistance data arrays
            R_F         = self.postProcessing.extractArrays(Winding)

            # Convert units
            R           = (dp.np.array(R_F[1:]) * 1e-3).tolist()  # Ohms -> mOhm
            F           = (dp.np.array(R_F[0]) * 1e3).tolist()    # Hz -> kHz

            # Append to the output lists
            Rvec.append(R)
            Fvec.append(F)

        return Fvec, Rvec

    def Mags_LI_Data(self, InductanceCurrentPath, mag_name):
        """
        This function reads L-I data from CSV or simulation results for a given magnetic
        component (e.g., inductor or transformer winding), converts the units to Henries,
        and returns current and inductance values as lists suitable for plotting or analysis.

        Args:
            InductanceCurrentPath (str): Path to the folder containing inductance data files.
            mag_name (str): Name identifier for the magnetic component.

        Returns:
            tuple: Two lists:
                - Ivec: Current values (A)
                - Lvec: Corresponding inductance values (H)

        Notes:
            - CSV files are expected to have the first column as current and subsequent columns as inductance values.
            - Unit conversion: µH -> H (*1e-6)
            - Uses NumPy for array manipulation: https://numpy.org/doc/stable/

        Example:
            Ivec[i] corresponds to the current for the i-th data point,
            Lvec[i] is the corresponding inductance.
        """

        # Construct full file path
        Mag     = InductanceCurrentPath + mag_name

        # Extract L-I data arrays
        L_I_Vec = self.postProcessing.extractArrays(Mag)

        # Separate current and inductance vectors
        Ivec    = L_I_Vec[0]

        # Convert inductance to Henries and transpose
        Lvec    = dp.np.array(L_I_Vec[1:])
        Lvec    = (dp.np.array(Lvec) * 1e-6).T.tolist()

        return Ivec, Lvec

    def scaledList(self, arrayList, scale=1.0):
        """

        This function takes a list of arrays (or lists), multiplies each element
        by a given scaling factor, and returns the scaled list transposed.
        Useful for normalizing or converting units of multiple datasets at once.

        Args:
            arrayList (list): List of arrays or lists to be scaled.
            scale (float, optional): Scaling factor to apply. Defaults to 1.0.

        Returns:
            list: List of scaled arrays, transposed.

        Notes:
            - Handles both NumPy arrays and standard Python lists.
            - Uses NumPy for efficient array operations: https://numpy.org/doc/stable/

        Example:
            scaled = scaledList([[1,2,3],[4,5,6]], scale=2)
            # Returns [[2,8],[4,10],[6,12]]
        """
        
        # Convert all elements to lists for uniformity
        arrayList   = (dp.np.array(arrayList)).tolist()
        
        # Scale each array or list
        for i in range(len(arrayList)):

            if isinstance(arrayList[i], dp.np.ndarray):

                # If already a NumPy array, multiply directly and convert to list
                tempList        = (arrayList[i] * scale).tolist()
                arrayList[i]    = tempList

            else:

                # Convert list to NumPy array, scale, and convert back to list
                arrayList[i]    = (dp.np.array(arrayList[i]) * scale).tolist()

        # Transpose the scaled list and return
        arrayList   = (dp.np.array(arrayList)).T.tolist()

        return arrayList

    def getCoss(self, switch, blockingVoltage, time_energy):
        """
        Calculate the effective output capacitance (Coss) of a MOSFET.

        This function computes Coss at a given blocking voltage using either
        time-effective (Qoss-based) or energy-effective (Eoss-based) methods
        commonly used in power electronics.

        Args:
            switch (dict): Dictionary containing MOSFET capacitance characteristics with keys:
                - 'Vvec': List of voltages (V)
                - 'Cvec': List of measured capacitances (F)
                - 'Qoss': List of stored charge values (Coulombs)
                - 'Eoss': List of energy values (Joules)
            blockingVoltage (float): Voltage (V) at which to evaluate Coss.
            time_energy (bool): Select calculation method:
                - True: Time-effective capacitance (Coss = Qoss / ΔV)
                - False: Energy-effective capacitance (Coss = 2*Eoss / ΔV²)

        Returns:
            float: Effective output capacitance (Coss) in Farads.

        Notes:
            - ΔV = V_blocking - V_min
            - Time-effective formula: Coss_eff = Qoss / (V_blocking - V_min)
            - Energy-effective formula: Coss_eff = 2 * Eoss / (V_blocking² - V_min²)
            - Result is rounded to 2 decimal places in pF and converted back to F.
            - Uses NumPy for array operations: https://numpy.org/doc/stable/

        Example:
            Coss = getCoss(mosfet_data, 600, True)
        """

        # Extract voltage and capacitance arrays from dictionary
        voltageVector   = switch['Coss']['Vvec']
        CossVector      = switch['Coss']['Cvec']
        QossVector      = switch['Coss']['Qoss']
        EossVector      = switch['Coss']['Eoss']
        
        # Prepare voltage-capacitance pair for indexing
        Coss            = [voltageVector, CossVector]

        # Get the index of the closest voltage to the blockingVoltage
        Coss_idx        = self.simutil.postProcessing.get_index(Coss, blockingVoltage, 0)

        # Compute effective Coss based on selected method
        if time_energy:
            Qoss        = QossVector[Coss_idx]
            Coss_eff    = Qoss / (Coss[0][Coss_idx] - Coss[0][0])  # Time-effective
        else:
            Eoss        = EossVector[Coss_idx]
            Coss_eff    = 2 * Eoss / (Coss[0][Coss_idx]**2 - Coss[0][0]**2)  # Energy-effective
        
        # Round result to 2 decimal pF and convert back to Farads
        Coss_eff        = round(Coss_eff * 1e12, 2) * 1e-12

        return Coss_eff

    def PrechargeILVref(self, V_snub, V_LV_OP, Np, Ns, fs, Lfilter, Lks, Lkp, I_C_max, ILVmax, tonsnubmin, Points):
        """

        This function computes a voltage vector, corresponding precharge current references,
        and the final snubber turn-on time based on transformer parameters, leakage
        inductances, and snubber constraints.

        Args:
            V_snub (float): Snubber circuit voltage (V)
            V_LV_OP (float): Low-voltage operational voltage (V)
            Np (int): Primary winding turns
            Ns (int): Secondary winding turns
            fs (float): Switching frequency (Hz)
            Lfilter (float): Filter inductance (H)
            Lks (float): Secondary leakage inductance (H)
            Lkp (float): Primary leakage inductance (H)
            I_C_max (float): Maximum allowable snubber capacitor current (A)
            ILVmax (int): Maximum low-voltage current index
            tonsnubmin (float): Minimum allowable snubber turn-on time (s)
            Points (int): Number of points for voltage/current vector calculation

        Returns:
            tuple: Contains three elements:
                - Vvec (list): Voltage vector (V)
                - Ivec (list): Precharge current reference vector (A)
                - ton_snub_final (float): Final snubber turn-on time (s)

        Notes:
            - ntr = Np/Ns is the turns ratio
            - L_leak_lv = (Lks + Lkp) / ntr^2 is the low-voltage referred leakage inductance
            - Duty cycle: Duty = (V_snub - V_LV_OP) / (V_snub - V_HV / ntr)
            - Snubber on-time: ton_snub = sqrt(2 * L_leak_lv * ILV * toff / (V_snub - V_HV/ntr))
            - Low-voltage ripple: dI_LV = (V_snub - V_LV_OP) * toff / Lfilter
            - Snubber peak current: Ipeak_snub = (V_snub - V_HV/ntr) * ton_snub / L_leak_lv
            - RMS snubber capacitor current: IC_snub_RMS = sqrt(IC_snub_P^2 + IC_snub_N^2)
            - Uses NumPy for array and linspace operations: https://numpy.org/doc/stable/

        References:
            - Standard snubber design for leakage inductance energy dissipation
            - Equations based on power electronics transformer precharge design
        """
        
        # Compute turns ratio and low-voltage referred leakage inductance
        ntr             = Np / Ns
        L_leak_lv       = (Lks + Lkp) / (ntr ** 2)

        # Generate voltage vector
        Vvec            = list(dp.np.linspace(0, V_LV_OP * ntr, Points))
        Ivec            = dp.copy.deepcopy(Vvec)
        
        # Loop over each voltage and low-voltage current
        for V_HV in Vvec:
            for ILV in range(ILVmax + 1):

                Duty        = (V_snub - V_LV_OP) / (V_snub - V_HV / ntr)
                toff        = (1 - Duty) / (2 * fs)
                ton_snub    = pow(2 * L_leak_lv * ILV * toff / (V_snub - V_HV / ntr), 0.5)
                dI_LV       = (V_snub - V_LV_OP) * toff / Lfilter
                ILV_peak    = ILV + dI_LV / 2
                Ipeak_snub  = (V_snub - V_HV / ntr) * ton_snub / L_leak_lv
                IC_snub_P   = pow(2 * fs * ((ILV_peak**2 * toff) + ((V_snub - V_LV_OP)**2 * toff**3) / (3 * Lfilter**2)) -(ILV_peak * (V_snub - V_LV_OP) * toff**2 / Lfilter), 0.5)
                IC_snub_N   = Ipeak_snub * pow((2 * fs * ton_snub / 3), 0.5)
                IC_snub_RMS = pow(IC_snub_P**2 + IC_snub_N**2, 0.5)

                # Select precharge current if RMS current is below max
                if IC_snub_RMS < I_C_max:   Iref1 = ILV

            # Determine final snubber turn-on time
            if V_HV == 0:   ton_snub_final = tonsnubmin if ton_snub < tonsnubmin else ton_snub

            Ivec[Vvec.index(V_HV)] = Iref1

        # Convert voltage vector to integer
        Vvec    = (dp.np.array(Vvec).astype(int)).tolist()

        return Vvec, Ivec, ton_snub_final

    def dcdcAverageModelCalculate(self, ModelVars):
        """
        Calculate parameters for the average model of a DC-DC converter.

        This function extracts relevant parameters from the ModelVars dictionary
        and computes equivalent resistances, inductances, duty cycles, snubber
        components, and other derived quantities for the DC-DC converter average
        model, suitable for small-signal or simplified simulations.

        Args:
            ModelVars (dict): Dictionary containing all model parameters with keys for:
                - DCDC_Rail1: Information about the first DC-DC rail (MOSFETs, rectifiers, transformer, filter)
                - Common: Common parameters like PWM, control targets, and MCU settings

        Returns:
            dict: Dictionary containing calculated average model parameters, including:
                - Resistances: Rds_on, Rds_ons, Rp, Rs, Rs2
                - Inductances: Lk (leakage), Lf (filter)
                - Duty cycle and timing: d, Tdead, Fs, Ts
                - Snubber components: Csnub, Rsnub, Csnubs, Rsnubs
                - Equivalent model coefficients: Ap2, A_dL, B_dL, C_dL, D_dL
                - Equivalent resistances for converter model: R_d, R_eq
                - Forward voltage of rectifier diode: Vd

        Notes:
            - N_Tr = Turns ratio of transformer: Np / Ns
            - Lk = Lkp + Lks * N_Tr^2: total referred leakage inductance
            - Duty cycle: d = N_Tr * Vout_target / Vin_input
            - Ap2, A_dL, B_dL, C_dL, D_dL are derived from small-signal modeling equations
            - Rp, Rs, Rs2 are equivalent series resistances used in average model
            - Uses NumPy implicitly via dp.np if needed for array operations: https://numpy.org/doc/stable/

        Example:
            avg_params = dcdcAverageModelCalculate(ModelVars)
        """

        # Extract MOSFET and rectifier resistances (divide by parallel count)
        Rds_on      = ModelVars['DCDC_Rail1']['LeftLeg_1']['Transistor']['Rds_on'] / ModelVars['DCDC_Rail1']['LeftLeg_1']['nParallel']
        Rds_ons     = ModelVars['DCDC_Rail1']['Rectifier_1']['Transistor']['Rds_on'] / ModelVars['DCDC_Rail1']['LeftLeg_1']['nParallel']

        # Transformer turns ratio and leakage inductance
        N_Tr        = ModelVars['DCDC_Rail1']['Trafo']['Np'] / ModelVars['DCDC_Rail1']['Trafo']['Ns']
        Lk          = ModelVars['DCDC_Rail1']['Trafo']['Lkp'] + ModelVars['DCDC_Rail1']['Trafo']['Lks'] * N_Tr**2

        # Filter inductance and resistance
        Lf          = ModelVars['DCDC_Rail1']['Lf']['L']
        DCR         = ModelVars['DCDC_Rail1']['Lf']['R']
        
        # Duty cycle, PWM deadtime, switching frequency/period
        d           = N_Tr * ModelVars['Common']['Control']['Targets']['Vout'] / ModelVars['DCDC_Rail1']['Control']['Inputs']['Vin']
        Tdead       = ModelVars['Common']['PWM']['Deadtimes_Rail_1']['S1']
        Fs          = ModelVars['Common']['MCU']['f_s']
        Ts          = ModelVars['Common']['MCU']['T_s']

        # Snubber capacitances and resistances
        Csnub       = ModelVars['DCDC_Rail1']['LeftLeg_1']['Coss']['C']
        Rsnub       = ModelVars['DCDC_Rail1']['LeftLeg_1']['Coss']['R']
        Csnubs      = ModelVars['DCDC_Rail1']['Rectifier_1']['Coss']['C']
        Rsnubs      = ModelVars['DCDC_Rail1']['Rectifier_1']['Coss']['R']
        
        # Equivalent series resistances
        Rp          = 2 * Rds_on
        Rs          = 2 * Rds_ons
        Rs2         = Rs + DCR

        # Assemble average model dictionary
        DCDC_Average = {
                            'Rds_on'  : Rds_on                                                       ,
                            'Rds_ons' : Rds_ons                                                      ,
                            'R_ss'    : 0                                                            ,
                            'N_Tr'    : N_Tr                                                         ,
                            'Lk'      : max(2e-6, Lk)                                                ,
                            'Lf'      : Lf                                                           ,
                            'DCR'     : DCR                                                          ,
                            'd'       : d                                                            ,
                            'Tdead'   : Tdead                                                        ,
                            'Fs'      : Fs                                                           ,
                            'Ts'      : Ts                                                           ,
                            'Csnub'   : Csnub                                                        ,
                            'Rsnub'   : Rsnub                                                        ,
                            'Csnubs'  : Csnubs                                                       ,
                            'Rsnubs'  : Rsnubs                                                       ,
                            'Rp'      : Rp                                                           ,
                            'Rs'      : Rs                                                           ,
                            'Rs2'     : Rs2                                                          ,
                            'Ap2'     : -(N_Tr/2*2*Rds_ons + 2*Rds_on) / Lk                          ,
                            'A_dL'    : Rp                                                           ,
                            'B_dL'    : Rs2 + Rp / N_Tr**2                                           ,
                            'C_dL'    : (Lf + Lk / N_Tr**2) * Lk / N_Tr                              ,
                            'D_dL'    : Lf + Lk / N_Tr**2                                            ,
                            'R_d'     : Rs * (0.5 + d/2 - Tdead * Fs) + DCR                          ,
                            'R_eq'    : Rs * (0.5 + d/2 - Tdead * Fs) + DCR                          ,
                            'Vd'      : ModelVars['DCDC_Rail1']['Rectifier_1']['BodyDiode']['Vf']    
                        }


        return DCDC_Average

    def batteryParams(self, Path, Type):
        """

        This function processes battery data (e.g., voltage, SOC, current) provided as
        a table from a CSV. The data is reshaped into a MATLAB-style
        3D array to represent parameters as a function of current, state-of-charge (SOC),
        and temperature/time steps.

        Args:
            Path (str): Directory path containing the battery data file.
            Type (str): Filename or type identifier of the battery data.

        Returns:
            tuple: Contains three elements:
                - current (list): List of unique battery currents (A) extracted from the first column.
                - cat (str): MATLAB-style 3D concatenation string for reconstructing 3D arrays.
                - Param (list): 3D list of battery parameters with shape (temp_length, curr_length, soc_length).

        Notes:
            - The first column of the CSV is assumed to contain current values.
            - The remaining columns represent parameters across different SOC or voltage points.
            - The function uses NumPy for array operations: https://numpy.org/doc/stable/
            - 3D reshaping is done such that the first dimension is temperature/measurement points,
            the second dimension is current, and the third dimension is SOC or parameter index.

        Example:
            current, cat, Param = batteryParams("data/", "BatteryTypeA")
        """

        # Construct full path to battery data file
        Battery     = Path + Type

        # Extract arrays from the file using post-processing helper
        Data        = self.postProcessing.extractArrays(Battery)
        Data        = dp.np.array(Data)
        Data_T      = Data[1:].T  # Transpose all columns except the first (currents)

        # Identify unique current values from first column
        current     = (dp.np.unique(Data[0])).tolist()
        
        # Determine dimensions for 3D reshaping
        temp_length = (Data[0].tolist()).count(Data[0][0]) 
        soc_length  = len(Data) - 1                         
        curr_length = len(current)                          
        curr_idx    = dp.np.array(list(range(0, curr_length)))  

        # Initialize empty 3D array
        LuT_3D      = dp.np.empty((temp_length, curr_length, soc_length))
        cat         = 'cat(3'
        
        # Fill 3D array with reshaped data
        for i in range(temp_length):
            indices             = i * curr_length + curr_idx
            LuT_3D[:][:][i]     = (Data_T[indices, :])
            cat                 = cat + ',' + 'LuT_3D' + '(:,:,' + str(i + 1) + ')'

        # Complete MATLAB-style concatenation string
        cat         = cat + ')'

        # Convert NumPy 3D array to Python list for easier handling
        Param       = LuT_3D.tolist()

        return current, cat, Param

    def Battery_OCV(self, BatteryOCVPath, battery_state):
        """
        Extract battery open-circuit voltage (OCV) vs. state-of-charge (SOC) data.

        This function reads OCV data from  CSV files and
        organizes it into a list of voltage values and corresponding SOC points.
        Useful for battery modeling, SoC estimation, and DC-DC converter simulations.

        Args:
            BatteryOCVPath (str): Directory path containing the OCV data files.
            battery_state (str): Name identifier for the battery OCV dataset.

        Returns:
            tuple: Contains two elements:
                - OCV (list): Open-circuit voltage values for each SOC point.
                - OCV_soc (list): Corresponding state-of-charge values (fraction or percentage).

        Notes:
            - The first column of the CSV is assumed to contain SOC values.
            - Remaining columns contain OCV data corresponding to those SOC points.
            - Uses NumPy for array manipulation: https://numpy.org/doc/stable/

        Example:
            OCV, OCV_soc = Battery_OCV("data/", "LiIonModuleA")
        """

        # Construct full path to OCV data file
        Battery     = BatteryOCVPath + battery_state + '_OCV'

        # Extract arrays from the file using post-processing helper
        Data        = self.postProcessing.extractArrays(Battery)
        Data        = dp.np.array(Data)

        # First column = SOC values
        OCV_soc     = dp.np.unique(Data[0]).tolist()

        # Remaining columns = OCV values
        OCV         = dp.np.array(Data[1:])
        OCV         = (OCV.T).tolist()  # Transpose so rows correspond to SOC points

        return OCV, OCV_soc

    def LuT3D_Generator(self, fileName, Xscale=1, Zscale=1, Zoffset=0):
        """

        This function reads tabular data from a file and reshapes it into a 3D array
        suitable for MATLAB-style 3D lookups. Scaling and offset options allow
        adjusting X-axis and Z-values for simulation or modeling purposes.

        Args:
            fileName (str): Path to the input data file.
            Xscale (float, optional): Scaling factor for X-axis values. Defaults to 1.
            Zscale (float, optional): Scaling factor for Z-values. Defaults to 1.
            Zoffset (float, optional): Offset for Z-values (applied before scaling). Defaults to 0.

        Returns:
            tuple: Contains three elements:
                - X_axis (list): Unique X-axis values after scaling.
                - cat (str): MATLAB-style 3D concatenation string for reconstructing 3D arrays.
                - LuT_3D (list): 3D list of scaled Z-values with shape (Z_length, X_length, Y_length).

        Notes:
            - The first column of the input file is assumed to contain X-axis values.
            - Remaining columns contain Z-values (dependent variables).
            - Uses NumPy for array manipulation: https://numpy.org/doc/stable/
            - 3D reshaping is done such that:
                - First dimension = repeated Z-values (rows per measurement)
                - Second dimension = X-axis
                - Third dimension = columns (Y-axis, typically voltage/current)

        Example:
            X_axis, cat, LuT_3D = LuT3D_Generator("data/simulation.csv", Xscale=1e3, Zscale=1e-6)
        """

        # Load the input file and convert to NumPy array
        inputFile       = fileName
        Data            = self.postProcessing.extractArrays(inputFile)
        Data            = dp.np.array(Data)
        Data_T          = Data[1:].T

        # Unique X-axis values (scaled)
        X_axis          = ((dp.np.unique(Data[0])) * Xscale).tolist()

        # Determine dimensions for 3D reshaping
        Z_length        = (Data[0].tolist()).count(Data[0][0]) 
        Y_length        = len(Data) - 1                        
        X_length        = len(X_axis)                          
        X_idx           = dp.np.array(list(range(0, X_length)))   

        # Initialize empty 3D array
        LuT_3D          = dp.np.empty((Z_length, X_length, Y_length))

        # Fill 3D array with scaled and offset data
        cat             = 'cat(3'

        for i in range(Z_length):
            indices             = i * X_length + X_idx
            LuT_3D[:][:][i]     = (Data_T[indices, :] - Data[0][0] * Zoffset) * Zscale
            cat                 = cat + ',' + 'LuT_3D' + '(:,:,' + str(i + 1) + ')'
        
        cat             = cat + ')'

        # Convert NumPy array to Python list
        LuT_3D          = LuT_3D.tolist()

        return X_axis, cat, LuT_3D

    def LuT2D_Generator(self, fileName, Xscale=1, Fscale=1):
        """

        This function reads tabular data from a file and prepares X-axis values and
        corresponding function values, with optional scaling for both axes. Useful
        for control algorithms, interpolation, or MATLAB-style 2D lookups.

        Args:
            fileName (str): Path to the input data file.
            Xscale (float, optional): Scaling factor for X-axis values. Defaults to 1.
            Fscale (float, optional): Scaling factor for function values (Y-axis). Defaults to 1.

        Returns:
            tuple: Contains two elements:
                - Xvec (list): X-axis values after scaling.
                - Fvec (list): Corresponding function values after scaling and transposing.

        Notes:
            - The first row/column of the input file is assumed to contain X-axis values.
            - Remaining rows/columns contain the function values.
            - Uses NumPy for array manipulation: https://numpy.org/doc/stable/
            - Transposition ensures that each row of Fvec corresponds to a single X value.

        Example:
            Xvec, Fvec = LuT2D_Generator("data/simulation.csv", Xscale=1e3, Fscale=1e-6)
        """

        # Load the input file and extract arrays
        inputFile       = fileName
        F_X_Vec         = self.postProcessing.extractArrays(inputFile)

        # Scale X-axis values
        Xvec            = (dp.np.array(F_X_Vec[0]) * Xscale).tolist()

        # Extract and scale function values, transpose so each row corresponds to X
        Fvec            = dp.np.array(F_X_Vec[1:])
        Fvec            = ((dp.np.array(Fvec) * Fscale).T).tolist()

        return Xvec, Fvec

    def LuT1D_Generator(self, fileName, Xscale=1, Fscale=1):
        """

        This function reads tabular data from a file and prepares X-axis values and
        corresponding function values, with optional scaling for both axes. Useful
        for control algorithms, interpolation, or MATLAB-style 1D lookups.

        Args:
            fileName (str): Path to the input data file.
            Xscale (float, optional): Scaling factor for X-axis values. Defaults to 1.
            Fscale (float, optional): Scaling factor for function values (Y-axis). Defaults to 1.

        Returns:
            tuple: Contains two elements:
                - Xvec (list): X-axis values after scaling.
                - Fvec (list): Corresponding function values after scaling.

        Notes:
            - The first row/column of the input file is assumed to contain X-axis values.
            - The second row/column contains the function values.
            - Uses NumPy for array manipulation: https://numpy.org/doc/stable/

        Example:
            Xvec, Fvec = LuT1D_Generator("data/simulation.csv", Xscale=1e3, Fscale=1e-6)
        """

        # Load the input file and extract arrays
        inputFile       = fileName
        F_X_Vec         = self.postProcessing.extractArrays(inputFile)

        # Scale X-axis values
        Xvec            = (dp.np.array(F_X_Vec[0]) * Xscale).tolist()

        # Extract and scale function values
        Fvec            = dp.np.array(F_X_Vec[1])
        Fvec            = (Fvec * Fscale).tolist()

        return Xvec, Fvec

    def limit_precision(self, nested_dict, precision):
        """
        Recursively limit the precision of numeric values in a nested dictionary or collection.

        This function traverses dictionaries, lists, tuples, and sets, truncating all numeric
        values to the specified number of significant digits. Non-numeric values are preserved
        as-is. Useful for logging, saving data, or formatting simulation results.

        Args:
            nested_dict (dict): Dictionary to process (can be nested and contain lists/tuples/sets).
            precision (int): Number of significant digits to keep.

        Returns:
            dict: Dictionary (or nested collection) with numeric values truncated to the specified precision.

        Notes:
            - Handles floats, integers, complex numbers, and numeric strings.
            - Preserves non-numeric values unchanged.
            - Maintains the structure and nesting of all collections.
        """

        def truncate_value(value):

            """Truncate individual numeric value to the specified precision."""

            if isinstance(value, float):

                # Format float to specified significant digits
                return float(f"{value:.{precision}g}")
            
            elif isinstance(value, (int, complex)):

                # Leave integer and complex numbers as-is
                return value
            
            elif isinstance(value, str):
                try:

                    # Attempt to convert string to float and format
                    float_value = float(value)

                    return f"{float_value:.{precision}g}"
                
                except ValueError:

                    # Return original string if conversion fails
                    return value
                
            # Return non-numeric values as-is
            return value

        def traverse(obj):

            """Recursively traverse and truncate values in nested collections."""
            
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

        # Start recursive traversal
        return traverse(nested_dict)

#?-------------------------------------------------------------------------------------------------------------------------------------------------------------