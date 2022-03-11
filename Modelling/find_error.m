clc;clear;
flanged = readmatrix("Flanged\magnitudes_flanged.csv");
simplified = readmatrix("Frequencies-more-data\magnitudes_simplified.csv");
a = horzcat(simplified(:,1), (simplified(:,2:4) - flanged(:,2:4))./simplified(:,2:4));
figure; hold on;
plot(a(:,1), a(:,4), "DisplayName", "Stem")
plot(a(:,1), a(:,3), "DisplayName", "Collar")
plot(a(:,1), a(:,2), "DisplayName", "Spigot")
legend;
writematrix(a, "error_flanged-simplified.csv")