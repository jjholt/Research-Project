clc;clear;
flanged = readmatrix("Flanged\magnitudes_flanged.csv");
simplified = readmatrix("Frequencies\magnitudes_simplified.csv");
a = horzcat(simplified(:,1), (simplified(:,2:4) - flanged(:,2:4))./simplified(:,2:4));
writematrix(a, "error_flanged-simplified.csv")