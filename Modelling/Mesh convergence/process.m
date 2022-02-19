clc;clear;
dd = dir("csv/*.csv");
file_names = {dd.name};
data = cell(numel(file_names),2);
data(:,1) = regexprep(file_names, '.csv','');

for i = 1:numel(file_names)
    data{i,2} = readmatrix("csv/" + file_names{i});
end
clear dd file_names i 
collected_data = {};
for i = 1:3:size(data,1)
    particular_frequency = [];
    for j = 0:2
        one_frequency = data(i+j,:);
        all_three_of_same_freq = one_frequency{2};
        if j == 0 % Add the time column if it's the first of that group
            particular_frequency(:,1) = all_three_of_same_freq(:,1);
        end
        particular_frequency = horzcat(particular_frequency, all_three_of_same_freq(:,2));
    end
    collected_data{end+1} = particular_frequency;
end
clear all_three_of_same_freq one_frequency particular_frequency i j

mesh_sizes = [0.01 0.005 0.0025 0.00125].*1e3;
maxima = zeros(size(mesh_sizes));
for i = 1:numel(collected_data)
    datum = collected_data{i};
    magnitude = sqrt(sum(datum(:, 2:4).^2, 2)).*1e9;
    maxima(i) = max(magnitude);
end
scatter(mesh_sizes, maxima)
xlabel("Mesh sizes [mm]"); ylabel("Maximum displacement [nm]")
title("Maximum total displacement")
writematrix(horzcat(mesh_sizes', maxima'), "mesh_size.csv");