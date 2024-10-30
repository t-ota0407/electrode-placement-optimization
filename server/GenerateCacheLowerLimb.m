clear variables;
close all;

%% configurations

model_path = './models/lower_limb.mph';

save_dir_name = 'results';

save_solution_csv_file_name = 'solutions.csv';

electrode_mesh_numbers = [21454, 22301, 21852, 21052, 20517, 19270, 27698,...
    26966, 26375, 25386, 32098, 31095, 30693, 30478, 36994, 36281, 36443,...
    34656, 34796, 34626, 37807, 37535, 37238, 36918, 35845, 36350, 35102,...
    34992, 35843, 35935, 34490, 34277, 34641, 35999, 31669, 31893, 31677,...
    31517, 27007, 26381, 26754, 26358, 19919, 19951, 19984, 19385, 13357,...
    12497, 11871, 11158, 7358, 6815, 6770, 6669, 6436, 6235, 5568, 6142,...
    4743, 4718, 4701, 4533, 5024, 4693, 4554, 3857, 7223, 6303, 5476, 4876,...
    12152, 10106, 9162, 7763, 15983, 16231, 16019, 14665, 12792, 11943];

current_intensity_milliampere = 3.0;

% 前脛骨筋
selections_ta_muscle = [159];

% 腓腹筋
selections_gas_muscle = [104];

% 長腓骨筋
selections_pl_muscle = [10];

% 長趾屈筋
selections_fdl_muscle = [3088, 3375];

% その他の筋
selections_other_muscles = [702, 2147, 3921, 3998, 5, 2914, 2946, 3012, 3224,...
    3399, 2107, 2028, 3200, 3559, 3584, 3595, 3597, 3599, 3604, 3607, 3610,...
    3612, 3615, 3628, 3642, 3656, 3664, 757, 527, 483, 692, 1400, 2305, 2424,...
    2483, 2571, 2838, 2999, 408, 1071, 1207, 2035, 2138, 2915, 449, 1122,...
    1329, 2230, 2961, 3033, 3050, 3066, 3073, 3089, 1046, 1087, 3334, 3451,...
    3485, 3493, 3547, 3590, 3640, 3654, 3663, 3690, 3692, 2899, 174, 233,...
    258, 360, 396, 446, 485, 518, 563, 599, 659, 1377, 2326, 2464, 2487, 2548,...
    2553, 2593, 2598, 2754, 2775, 116, 149, 860, 3227, 3229, 3248, 3263, 3408,...
    2184, 3398, 3424, 3457, 3477, 3516, 3609, 3666, 306, 447, 475, 522, 557,...
    565, 567, 654, 660, 664, 707, 762, 766, 781, 813, 830, 831, 851, 853, 889,...
    900, 905, 921, 922, 961, 974, 979, 988, 995, 1015, 1016, 1028, 1032, 1051,...
    1053, 1058, 1070, 1083, 1109, 1110, 1145, 1149, 1174, 1180, 1181, 1182,...
    1183, 1191, 1265, 1279, 1281, 1373, 1422, 1458, 1534, 1580, 1654, 1696,...
    1712, 1716, 1736, 1784, 1790, 1839, 1846, 1923, 2023, 2033, 2110, 2112,...
    2206, 2224, 2311, 2484, 2508, 2538, 907, 936, 990, 1494, 1540, 1572, 1575,...
    1584, 1600, 1627, 1635, 2458, 523, 2704, 2853, 3281, 3611, 56, 25, 32, 34,...
    38, 41, 44, 63, 64, 71, 73, 77, 79, 81, 84, 88, 99, 100, 101, 113, 115,...
    121, 124, 125, 126, 128, 129, 133, 134, 137, 140, 141, 144, 153, 154, 156,...
    160, 162, 163, 166, 171, 175, 176, 179, 183, 184, 186, 187, 190, 191, 194,...
    195, 197, 198, 203, 207, 208, 212, 214, 215, 216, 217, 218, 220, 222, 223,...
    226, 230, 234, 235, 236, 238, 239, 240, 241, 242, 243, 244, 246, 249, 252,...
    253, 254, 255, 256, 259, 260, 261, 262, 263, 267, 268, 269, 271, 273, 274,...
    275, 277, 278, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291];

% 前脛骨筋腱（前側）
selections_ta_tendon = [2523];

% アキレス腱（後側）
selections_ac_tendon = [2720, 3549];

% 長腓骨筋腱（外側）
selections_pl_tendon = [688];

% 長趾屈筋腱（内側）
selections_fdl_tendon = [3384, 3397];

% 深腓骨神経
selections_dpn_nerve = [225, 229, 257, 266];

% 浅腓骨神経
selections_spn_nerve = [151];

% 脛骨神経
selections_ti_nerve = [2806];

% 腓腹神経
selections_su_nerve = [92, 997];

% その他の神経
selections_other_nerves = [2282, 2715, 3368];

domains_plot_groups = {
    {'ALL', 'pg1'}; {'SKIN', 'pg4'}; {'BONE', 'pg5'}; {'CIRCULATORY', 'pg6'};
    {'TA_MUSCLE', 'pg7'}; {'GAS_MUSCLE', 'pg8'}; {'FDL_MUSCLE', 'pg9'}; {'PL_MUSCLE', 'pg10'}; {'OTHER_MUSCLES', 'pg11'};
    {'TA_TENDON', 'pg12'}; {'AC_TENDON', 'pg13'}; {'FDL_TENDON', 'pg14'}; {'PL_TENDON', 'pg15'};
    {'DPN_NERVE', 'pg16'}; {'SPN_NERVE', 'pg17'}; {'TI_NERVE', 'pg18'}; {'SU_NERVE', 'pg19'}; {'OTHER_NERVES', 'pg20'};
};

%% calculation process

if ~exist(save_dir_name, 'dir')
    mkdir(save_dir_name)
end

saveSolutionPath = fullfile(save_dir_name, save_solution_csv_file_name);
if ~exist(saveSolutionPath, 'file')
    header = {'Condition', 'Anode', 'Cathode',...
    'TA muscle', 'GAS muscle', 'PL muscle', 'FDL muscle', 'other muscles',...
    'TA tendon', 'AC tendon', 'PL tendon', 'FDL tendon',...
    'DPN nerve', 'SPN nerve', 'TI nerve', 'SU nerve', 'other nerves'};

    writecell(header, saveSolutionPath, 'WriteMode', 'append');
end

stimulationConditions = [];
id = 1;
numElectrodes = length(electrode_mesh_numbers);
for i = 1:numElectrodes-1
    for j = i+1:numElectrodes
        diff1 = mod(i-j, length(electrode_mesh_numbers));
        diff2 = mod(j-i, length(electrode_mesh_numbers));
        if diff1 <= 20 || diff2 <= 20
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
        solTaMuscle = getMaxCurrentDensityInDomain(model, selections_ta_muscle);
        solGasMuscle = getMaxCurrentDensityInDomain(model, selections_gas_muscle);
        solPlMuscle = getMaxCurrentDensityInDomain(model, selections_pl_muscle);
        solFdlMuscle = getMaxCurrentDensityInDomain(model, selections_fdl_muscle);
        solOtherMuscles = getMaxCurrentDensityInDomain(model, selections_other_muscles);
        solTaTendon = getMaxCurrentDensityInDomain(model, selections_ta_tendon);
        solAcTendon = getMaxCurrentDensityInDomain(model, selections_ac_tendon);
        solPlTendon = getMaxCurrentDensityInDomain(model, selections_pl_tendon);
        solFdlTendon = getMaxCurrentDensityInDomain(model, selections_fdl_tendon);
        solDpnNerve = getMaxCurrentDensityInDomain(model, selections_dpn_nerve);
        solSpnNerve = getMaxCurrentDensityInDomain(model, selections_spn_nerve);
        solTiNerve = getMaxCurrentDensityInDomain(model, selections_ti_nerve);
        solSuNerve = getMaxCurrentDensityInDomain(model, selections_su_nerve);
        solOtherNerves = getMaxCurrentDensityInDomain(model, selections_other_nerves);
        
        % save solution
        solutions = [stimulationCondition.Condition, stimulationCondition.AnodeSelection, stimulationCondition.CathodeSelection,...
            solTaMuscle, solGasMuscle, solPlMuscle, solFdlMuscle, solOtherMuscles,...
            solTaTendon, solAcTendon, solPlTendon, solFdlTendon,...
            solDpnNerve, solSpnNerve, solTiNerve, solSuNerve, solOtherNerves];
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
