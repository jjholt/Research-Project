clc;clear
Fs = 2000;
T = 1/Fs;
L = 1600;
t = (0:L-1)*T;
rando = 2*rand([1 L/2]);
X(1:length(t)/2) = 1.5e-7*(1 + sin(2*pi*900*t(1:length(t)/2)) );
X(length(t)/2+1:length(t)) = 1.5e-7*(1 + rando.*sin(2*pi*500*t(length(t)/2+1:length(t))) );
Y = fft(X);
P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);
f = Fs*(0:(L/2))/L;

figure

subplot(2,2,1)
plot(t, X)
% title([strcat(names(n)," ", "30 Hz") "Time domain"])
xlabel("Time [s]")

subplot(2,2,2)
plot(f, P1)
% title([strcat(names(n)," ", "30 Hz") "Frequency domain"])
xlabel("frequency [Hz]")

subplot(2,2,3)
spectrogram(X, 128, 120, 128, 2000, 'yaxis'); colormap plasma

subplot(2,2,4)
spectrogram(X, [], [], [], 2000); colormap plasma