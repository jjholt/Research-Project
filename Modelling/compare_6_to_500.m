clc;clear;
low = load("Frequencies/maxima-and-tail.mat");
high = load("Frequencies-500-periods/maxima-and-tail.mat");

err_collar = zeros(size(high.stem_max_magnitude));
err_spigot = zeros(size(high.stem_max_magnitude));
err_stem = zeros(size(high.stem_max_magnitude));

for i = 1:length(high.tail_end)
    err_collar(:, i) = high.collar_max_magnitude(:,end)./high.collar_max_magnitude(:,i);
    err_spigot(:, i) = high.spigot_max_magnitude(:,end)./high.spigot_max_magnitude(:,i);
    err_stem(:, i)   = high.stem_max_magnitude(:,end)./high.stem_max_magnitude(:,i);
end

% Absolute error by frequency
for freq = 1:length(high.frequencies)
    writematrix(horzcat(high.tail_end', (err_collar(freq,:) - err_collar(freq,end))'), strcat("Error/collar-", num2str(high.frequencies(freq)), ".csv"));
    writematrix(horzcat(high.tail_end', (err_spigot(freq,:) - err_spigot(freq,end))'), strcat("Error/spigot-", num2str(high.frequencies(freq)), ".csv"));
    writematrix(horzcat(high.tail_end', (err_stem(freq,:) - err_stem(freq,end))'), strcat("Error/stem-", num2str(high.frequencies(freq)), ".csv"));
end
