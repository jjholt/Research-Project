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

time = stem{end}(:,1);
time_filtered = time(time < 0.1);
stem_magnitude_filtered = stem_magnitude(time < 0.1);
figure(1); plot(time, stem_magnitude);
figure(2); plot(time_filtered, stem_magnitude_filtered);
% FFT
% names = ["stem" "collar" "spigot"];
% for freq_pos = 23
%     part = [ sqrt(sum(stem{freq_pos}(:,2:4).^2, 2)) sqrt(sum(collar{freq_pos}(:,2:4).^2, 2)) sqrt(sum(spigot{freq_pos}(:,2:4).^2, 2))];
%     for n = 1:size(part,2)
%         L = length(part(:,n));
%         Fs = 2000;
%         T = 1/Fs;
%         time = stem{end}(:,1);
%         
%         P2 = abs(part(:,n)/L);
%         P1 = P2(1:L/2+1);
%         P1(2:end-1) = 2*P1(2:end-1);
%         f = Fs*(0:(L/2))/L;
%         writematrix(horzcat(f', P1), strcat("fft_", names(n),"_", int2str(frequencies(freq_pos)) , "Hz", ".csv"));
%         figure
%         plot(f, P1)
%         xlabel("frequency [Hz]")
%         title(names(n))
%     end
% end
% clear f Fs L P1 P2 T
% 
% figure;
% spectrogram(stem_magnitude, 3, 2, 3, 2000, 'yaxis')
% stem_s = spectrogram(stem_magnitude);
% spigot_s = spectrogram(spigot_magnitude);
% plot(abs(stem_s - spigot_s))

% 
% writematrix(horzcat(time, (spigot_magnitude./spigot_magnitude)), "spigot_900_norm.csv");
% 
% writematrix(horzcat(time, (stem_magnitude./spigot_magnitude)), "stem_900_norm.csv");