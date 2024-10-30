clear variables;
close all;

%% configurations

model_path = './models/head_20240920.mph';

save_dir_name = 'results_head_20240920';

save_solution_csv_file_name = 'solutions.csv';

electrode_mesh_numbers = [1607, 1680, 5818, 5244, 5018, 5233, 5729, 6312, 8460,...
    13242, 10197, 10850, 11291, 20061, 19178, 19592, 19569, 19558, 29672, 30846,...
    30462, 29468, 36184, 37476, 38303, 38314, 37099, 36326, 31425, 41115, 41295,...
    43765, 43684, 43195, 41333, 34975, 20120, 20195, 8053, 2535, 447, 118, 82];

current_intensity_milliampere = 3.0;

% 右側視神経
selections_right_opticus_nerve = [66, 772];

% 左側視神経
selections_left_opticus_nerve = [1978];

% 右側三叉神経
selections_right_trigeminal_nerve = [739];

% 左側三叉神経
selections_left_trigeminal_nerve = [1995];

% その他の神経
selections_other_nerves = [29, 527, 804, 831, 1157, 1201, 1235, 1266, 1325,...
    1676, 1816, 1968, 2000, 2032, 2184, 2371];

domains_plot_groups = {
    {'ALL', 'pg1'}; {'SKIN', 'pg2'}; {'BONE', 'pg3'}; {'CIRCULATORY', 'pg4'};
    {'RIG_OPT_NERVE', 'pg5'}; {'LEF_OPT_NERVE', 'pg6'};
    {'RIG_TRI_NERVE', 'pg7'}; {'LEF_TRI_NERVE', 'pg8'}; {'OTHER_NERVES', 'pg9'};
};

%% calculation process

if ~exist(save_dir_name, 'dir')
    mkdir(save_dir_name)
end

saveSolutionPath = fullfile(save_dir_name, save_solution_csv_file_name);
if ~exist(saveSolutionPath, 'file')
    header = {'Condition', 'Anode', 'Cathode',...
    'RIG OPT nerve', 'LEF OPT nerve',...
    'RIG TRI nerve', 'LEF TRI nerve', 'other nerves'};

    writecell(header, saveSolutionPath, 'WriteMode', 'append');
end

stimulationConditions = [];
id = 1;
numElectrodes = length(electrode_mesh_numbers);
for i = 1:numElectrodes-1
    for j = i+1:numElectrodes
        diff1 = mod(i-j, length(electrode_mesh_numbers));
        diff2 = mod(j-i, length(electrode_mesh_numbers));
        if diff1 <= 40 || diff2 <= 40
            anode = electrode_mesh_numbers(i);
            cathode = electrode_mesh_numbers(j);
            condition = StimulationCondition(id, anode, cathode);
            stimulationConditions{end+1} = condition;
            id = id + 1;
        end
    end
end

for stimulationCondition = stimulationConditions

    stimulationCondition = stimulationCondition{1};

    saveSolutionTable = readtable(saveSolutionPath, 'VariableNamingRule', 'preserve');
    containedRow = any((saveSolutionTable.Anode == stimulationCondition.AnodeSelection)...
        & (saveSolutionTable.Cathode == stimulationCondition.CathodeSelection));
    is_solution_exist = any(containedRow);


    if is_solution_exist
        disp(strcat('[SKIP]', ' ', num2str(stimulationCondition.Condition), ' / ', num2str(length(stimulationConditions))));
        continue;
    else
        disp(strcat('[CALCULATE]', ' ', num2str(stimulationCondition.Condition), ' / ', num2str(length(stimulationConditions))));
         
        % load model
        model = mphopen(model_path);
        
        % set electrode position
        model.component('comp1').selection('sel1').set(stimulationCondition.AnodeSelection);
        model.component('comp1').selection('sel2').set(stimulationCondition.CathodeSelection);
        
        % set electrical stimulation intensity
        anodeAreaSquareMeter = mphint2(model, '1', 'surface', 'selection', stimulationCondition.AnodeSelection);
        normal_current_density = current_intensity_milliampere / anodeAreaSquareMeter * 0.001; % [A/m^2]
        model.component('comp1').physics('ec').feature('ncd1').set('nJ', normal_current_density);
        
        % run calculation
        model.study('std1').run;

        % save rendering cache
        for i=1:length(domains_plot_groups)
            domainsPlotGroup = domains_plot_groups{i};

            plotData = mphplot(model, domainsPlotGroup{2}, 'rangenum', 1, 'createplot', 'off');
            plotJsonString = jsonencode(plotData);

            cacheFileName = strcat('HEAD', ...
                '-', num2str(stimulationCondition.AnodeSelection),...
                '-', num2str(stimulationCondition.CathodeSelection),...
                '-', domainsPlotGroup{1}, '.txt');
            
            saveCachePath = fullfile(save_dir_name, cacheFileName);
            fileId = fopen(saveCachePath, 'w');
            fprintf(fileId, '%s', plotJsonString);
            fclose(fileId);
        end

        % evaluate max current density in each domain
        solRigOptNerve = getMaxCurrentDensityInDomain(model, selections_right_opticus_nerve);
        solLefOptNerve = getMaxCurrentDensityInDomain(model, selections_left_opticus_nerve);
        solRigTriNerve = getMaxCurrentDensityInDomain(model, selections_right_trigeminal_nerve);
        solLefTriNerve = getMaxCurrentDensityInDomain(model, selections_left_trigeminal_nerve);
        solOtherNerves = getMaxCurrentDensityInDomain(model, selections_other_nerves);
        
        % save solution
        solutions = [stimulationCondition.Condition, stimulationCondition.AnodeSelection, stimulationCondition.CathodeSelection,...
            solRigOptNerve, solLefOptNerve,...
            solRigTriNerve, solLefTriNerve, solOtherNerves];
        writematrix(solutions, saveSolutionPath, 'WriteMode', 'append');
    end
end

%% functions
function maxCurrentDensityInDomain = getMaxCurrentDensityInDomain(model, targetDomainSelections)
    maxCurrentDensityInDomain = 0;
    for selection = targetDomainSelections
        maxCurrentDensityInSelection = mphmax(model, 'ec.normJ', 'volume', 'selection', selection);
        if maxCurrentDensityInSelection > maxCurrentDensityInDomain
            maxCurrentDensityInDomain = maxCurrentDensityInSelection;
        end
    end
end
