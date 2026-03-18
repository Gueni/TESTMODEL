% Simulation Sweep Script 
plecs('clc');                                           % Clear Console.
plecs('warning', 'warning message');                    % Display Warnings.

%% Configuration
RESULTS_DIR     = 'D:\WORKSPACE\TESTMODEL\simulation_results';               % Directory for results
HOLD_TRACES     = true;                                 % Set to true to hold traces after each simulation
CLEAR_TRACES    = true;                                 % Set to true to clear traces before starting
SAVE_TRACES     = true;                                 % Set to true to save traces to files

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

simStruct = struct('ModelVars', struct('Common', struct('Thermal', struct('Twater', 0), 'Load', struct('Front', struct('R_L', 0)), 'Control', struct('Targets', struct('Vout', 0, 'Pout', 0))), 'DCDC_Rail1', struct('Control', struct('Inputs', struct('Vin', 0, 'Iin', 0, 'Pout', 0, 'Vout', 0)))), 'SolverOpts', struct());

% Get model name and scope list
mdl = plecs('get', '', 'CurrentCircuit');
mdl_name = (strsplit(mdl, filesep)){end};               % Extract just the model name
mdl_name = (strsplit(mdl_name, '.')){1};                % Remove extension

% List of scopes in the model
scopes = { "Line-to-Line", "Lines-to-Neutral", " Lines-to-Chassis" };

% Clear all traces before starting if enabled
if CLEAR_TRACES
    for i = 1:length(scopes)
        try
            plecs('scope', [mdl '/' scopes{i}], 'ClearTraces');
        catch
            % Silently ignore errors
        end
    end
end

% Create results directory if saving is enabled
if SAVE_TRACES
    if ~exist(RESULTS_DIR, 'dir')
        mkdir(RESULTS_DIR);
    end
    
    % Create traces directory
    traces_dir = fullfile(RESULTS_DIR, 'Scopes_Traces');
    if ~exist(traces_dir, 'dir')
        mkdir(traces_dir);
    end
end

t = localtime(time());
fprintf('Date               : %s\n', strftime("%r(%Z) %A %e %B %Y", t));
fprintf('Time               : %s\n', strftime("%H:%M:%S", t));
fprintf('Model              : %s\n', mdl_name);
fprintf('Iterations         : %d\n', size(data, 1));

for sim = 1:size(data, 1)

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
    
    %% Hold traces for all scopes if enabled
    if HOLD_TRACES
        trace_name = sprintf('Iteration_%d_Standalone', sim);
        for i = 1:length(scopes)
            try
                plecs('scope', [mdl '/' scopes{i}], 'HoldTrace', trace_name);
            catch
                % Silently ignore errors
            end
        end
    end
    

    
    %% ------------------------------------------------------------------------
end

%% Save traces once per scope after all iterations
if SAVE_TRACES
    for i = 1:length(scopes)
        try
            scope_path = [mdl '/' scopes{i}];
            % Replace any slashes in scope name for filename
            safe_scope_name = strrep(scopes{i}, '/', '_');
            trace_file = fullfile(traces_dir, sprintf('%s', safe_scope_name));
            plecs('scope', scope_path, 'SaveTraces', trace_file);
        catch
            % Silently ignore errors
        end
    end
end

fprintf('\nComplete! Ran %d Iterations\n', size(data, 1));
if SAVE_TRACES
    fprintf('Traces saved in    : %s\n', traces_dir);
end
fprintf('%s\n', '-' * ones(1, 90));