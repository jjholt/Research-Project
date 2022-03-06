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

writematrix(horzcat(frequencies', spigot_max_magnitude'), "spigot_maxima.csv");
writematrix(horzcat(frequencies', stem_max_magnitude'), "stem_maxima.csv");
writematrix(horzcat(frequencies', collar_max_magnitude'), "collar_maxima.csv");

% Change relative to spigot
writematrix(horzcat(frequencies', (stem_max_magnitude - spigot_max_magnitude)'), "stem_maxima_diff.csv");
writematrix(horzcat(frequencies', (collar_max_magnitude - spigot_max_magnitude)'), "collar_maxima_diff.csv");

writematrix(horzcat(frequencies', ((stem_max_magnitude - spigot_max_magnitude)./spigot_max_magnitude)'), "stem_maxima_normalised_diff.csv");
writematrix(horzcat(frequencies', ((collar_max_magnitude - spigot_max_magnitude)./spigot_max_magnitude)'), "collar_maxima_normalised_diff.csv");

writematrix(horzcat(frequencies', (stem_max_magnitude./spigot_max_magnitude)'), "stem_maxima_normalised.csv");
writematrix(horzcat(frequencies', (collar_max_magnitude./spigot_max_magnitude)'), "collar_maxima_normalised.csv");



% FFT
names = ["stem" "collar" "spigot"];
for freq_pos = 23 %1 to 23
%     part = [ sqrt(sum(stem{freq_pos}(:,4).^2, 2)) sqrt(sum(collar{freq_pos}(:,4).^2, 2)) sqrt(sum(spigot{freq_pos}(:,4).^2, 2))];
    part = [stem{freq_pos}(:,4) collar{freq_pos}(:,4) spigot{freq_pos}(:,4)];
    times = [stem{freq_pos}(:,1) collar{freq_pos}(:,1) spigot{freq_pos}(:,1)];
    for n = 1:size(part,2)
        Fs = 2000;
        t = times(:,n);
        L = length(t);
        X = part(:,n);
        Y = fft(X);
        P2 = abs(Y/L);
        P1 = P2(1:L/2+1);
        P1(2:end-1) = 2*P1(2:end-1);
        f = Fs*(0:(L/2))/L;

        writematrix(horzcat(f', P1), strcat("fft_", names(n),"_", int2str(frequencies(freq_pos)) , "Hz", ".csv"));
        
        figure(1); 
        subplot(2,1,1); hold on;
        plot(t, X, "DisplayName", names(n))
        title([strcat(int2str(frequencies(freq_pos)), "Hz") "Time domain"])
        xlabel("Time [s]")

        subplot(2,1,2); hold on;
        plot(f, P1, "DisplayName", names(n))
        title([strcat(int2str(frequencies(freq_pos)), "Hz") "Frequency domain"])
        xlabel("frequency [Hz]")
    end
    legend;
end
% clear f Fs L P1 P2 T y n 

figure(2);
spectrogram(X, [], [], [], 2000, 'yaxis')
colormap plasma