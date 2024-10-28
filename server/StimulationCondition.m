classdef StimulationCondition
    properties
        Condition {mustBeInteger}
        AnodeSelection {mustBeNonnegative}
        CathodeSelection {mustBeNonnegative}
    end
    methods
        function obj = StimulationCondition(condition, anode_mesh, cathode_mesh)
            obj.Condition = condition;
            obj.AnodeSelection = anode_mesh;
            obj.CathodeSelection = cathode_mesh;
        end
        function r = str(obj)
            r = append('StimulationCondition {',...
                ' Condition: ', num2str(obj.Condition), ',',...
                ' Anode: ', num2str(obj.AnodeSelection), ',',...
                ' Cathode: ', num2str(obj.CathodeSelection),...
                ' }');
        end
        function r = repr(obj)
            r = append(num2str(obj.Condition), '_', num2str(obj.AnodeSelection), '_', num2str(obj.CathodeSelection));
        end
    end
end
