clear all;

% remember to change the file path into the path in your computer
filePath_nav = 'D:\github\python_code\現代衛星導航作業\HW05\SkyTraq receiver guide\RINEX-reader\New_GPS_day2_out.nav';
filePath_obs = 'D:\github\python_code\現代衛星導航作業\HW05\SkyTraq receiver guide\RINEX-reader\New_GPS_day2_out.obs';

[XYZ_station,obs,observablesHeader,measurementsInterval]=readRinex302(filePath_obs);
[outputEphemeris] = readRinexNav(filePath_nav);

% save observation data(obs) in to rcvr.dat
fid1 = fopen('rcvr_New_GPS_day2_out.dat', 'w+');
[m,n]=size(obs);
for i=1:1:m
    for j=1:1:n
        if j==n
            fprintf(fid1, '%.15d \n', obs(i,j) );
        else
            fprintf(fid1, '%.15d \t', obs(i,j) );
        end
    end
end
fclose(fid1);

% save ephemeris data(outputEphemeris) in to eph.dat
fid2 = fopen('eph_New_GPS_day2_out.dat', 'w+');
[m,n]=size(outputEphemeris.gpsEphemeris);
for i=1:1:m
    for j=1:1:n
        if j==n
            fprintf(fid2, '%.15d \n', outputEphemeris.gpsEphemeris(i,j) );
        else
            fprintf(fid2, '%.15d \t', outputEphemeris.gpsEphemeris(i,j) );
        end
    end
end
fclose(fid2);