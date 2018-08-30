%----------------------------------clear----------------------------------%
clear variables
close all
clc
%------------------------------importdata---------------------------------%
A = importdata('rcvr.dat');
B = importdata('eph.dat');
%------------------------------Sorting order------------------------------%
C = zeros(size(A));
D = zeros(size(B));
count = 1;
for s = 1:11
    for t = 1:11
        if A(s,2)==B(t,2)
            C(count,:) = A(s,:);
            D(count,:) = B(t,:);
            count = count+1;
            break
        end
    end
end
%------------------------------define parameters--------------------------%
[r_1,c_1] = size(C);
[r_2,c_2] = size(D);

rcvr_tow_1 = C(:,1);
svid_1 = C(:,2);
pr = C(:,3);
carr_phas = C(:,4);
dop_fre = C(:,5);
snr_dbhz = C(:,6);

rcvr_tow_2 = D(:,1);
svid_2 = D(:,2);
toc = D(:,3);
toe = D(:,4);
af0 = D(:,5);
af1 = D(:,6);
af2 = D(:,7);
ura = D(:,8);
e = D(:,9);
sqrtA = D(:,10);
dn = D(:,11);
m0 = D(:,12);
w = D(:,13);
omg0 = D(:,14);
i0 = D(:,15);
odot = D(:,16);
idot = D(:,17);
cus = D(:,18);
cuc = D(:,19);
cis = D(:,20);
cic = D(:,21);
crs = D(:,22);
crc = D(:,23);
iod = D(:,24);
%----------------------------some constants-------------------------------%
Mu = 3.986005e14;                   %----(m^3/s^2)----%
odote =  7.2921151467e-5;           %----(r/s)----%
c = 299792458;                      %----(m/s)----%
F = -4.442807633e-10;               %----(s)----%
%----------------------------find sv xk yk zk-----------------------------%
A = sqrtA .^ 2;
n0 = (Mu ./ A .^ 3) .^(1/2);
t = rcvr_tow_1 - pr / c;
tk = t - toe;
n = n0 + dn;

mk = m0 + n .* tk;
Ek = mk;
Epre = 0;
for s=1:11
    while abs(Ek(s) - Epre) >= 1e-12
        Epre = Ek(s);
        Ek(s) = mk(s) + e(s) * sin(Ek(s));
    end
    Epre = 0;
end
Ek;
Vk = atan2( (sqrt(1 - e.^2) .* sin(Ek)) , (cos(Ek) - e));
phi_k = Vk + w;

duk = cus .* sin(2*phi_k) + cuc .* cos(2*phi_k);
dik = cis .* sin(2*phi_k) + cic .* cos(2*phi_k);
drk = crs .* sin(2*phi_k) + crc .* cos(2*phi_k);

uk = phi_k + duk;
ik = i0 + dik + idot .* tk;
rk = A .* (1 - e .* cos(Ek)) + drk;

xkPr = rk .* cos(uk);
ykPr = rk .* sin(uk);
omgk = omg0 + (odot - odote) .*tk - odote .* toe;

xk = xkPr .* cos(omgk) - ykPr .* cos(ik) .* sin(omgk);
yk = xkPr .* sin(omgk) + ykPr .* cos(ik) .* cos(omgk);
zk = ykPr .* sin(ik);

scatter3(xk,yk,zk,'*'); text(xk, yk, zk, num2str(svid_1));
hold on
scatter3(0,0,0); text(0,0,0, 'origin');
hold on
scatter3(-2950000,5070000,2470000); text(-2950000,5070000,2470000, 'u_i');
hold on
%%---------------------------find user xk yk zk--------------------------%%
%----------------------------find guess Rho-------------------------------%
dtr = F * e .^ sqrtA .* sin(Ek); 
dtsv = af0 + af1 .* (t - toc) +af2 .* (t - toc) .^ 2 + dtr;
Rho = pr + c * dtsv;
G_Pos = [-2950000 5070000 2470000 0]';
Del_Pos = ones(r_1,1);
while abs(Del_Pos(1)) >= 1e-4
    G_Rho = sqrt((G_Pos(1)*ones(r_1,1) - xk).^2+(G_Pos(2)*ones(r_1,1) - yk).^2+(G_Pos(3)*ones(r_1,1) - zk).^2);
    %----------------------------create H-------------------------------------%
    e1 = zeros(r_1,4); e2 = zeros(r_1,4); e3 = zeros(r_1,4); e4 = zeros(r_1,4);
    e1(:,1) = (G_Pos(1)*ones(r_1,1) - xk)./ G_Rho;
    e2(:,2) = (G_Pos(2)*ones(r_1,1) - yk)./ G_Rho;
    e3(:,3) = (G_Pos(3)*ones(r_1,1) - zk)./ G_Rho;
    e4(:,4) = 1;
    H = e1 + e2 + e3 + e4;
    %----------------------------find user xk yk zk---------------------------%
    Del_Rho = Rho - G_Rho;
    Del_Pos = pinv(H) * Del_Rho;
    G_Pos = G_Pos + Del_Pos;
    hold on
end
scatter3(G_Pos(1),G_Pos(2),G_Pos(3)); text(G_Pos(1),G_Pos(2),G_Pos(3), 'u_f');
xk
yk
zk
dtsv
Del_Pos
G_Pos

