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

    collar_magnitude = sqrt(sum(collar{n}(:,2:4).^2, 2));
    collar_max_magnitude(n) = max(collar_magnitude);

    spigot_magnitude = sqrt(sum(spigot{n}(:,2:4).^2, 2));
    spigot_max_magnitude(n) = max(spigot_magnitude);
end
writematrix(horzcat(frequencies', ((stem_max_magnitude - spigot_max_magnitude)./spigot_max_magnitude)'), "stem_maxima_normalised_diff.csv");
writematrix(horzcat(frequencies', ((collar_max_magnitude - spigot_max_magnitude)./spigot_max_magnitude)'), "collar_maxima_normalised_diff.csv");
% u_3(u_3 < 1e-11) = 0;
% scatter(frequencies, maxima_u1_u2_u3)
% set(gca, 'yscale', 'log')
% xlabel("Frequency [Hz]"); ylabel("Maximum displacement [m]")
% title("Maximum total displacement")
writematrix(horzcat(frequencies', spigot_max_magnitude'), "spigot_maxima.csv");
writematrix(horzcat(frequencies', stem_max_magnitude'), "stem_maxima.csv");
writematrix(horzcat(frequencies', collar_max_magnitude'), "collar_maxima.csv");

names = ["stem" "collar" "spigot"];
for freq_pos = 23
    part = [ sqrt(sum(stem{freq_pos}(:,2:4).^2, 2)) sqrt(sum(collar{freq_pos}(:,2:4).^2, 2)) sqrt(sum(spigot{freq_pos}(:,2:4).^2, 2))];
    for n = 1:size(part,2)
        L = length(part(:,n));
        Fs = 2000;
        T = 1/Fs;
        time = stem{end}(:,1);
        
        P2 = abs(part(:,n)/L);
        P1 = P2(1:L/2+1);
        P1(2:end-1) = 2*P1(2:end-1);
        f = Fs*(0:(L/2))/L;
%         writematrix(horzcat(f', P1), strcat("fft_", names(n),"_", int2str(frequencies(freq_pos)) , "Hz", ".csv"));
        figure
        plot(f, P1)
        title(names(n))
    end
end