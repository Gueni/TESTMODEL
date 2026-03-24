% Simulation Sweep Script 
plecs('clc');                                   % Clear Console.
plecs('warning', 'warning message');            % Display Warnings.

%% Sweep data
% 3D data structure
data = {
    { [25, 300, 5, 180], [25, 300, 10, 280], [3, 5, 0.6, 9], [25, 300, 5, 180] };
    { [20, 200, 10, 200], [20, 300, 10, 250], [3, 5, 0.6, 9], [20, 200, 10, 200] };
    { [20, 300, 5, 150], [20, 300, 10, 250], [3, 5, 0.6, 9], [20, 200, 10, 200] };
    { [20, 300, 10, 250], [20, 300, 10, 250], [3, 5, 0.6, 9], [20, 200, 10, 200] };
    { [25, 200, 5, 120], [20, 300, 10, 250], [3, 5, 0.6, 9], [20, 200, 10, 200] };
    { [25, 200, 10, 220], [20, 300, 10, 250], [3, 5, 0.6, 9], [20, 200, 10, 200] };
    { [25, 300, 5, 180], [20, 300, 10, 250], [3, 5, 0.6, 9], [20, 200, 10, 200] };
    { [25, 300, 10, 280], [20, 300, 10, 250], [3, 5, 0.6, 9], [20, 200, 10, 200] };
    { [30, 200, 5, 140], [20, 300, 10, 250], [3, 5, 0.6, 9], [20, 200, 10, 200] };
    { [30, 200, 10, 240], [20, 300, 10, 250], [3, 5, 0.6, 9], [20, 200, 10, 200] };
    { [30, 300, 5, 190], [20, 300, 10, 250], [3, 5, 0.6, 9], [20, 200, 10, 200] };
    { [30, 300, 10, 290], [20, 300, 10, 250], [3, 5, 0.6, 9], [20, 200, 10, 200] }};

simStruct = struct('ModelVars', struct('DCDC_Rail1', struct('Control', struct('Inputs', struct('Vin', 0, 'Pout', 0, 'Vout', 0, 'Iin', 0))), 'Common', struct('Control', struct('Targets', struct('Pout', 0, 'Vout', 0)), 'ToFile', struct('FileNameStandalone', ''), 'Thermal', struct('Twater', 0), 'Load', struct('Front', struct('R_L', 0)))), 'SolverOpts', struct());

t = localtime(time());
fprintf('Date               : %s\n', strftime("%r (%Z) %A %e %B %Y", t));
fprintf('Time               : %s\n', strftime("%H:%M:%S", t));
fprintf('Iterations         : %d\n', size(data, 1));

for sim = 1:size(data, 1)
    
    % Construct filename using strcat with simulation number
    filename = strcat('D:\WORKSPACE\TESTMODEL\simulation_results\standalonefiletest', sprintf('_%03d.csv', sim));

    % Assign filename to ToFile block
    simStruct.ModelVars.Common.ToFile.FileNameStandalone = filename;
    
    % Print filename for verification
    fprintf('Output File: %s\n', filename);


    fprintf('\n');
    %% ------------------------------------------------------------------------
    fprintf('%s\n', '-' * ones(1, 90));
    fprintf('Iteration Number   : %d\n\n', sim);
    fprintf('\n');

    % Assign value
    simStruct.ModelVars.Common.Thermal.Twater = data{sim}{1}(1);
    
    % Print evaluated value
    fprintf('%-50s = %12g\n','simStruct.ModelVars.Common.Thermal.Twater', simStruct.ModelVars.Common.Thermal.Twater);
    % Assign value
    simStruct.ModelVars.DCDC_Rail1.Control.Inputs.Vin = data{sim}{2}(3);
    
    % Print evaluated value
    fprintf('%-50s = %12g\n','simStruct.ModelVars.DCDC_Rail1.Control.Inputs.Vin', simStruct.ModelVars.DCDC_Rail1.Control.Inputs.Vin);
    % Assign value
    simStruct.ModelVars.Common.Control.Targets.Vout = data{sim}{3}(1);
    
    % Print evaluated value
    fprintf('%-50s = %12g\n','simStruct.ModelVars.Common.Control.Targets.Vout', simStruct.ModelVars.Common.Control.Targets.Vout);
    % Assign value
    simStruct.ModelVars.Common.Control.Targets.Pout = data{sim}{4}(2);
    
    % Print evaluated value
    fprintf('%-50s = %12g\n','simStruct.ModelVars.Common.Control.Targets.Pout', simStruct.ModelVars.Common.Control.Targets.Pout);
    % Assign value
    simStruct.ModelVars.DCDC_Rail1.Control.Inputs.Vin = data{sim}{2}(3);
    
    % Print evaluated value
    fprintf('%-50s = %12g\n','simStruct.ModelVars.DCDC_Rail1.Control.Inputs.Vin', simStruct.ModelVars.DCDC_Rail1.Control.Inputs.Vin);
    % Assign value
    simStruct.ModelVars.DCDC_Rail1.Control.Inputs.Iin = data{sim}{2}(4);
    
    % Print evaluated value
    fprintf('%-50s = %12g\n','simStruct.ModelVars.DCDC_Rail1.Control.Inputs.Iin', simStruct.ModelVars.DCDC_Rail1.Control.Inputs.Iin);
    % Assign value
    simStruct.ModelVars.DCDC_Rail1.Control.Inputs.Vout = data{sim}{3}(1);
    
    % Print evaluated value
    fprintf('%-50s = %12g\n','simStruct.ModelVars.DCDC_Rail1.Control.Inputs.Vout', simStruct.ModelVars.DCDC_Rail1.Control.Inputs.Vout);
    % Assign value
    simStruct.ModelVars.DCDC_Rail1.Control.Inputs.Pout = data{sim}{4}(2);
    
    % Print evaluated value
    fprintf('%-50s = %12g\n','simStruct.ModelVars.DCDC_Rail1.Control.Inputs.Pout', simStruct.ModelVars.DCDC_Rail1.Control.Inputs.Pout);
    % Assign value
    simStruct.ModelVars.Common.Load.Front.R_L = data{sim}{3}(1)^2/data{sim}{4}(2)*1e-9;
    
    % Print evaluated value
    fprintf('%-50s = %12g\n','simStruct.ModelVars.Common.Load.Front.R_L', simStruct.ModelVars.Common.Load.Front.R_L);
    % Assign value
    simStruct.ModelVars.Common.Load.Front.R_L = 20^2/20*1e-9 + data{sim}{1}(1);
    
    % Print evaluated value
    fprintf('%-50s = %12g\n','simStruct.ModelVars.Common.Load.Front.R_L', simStruct.ModelVars.Common.Load.Front.R_L);

    fprintf('\n');
    %% ------------------------------------------------------------------------
    plecs('simulate', simStruct);
    %% ------------------------------------------------------------------------
end

fprintf('\nComplete! Ran %d Iterations\n', size(data, 1));
fprintf('%s\n', '-' * ones(1, 90));