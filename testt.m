
%% Sweep data
data = [
    [20, 200, 5];
    [20, 200, 10];
    [20, 300, 5];
    [20, 300, 10];
    [25, 200, 5];
    [25, 200, 10];
    [25, 300, 5];
    [25, 300, 10];
    [30, 200, 5];
    [30, 200, 10];
    [30, 300, 5];
    [30, 300, 10];
    ];

% define mdlVars as empty struct in initialization

t = localtime(time());
fprintf('Date               : %s\n', strftime("%r (%Z) %A %e %B %Y", t));
fprintf('Time               : %s\n', strftime("%H:%M:%S", t));
fprintf('Iterations         : %d\n', size(data, 1));


for sim = 1:size(data, 1)

    fprintf('\n');
    %% ------------------------------------------------------------------------
    fprintf('%s\n', '-' * ones(1, 90));

    fprintf('Iteration Number   : %d\n\n', sim);
    fprintf('\n');

    mdlVars    = struct();
    % Assign value
    mdlVars.Common.Thermal.Twater = data(sim, 1);

    % Print aligned output
    fprintf('%-18s : %-45s = %12g\n', 'Water Temperature', 'mdlVars.Common.Thermal.Twater', data(sim, 1));

    % Assign value
    mdlVars.DCDC_Rail1.Control.Inputs.Vin = data(sim, 2);

    % Print aligned output
    fprintf('%-18s : %-45s = %12g\n', 'Input Voltage', 'mdlVars.DCDC_Rail1.Control.Inputs.Vin', data(sim, 2));

    % Assign value
    mdlVars.Common.Control.Targets.Vout = data(sim, 3);

    % Print aligned output
    fprintf('%-18s : %-45s = %12g\n', 'Output Current', 'mdlVars.Common.Control.Targets.Vout', data(sim, 3));

    fprintf('\n');
    %% ------------------------------------------------------------------------

end

fprintf('\nComplete! Ran %d simulations\n', size(data, 1));fprintf('%s\n', '-' * ones(1, 90));

