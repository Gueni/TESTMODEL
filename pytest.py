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
mdlVars    = struct();

solverOpts = struct('StopTime', 0);
simStruct  = struct('mdlVars', mdlVars, 'SolverOpts', solverOpts);

fprintf('Running %d simulations...\n\n', size(data, 1));

fprintf('Total Iterations :\n');
%% Print summary table header
fprintf('\n%s\n', '=' * ones(1, 70));
fprintf('%-12s', 'Iter');
for i = 1:length(sweepnames)
    fprintf('  %-18s', sweepnames{i});
end
fprintf('\n');
fprintf('%s\n', '-' * ones(1, 70));

for sim = 1:size(data, 1)
     % Print summary line
    fprintf('%-12d', sim);
    for col = 1:size(data, 2)
        fprintf('  %-18g', data(sim, col));
    end
    fprintf('\n');

    % Print detailed info every iteration
    fprintf('\n');
    fprintf('  Detailed assignment for iteration %d:\n', sim);

    fprintf('\n');
    %% ------------------------------------------------------------------------
    fprintf('****************************************************************\n');
    t = localtime(time());
    fprintf('****************************************************************\n');
    fprintf('Date               : %s\n', strftime("%r (%Z) %A %e %B %Y", t));
    fprintf('Time               : %s\n', strftime("%H:%M:%S", t));
    fprintf('Iteration Number   : %d\n\n', sim);
    fprintf('\n');
    fprintf('****************************************************************\n');
    fprintf('\n');


    % Assign value
    simStruct.mdlVars.Common.Thermal.Twater = data(sim, 1);

    % Print aligned output
    fprintf('%-25s : simStruct.%-45s = %12g\n','Water Temperature', 'mdlVars.Common.Thermal.Twater', data(sim, 1));

    % Assign value
    simStruct.mdlVars.DCDC_Rail1.Control.Inputs.Vin = data(sim, 2);

    % Print aligned output
    fprintf('%-25s : simStruct.%-45s = %12g\n','Input Voltage', 'mdlVars.DCDC_Rail1.Control.Inputs.Vin', data(sim, 2));

    % Assign value
    simStruct.mdlVars.Common.Control.Targets.Vout = data(sim, 3);

    % Print aligned output
    fprintf('%-25s : simStruct.%-45s = %12g\n','Output Current', 'mdlVars.Common.Control.Targets.Vout', data(sim, 3));

    fprintf('\n');
    %% ------------------------------------------------------------------------


    %% ------------------------------------------------------------------------

end

fprintf('\nComplete! Ran %d simulations\n', size(data, 1));
fprintf('****************************************************************\n');