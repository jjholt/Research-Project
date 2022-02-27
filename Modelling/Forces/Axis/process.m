clc;clear;
grouped_data = import_csv();
nodes = {};
[nodes{1}, nodes{2}, nodes{3}] = split_data(grouped_data);
names = ["base", "collar", "stem"];
t = nodes{1}{1}(:,1);
% frequencies = [1, 10, 20, 30, 40];
% frequencies = [frequencies 50:50:900];
% base_max_magnitude = zeros(size(frequencies));
% stem_max_magnitude = zeros(size(frequencies));
% rms_stem = zeros(size(frequencies));
% rms_base = zeros(size(frequencies));

% max_magnitude = zeros(size(amplitudes,1),numel(nodes));
for i = 1:numel(nodes)
%     max_magnitude = [];
%     for n = 1:numel(amplitudes)
%         magnitude = sqrt(sum(nodes{i}{n}(:,2:4).^2, 2));
%         max_magnitude(n) = max(magnitude);%     end
%     writematrix(horzcat(amplitudes', max_magnitude'), names(i)+".csv")
end
