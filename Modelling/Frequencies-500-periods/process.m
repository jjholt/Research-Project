clc;clear;
grouped_data = import_csv();
[spigot, collar, stem] = split_data(grouped_data);

frequencies = [1, 10, 20, 30, 40];
frequencies = [frequencies 50:50:900];
spigot_max_magnitude = zeros(size(frequencies));
stem_max_magnitude = zeros(size(frequencies));
collar_max_magnitude = zeros(size(frequencies));
tail_end = 0.10:0.05:0.95;
for num_tails = 1:numel(tail_end)
    for freq = 1:numel(frequencies)
        beginning = tail_end(num_tails)*numel(stem{freq}(:,1)); %tail-end 64% of all values
    
        stem_magnitude = sqrt(sum(stem{freq}(beginning:end,2:4).^2, 2));
        stem_max_magnitude(freq,num_tails) = max(stem_magnitude);
        
    
        spigot_magnitude = sqrt(sum(spigot{freq}(beginning:end,2:4).^2, 2));
        spigot_max_magnitude(freq,num_tails) = max(spigot_magnitude);
        
    
        collar_magnitude = sqrt(sum(collar{freq}(beginning:end,2:4).^2, 2));
        collar_max_magnitude(freq,num_tails) = max(collar_magnitude);
        
    end
end
stem_max_magnitude = stem_max_magnitude(:,1:length(tail_end));
spigot_max_magnitude = spigot_max_magnitude(:,1:length(tail_end));
collar_max_magnitude = collar_max_magnitude(:,1:length(tail_end));
save("maxima-and-tail", "collar_max_magnitude", "spigot_max_magnitude", "stem_max_magnitude", "tail_end", "frequencies");

% writematrix(horzcat(frequencies', spigot_max_magnitude', collar_max_magnitude', stem_max_magnitude'), "magnitudes_simplified.csv")
% 
% writematrix(horzcat(frequencies', spigot_max_magnitude'), "spigot_maxima.csv");
% writematrix(horzcat(frequencies', stem_max_magnitude'), "stem_maxima.csv");
% writematrix(horzcat(frequencies', collar_max_magnitude'), "collar_maxima.csv");
% 
% % Change relative to spigot
% 
% writematrix(horzcat(frequencies', (stem_max_magnitude./spigot_max_magnitude)'), "stem_maxima_normalised.csv");
% writematrix(horzcat(frequencies', (collar_max_magnitude./spigot_max_magnitude)'), "collar_maxima_normalised.csv");
% writematrix(horzcat(frequencies', (spigot_max_magnitude./spigot_max_magnitude)'), "spigot_maxima_normalised.csv");

% time = stem{end}(beginning:end,1);
% figure; plot(time, stem{end}(beginning:end,3));

% FFT

% names = ["stem" "collar" "spigot"];
% for freq_pos = 1:23
%     part = [ sqrt(sum(stem{freq_pos}(:,2:4).^2, 2)) sqrt(sum(collar{freq_pos}(:,2:4).^2, 2)) sqrt(sum(spigot{freq_pos}(:,2:4).^2, 2))];
%     figure;
%     for n = 1:size(part,2)
%         L = length(part(:,n));
%         Fs = 2000;
%         T = 1/Fs;
%         time = stem{end}(:,1);
%         
%         P2 = abs(fft(part(:,n))/L);
%         P1 = P2(1:L/2+1);
%         P1(2:end-1) = 2*P1(2:end-1);
%         f = Fs*(0:(L/2))/L;
% %         writematrix(horzcat(f', P1), strcat("fft_", names(n),"_", int2str(frequencies(freq_pos)) , "Hz", ".csv"));
%         subplot(3, 1, n); hold on;
%         plot(f, P1, "DisplayName", strcat(int2str(frequencies(freq_pos)), " Hz"));
%         xlabel("frequency [Hz]");
%         title(names(n));
%         legend;
%     end
% end

% clear f Fs L P1 P2 T
% 
% figure;
% spectrogram(stem_magnitude, [], [], [], 2000, 'yaxis'); colormap plasma
% stem_s = spectrogram(stem_magnitude);
% spigot_s = spectrogram(spigot_magnitude);

% plot(abs(stem_s - spigot_s))

% 
% writematrix(horzcat(time, (spigot_magnitude./spigot_magnitude)), "spigot_900_norm.csv");
% 
% writematrix(horzcat(time, (stem_magnitude./spigot_magnitude)), "stem_900_norm.csv");