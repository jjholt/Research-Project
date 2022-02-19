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
clear all_three_of_same_freq one_frequency i j

frequencies = [1, 10, 20, 30, 40];
frequencies = [frequencies 50:50:900];
maxima_u1 = zeros(1,length(frequencies));
maxima_u2 = zeros(1,length(frequencies));
maxima_u3 = zeros(1,length(frequencies));
maxima_u1_u2_u3 = zeros(1,length(frequencies));
u_3 = [];
for i = 1:numel(collected_data)
    datum = collected_data{i};                          %Everything up to here is to undo the choices in python. Produce just one .csv instead, dumdum
    magnitude = sqrt(sum(datum(:, 2:4).^2, 2));
    maxima_u1_u2_u3(i) = max(magnitude);
    maxima_u1(i) = max(abs(datum(:,2)));
    maxima_u2(i) = max(abs(datum(:,3)));
    maxima_u3(i) = max(abs(datum(:,4)));
    if frequencies(i) == 100
        u_3 = horzcat(datum(:,1), datum(:,4));
    end
end
u_3(u_3 < 1e-11) = 0;
scatter(frequencies, maxima_u1_u2_u3)
set(gca, 'yscale', 'log')
xlabel("Frequency [Hz]"); ylabel("Maximum displacement [m]")
title("Maximum total displacement")
writematrix(horzcat(frequencies', maxima_u1_u2_u3'), "maxima_u1_u2_u3.csv");
writematrix(horzcat(frequencies', maxima_u1'), "maxima_u1.csv");
writematrix(horzcat(frequencies', maxima_u2'), "maxima_u2.csv");
writematrix(horzcat(frequencies', maxima_u3'), "maxima_u3.csv");
writematrix(u_3, "u3.csv");