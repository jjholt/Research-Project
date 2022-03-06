clc;clear;
grouped_data = import_csv();
[spigot, collar, stem] = split_data(grouped_data);

offsets = 1:5:45;
spigot_max_magnitude = zeros(size(offsets));
stem_max_magnitude = zeros(size(offsets));
collar_max_magnitude = zeros(size(offsets));
for n = 1:numel(offsets)

    stem_magnitude = sqrt(sum(stem{n}(:,2:4).^2, 2));
    stem_max_magnitude(n) = max(stem_magnitude);

    spigot_magnitude = sqrt(sum(spigot{n}(:,2:4).^2, 2));
    spigot_max_magnitude(n) = max(spigot_magnitude);

    collar_magnitude = sqrt(sum(collar{n}(:,2:4).^2, 2));
    collar_max_magnitude(n) = max(collar_magnitude);
end

% u_3(u_3 < 1e-11) = 0;
% scatter(frequencies, maxima_u1_u2_u3)
% set(gca, 'yscale', 'log')
% xlabel("Frequency [Hz]"); ylabel("Maximum displacement [m]")
% title("Maximum total displacement")
writematrix(horzcat(offsets', spigot_max_magnitude'), "spigot_maxima.csv");
writematrix(horzcat(offsets', collar_max_magnitude'), "collar_maxima.csv");
writematrix(horzcat(offsets', stem_max_magnitude'), "stem_maxima.csv");