clear variables;
close all;

%% configurations

model_path = './models/upper_limb.mph';

save_dir_name = 'results_upperlimb';

save_solution_csv_file_name = 'solutions.csv';

electrode_mesh_numbers = [2456, 2966, 4327, 4601, 3342, 4389, 5130, 5893, 5232,...
    6317, 7120, 8358, 7298, 8478, 9822, 10609, 9567, 10538, 11282, 12167, 10960,...
    11667, 12410, 13044, 11382, 12000, 12573, 13314, 10735, 11476, 12347, 12733,...
    8602, 9862, 11096, 11900, 5944, 7192, 8768, 10001, 4129, 5150, 6094, 6901,...
    2781, 3252, 4306, 4907, 2405, 2825, 3486, 4378];

current_intensity_milliampere = 3.0;

% 浅指屈筋腱
selections_fd_muscle = [37, 640];

% 伸筋
selections_ex_muscle = [23, 401];

% その他の筋
selections_other_muscles = [4, 6, 10, 11, 12, 13, 14, 15, 18, 22, 28, 29, 36,...
    38, 42, 46, 49, 50, 51, 56, 57, 58, 61, 64, 69, 70, 72, 77, 79, 82, 87, 98,...
    109, 115, 119, 126, 128, 131, 132, 133, 134, 140, 151, 158, 162, 165, 169,...
    172, 175, 178, 179, 181, 184, 185, 190, 192, 202, 203, 206, 209, 219, 220,...
    223, 226, 244, 274, 280, 283, 291, 294, 314, 315, 320, 323, 324, 327, 334,...
    335, 336, 340, 341, 342, 343, 345, 350, 351, 354, 356, 359, 360, 366, 369,...
    372, 373, 375, 378, 380, 381, 382, 386, 387, 389, 392, 393, 394, 395, 396,...
    398, 400, 403, 404, 409, 410, 412, 417, 418, 419, 420, 425, 428, 429, 430,...
    431, 434, 435, 436, 452, 460, 461, 464, 466, 470, 473, 474, 477, 479, 482,...
    488, 492, 494, 496, 498, 499, 501, 503, 504, 511, 512, 515, 516, 517, 518,...
    520, 521, 523, 526, 527, 528, 530, 532, 533, 534, 535, 536, 537, 538, 540,...
    541, 542, 543, 544, 546, 547, 554, 556, 557, 558, 561, 564, 570, 571, 572,...
    573, 574, 575, 576, 579, 580, 586, 587, 589, 591, 599, 609, 611, 623, 626,...
    645, 671, 680, 692, 710, 785, 789, 794, 795, 802, 804, 806, 809, 810, 814,...
    820, 823, 824, 830, 876];

% 浅指屈筋腱（内側）
selections_fd_tendon = [304];

% 伸筋腱（外側）
selections_ex_tendon = [25, 86, 161, 237];

% 橈骨神経
selections_rad_nerve = [191, 397, 433, 697];

% 正中神経
selections_med_nerve = [338, 486, 762, 831, 903];

% 尺骨神経
selections_ul_nerve = [487, 620];

% その他の神経
selections_other_nerves = [365, 506, 650, 704, 705, 731, 735, 756, 776, 788,...
    811, 915];

domains_plot_groups = {
    {'ALL', 'pg1'}; {'SKIN', 'pg4'}; {'BONE', 'pg5'}; {'CIRCULATORY', 'pg6'};
    {'FD_MUSCLE', 'pg7'}; {'EX_MUSCLE', 'pg8'}; {'OTHER_MUSCLES', 'pg9'};
    {'FD_TENDON', 'pg10'}; {'EX_TENDON', 'pg11'};
    {'RAD_NERVE', 'pg12'}; {'MED_NERVE', 'pg13'}; {'UL_NERVE', 'pg14'}; {'OTHER_NERVES', 'pg15'};
};

%% calculation process

if ~exist(save_dir_name, 'dir')
    mkdir(save_dir_name)
end

saveSolutionPath = fullfile(save_dir_name, save_solution_csv_file_name);
if ~exist(saveSolutionPath, 'file')
    header = {'Condition', 'Anode', 'Cathode',...
    'FD muscle', 'EX muscle', 'other muscles',...
    'FD tendon', 'EX tendon',...
    'RAD nerve', 'MED nerve', 'UL nerve', 'other nerves'};

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

            cacheFileName = strcat('LOWER_LIMB', ...
                '-', num2str(stimulationCondition.AnodeSelection),...
                '-', num2str(stimulationCondition.CathodeSelection),...
                '-', domainsPlotGroup{1}, '.txt');
            
            saveCachePath = fullfile(save_dir_name, cacheFileName);
            fileId = fopen(saveCachePath, 'w');
            fprintf(fileId, '%s', plotJsonString);
            fclose(fileId);
        end

        % evaluate max current density in each domain
        solFdMuscle = getMaxCurrentDensityInDomain(model, selections_fd_muscle);
        solExMuscle = getMaxCurrentDensityInDomain(model, selections_ex_muscle);
        solOtherMuscles = getMaxCurrentDensityInDomain(model, selections_other_muscles);
        solFdTendon = getMaxCurrentDensityInDomain(model, selections_fd_tendon);
        solExTendon = getMaxCurrentDensityInDomain(model, selections_ex_tendon);
        solRadNerve = getMaxCurrentDensityInDomain(model, selections_rad_nerve);
        solMedNerve = getMaxCurrentDensityInDomain(model, selections_med_nerve);
        solUlNerve = getMaxCurrentDensityInDomain(model, selections_ul_nerve);
        solOtherNerves = getMaxCurrentDensityInDomain(model, selections_other_nerves);
        
        % save solution
        solutions = [stimulationCondition.Condition, stimulationCondition.AnodeSelection, stimulationCondition.CathodeSelection,...
            solFdMuscle, solExMuscle, solOtherMuscles,...
            solFdTendon, solExTendon,...
            solRadNerve, solMedNerve, solUlNerve, solOtherNerves];
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
