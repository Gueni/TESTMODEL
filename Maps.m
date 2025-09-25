%% import simulation data
clear
clc
close all

currentdirectory    =   pwd;
folders             =   dir(currentdirectory);

%% select desired folder and parameters
data                =   folders(12).name;
resultsFolder       =   dir(data);
csvFolder           =   resultsFolder(3).name;
csvMaps             =   dir(strcat(pwd,'\',data,'\',csvFolder));
csvNames            =   cell(1,2);
combinedMap         =   [];
csvNamesOrder       =   [3,4,6,7,10,11,12,13,14,15];
for i = 1:length(csvNamesOrder)
    csvNames{i}     =   csvMaps(csvNamesOrder(i)).name;
    x               =   load(csvNames{i});
    combinedMap     =   [combinedMap,x];                                    %#ok<*AGROW>
end

combinedMap         =   combinedMap';

%% read input json file
JSONfile            =   resultsFolder(7).name;
openJSON            =   fopen(JSONfile); 
RAW                 =   fread(openJSON,inf);
Strings             =   char(RAW');
fclose(openJSON);

JSONdata            =   struct('inputs',[]);
JSONdata.inputs     =   jsondecode(Strings);

%% read json header files
headerFolder        =   resultsFolder(5).name;
JSONheaders         =   dir(strcat(pwd,'\',data,'\',headerFolder));
JSONnames           =   struct('names',[]);

headerNamesOrder    =   [3,4,6,7,10,12,13,14,15,16];
for i = 1:length(headerNamesOrder)
    headerFile          =   JSONheaders(headerNamesOrder(i)).name;
    openJSON            =   fopen(headerFile);
    RAW                 =   fread(openJSON,inf);
    Strings             =   vertcat(Strings,jsondecode(char(RAW')));
    fclose(openJSON);
end
Strings(1)          =   [];
JSONnames.names     =   Strings;

%% combined data with corresponding header
componentNames      =   matlab.lang.makeValidName(JSONnames.names');
indices             =   size(combinedMap,1);
probedParams        =   cell2struct(mat2cell(1:indices,1,ones(indices,1)),...
                                    componentNames,2);                      %#ok<*MMTC>

paramsNames         =   fieldnames(probedParams);

%% extract operating points
X1  =   eval(JSONdata.inputs.X1);
X2  =   eval(JSONdata.inputs.X2);
X3  =   eval(JSONdata.inputs.X3);
X4  =   eval(JSONdata.inputs.X4);
X5  =   eval(JSONdata.inputs.X5);
X6  =   eval(JSONdata.inputs.X6);
X7  =   eval(JSONdata.inputs.X7);
X8  =   eval(JSONdata.inputs.X8);
X9  =   eval(JSONdata.inputs.X9);
X10 =   eval(JSONdata.inputs.X10);

%% 3D map plot
Constant_1 = 0;
Constant_2 = 35;
Constant_3 = 13.5;

Variable_1 = X3;
Variable_2 = X5;

if ~Constant_1
    Case = 'Typical';
else
    Case = 'Worst-Case';
end

Component = getfield(probedParams,'SRTL');             %#ok<*GFLD>

ij = 0;
x = zeros(1,length(Variable_1*length(Variable_2)));
for i = 1:length(Variable_1)
    for j = 1:length(Variable_2) 
        ij = ij + 1;
        x(ij) = findIndex(Constant_1,Constant_2,Variable_1(i),Constant_3,Variable_2(j),...
            0,0,0,0,0,...
            X1,X2,X3,X4,X5,X6,X7,X8,X9,X10);
        x(ij) = combinedMap(Component,x(ij));
    end
end

[X,Y] = meshgrid(Variable_2,Variable_1);
z = zeros(length(Variable_1),length(Variable_2));
k = 1;
for i = 0:length(x) - 1
    j = mod(i,length(Variable_2)) + 1;
    
    z(k,j) = x(i + 1);
    if (j == length(Variable_2))
        k = k + 1;
    end
end
z = z/8;
figure
h1 = surf(X,Y,z,'FaceAlpha',1.0);
c = colorbar;
% c.Label.String = 'Efficiency [%]';
c.Label.FontSize = 14;
xlabel('Target Load Power [W]', 'FontSize', 14);
ylabel('Input Voltage [V]', 'FontSize', 14);
zlabel(paramsNames{Component}, 'FontSize', 14,'Interpreter','none');

grid on
grid minor
title(strcat(paramsNames{Component}," ",...
      'Map in'," ",Case,' conditions with Respect to Input Voltage & Output Power at'," " ,...
      num2str(Constant_2),"�C ", 'Water Temperature & at'," ",num2str(Constant_3),"V ",'Output.'),'FontSize', 14,'Interpreter','none')

%% export flattened matrix
component_map               =   combinedMap(Component,1:end)*1.4444 + 0*combinedMap(Component+1,1:end);
component_map_reshaped      =   reshape(component_map,[length(X5),length(X4),length(X3),length(X2)]);
component_map_135           =   component_map_reshaped(:,4,:,:);
component_map_135_reshaped  =   reshape(component_map_135,[length(X5),length(X3),length(X2)]);

C                           =   permute(component_map_135_reshaped,[1 3 2]);
component_map_135_flat      =   reshape(C,[],size(component_map_135_reshaped,2),1);

component_map_135_flat_new  =   zeros(size(component_map_135_flat));
for i = 1:size((component_map_135_flat),2)
    component_map_135_flat_new(:,i+1) = component_map_135_flat(:,i);
end

for i = 1:length(component_map_135_flat)/length(X5)
    component_map_135_flat_new((i-1)*length(X5)+1:i*length(X5),1) = X5;
end

writetable(array2table(component_map_135_flat_new),'LuT_3D.csv','WriteVariableNames',0)

