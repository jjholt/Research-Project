clc;clear;
grouped_data = import_csv();
[base, collar, stem] = split_data(grouped_data);

offsets = 1:5:45;
base_max_magnitude = zeros(size(offsets));
stem_max_magnitude = zeros(size(offsets));
for n = 1:numel(offsets)

    stem_magnitude = sqrt(sum(stem{n}(:,2:4).^2, 2));
    stem_max_magnitude(n) = max(stem_magnitude);

    base_magnitude = sqrt(sum(base{n}(:,2:4).^2, 2));
    base_max_magnitude(n) = max(base_magnitude);
end

% u_3(u_3 < 1e-11) = 0;
% scatter(frequencies, maxima_u1_u2_u3)
% set(gca, 'yscale', 'log')
% xlabel("Frequency [Hz]"); ylabel("Maximum displacement [m]")
% title("Maximum total displacement")
writematrix(horzcat(offsets', base_max_magnitude'), "base_maxima.csv");
writematrix(horzcat(offsets', stem_max_magnitude'), "stem_maxima.csv");