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