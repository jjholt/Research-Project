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

stem_abs_diff = max(high.stem_max_magnitude,[], 2) - min(high.stem_max_magnitude,[], 2);
spigot_abs_diff = max(high.spigot_max_magnitude,[], 2) - min(high.spigot_max_magnitude,[], 2);
collar_abs_diff = max(high.collar_max_magnitude,[], 2) - min(high.collar_max_magnitude,[], 2);
writematrix(horzcat(high.frequencies', stem_abs_diff), "Error/stem_abs_diff.csv")
writematrix(horzcat(high.frequencies', spigot_abs_diff), "Error/spigot_abs_diff.csv")
writematrix(horzcat(high.frequencies', collar_abs_diff), "Error/collar_abs_diff.csv")



stem_rel_diff = (max(high.stem_max_magnitude,[], 2) - min(high.stem_max_magnitude,[], 2))./max(high.stem_max_magnitude,[], 2);
spigot_rel_diff = (max(high.spigot_max_magnitude,[], 2) - min(high.spigot_max_magnitude,[], 2))./max(high.spigot_max_magnitude,[], 2);
collar_rel_diff = (max(high.collar_max_magnitude,[], 2) - min(high.collar_max_magnitude,[], 2))./max(high.collar_max_magnitude,[], 2);
writematrix(horzcat(high.frequencies', stem_rel_diff), "Error/stem_rel_diff.csv")
writematrix(horzcat(high.frequencies', spigot_rel_diff), "Error/spigot_rel_diff.csv")
writematrix(horzcat(high.frequencies', collar_rel_diff), "Error/collar_rel_diff.csv")

% diff_diff = max(high.stem_max_magnitude,[], 2) - low.stem_max_magnitude';

% for freq = 1:length(high.frequencies)
%     writematrix(horzcat(high.tail_end', err_collar(freq, :)'), strcat("Error/collar-", int2str(high.frequencies(freq)), "Hz.csv"));
%     writematrix(horzcat(high.tail_end', err_spigot(freq, :)'), strcat("Error/spigot-", int2str(high.frequencies(freq)), "Hz.csv"));
%     writematrix(horzcat(high.tail_end', err_stem(freq, :)'), strcat("Error/stem-", int2str(high.frequencies(freq)), "Hz.csv"))
% end


% figure; hold on;
% for freq = 1:4:length(high.frequencies)
%     plot( ...
%         high.tail_end*100, err_collar(freq,:) ...
%         , DisplayName=strcat( int2str(high.frequencies(freq)), " Hz"  )...
%     );
% end
% set(gca, "Xdir", "reverse")
% legend;
% xlabel("Percentage of tail-end")
% ylabel("Relative error")
