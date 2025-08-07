class ParamProcess:
    def __init__(self):
        """Initialize the ParamProcess class with essential post-processing and simulation utilities.
        
        The constructor sets up two key components:
        - postProcessing: An instance of Processing class from Dependencies for data extraction and manipulation
        - simutil: An instance of SimulationUtils from Dependencies for simulation-related operations
        
        These components are used throughout the class methods for various parameter processing tasks.
        """

    def MOSFETcaps(self, path, switch_name, type):
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

    def Forward_Transfer_data(self, switchesTransferPath, switch_name):
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

    def MOSFETenergies(self, path, switch_name, type):
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

    def MOSFETrdson(self, path, switch_name, type):
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

    def DiodeVI_data(self, DiodeVIPath, diode_name):
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

    def Mags_CoreLoss_Data(self, TrafoCoreLossesPath, trafo_name):
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

    def Mags_FreqRes_Data(self, FreqResistancePath, mag_name):
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

    def Mags_LI_Data(self, InductanceCurrentPath, mag_name):
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

    def linearDerating(self, X1, X2, Y1, Y2, Ymin, Ymax, X):
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

    def scaledList(self, arrayList, scale=1.0):
        """Scale numerical values in nested list structure.
        
        Applies uniform scaling factor to all elements while preserving structure.
        Handles both regular lists and numpy arrays.
        
        Args:
            arrayList: Nested list/array structure containing numerical values
            scale: Multiplicative scaling factor (default=1.0)
            
        Returns:
            list: Scaled array with original structure, transposed
        """

    def getCoss(self, switch, blockingVoltage, time_energy):
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

    def PrechargeILVref(self, V_snub, V_LV_OP, Np, Ns, fs, Lfilter, Lks, Lkp, I_C_max, ILVmax, tonsnubmin, Points):
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

    def dcdcAverageModelCalculate(self, ModelVars):
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

    def Battery_Rs(self, RsdataPath, Rs_state):
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

    def Battery_OCV(self, BatteryOCVPath, battery_state):
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

    def LuT3D_Generator(self, fileName, Xscale=1, Zscale=1, Zoffset=0):
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

    def limit_precision(self, nested_dict, precision):
        """Recursively limit numerical precision in nested dictionary.
        
        Processes all numerical values (int, float, numeric strings) to specified
        significant digits while preserving data structure.
        
        Args:
            nested_dict: Input dictionary (may contain nested dicts/lists)
            precision: Number of significant digits to retain
            
        Returns:
            dict: Processed dictionary with limited precision values
        """