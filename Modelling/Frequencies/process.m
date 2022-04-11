clc;clear;
grouped_data = import_csv();
[spigot, collar, stem] = split_data(grouped_data);

frequencies = [1, 10, 20, 30, 40];
frequencies = [frequencies 50:50:900];
spigot_max_magnitude = zeros(size(frequencies));
stem_max_magnitude = zeros(size(frequencies));
collar_max_magnitude = zeros(size(frequencies));
for n = 1:numel(frequencies)

    stem_magnitude = sqrt(sum(stem{n}(:,2:4).^2, 2));
    stem_max_magnitude(n) = max(stem_magnitude);

    spigot_magnitude = sqrt(sum(spigot{n}(:,2:4).^2, 2));
    spigot_max_magnitude(n) = max(spigot_magnitude);

    collar_magnitude = sqrt(sum(collar{n}(:,2:4).^2, 2));
    collar_max_magnitude(n) = max(collar_magnitude);
end

writematrix(horzcat(frequencies', spigot_max_magnitude', collar_max_magnitude', stem_max_magnitude'), "magnitudes_simplified.csv")

writematrix(horzcat(frequencies', spigot_max_magnitude'), "spigot_maxima.csv");
writematrix(horzcat(frequencies', stem_max_magnitude'), "stem_maxima.csv");
writematrix(horzcat(frequencies', collar_max_magnitude'), "collar_maxima.csv");

% Change relative to spigot

writematrix(horzcat(frequencies', (stem_max_magnitude./spigot_max_magnitude)'), "stem_maxima_normalised.csv");
writematrix(horzcat(frequencies', (collar_max_magnitude./spigot_max_magnitude)'), "collar_maxima_normalised.csv");
writematrix(horzcat(frequencies', (spigot_max_magnitude./spigot_max_magnitude)'), "spigot_maxima_normalised.csv");

save("maxima-and-tail", "collar_max_magnitude", "spigot_max_magnitude", "stem_max_magnitude");