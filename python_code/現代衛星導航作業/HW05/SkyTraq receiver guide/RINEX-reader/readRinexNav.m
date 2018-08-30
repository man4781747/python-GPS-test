function [ outputEphemeris] = readRinexNav( filePath )
%readRinexNav Reads a mixed RINEX navigation file *.nav and returns the
%loaded ephemeris for each constellation
%   Reads Keplerian and Cartesian type ephemeris coming from RINEX 3.02
%   Files can be downlaoded from here: ftp://cddis.gsfc.nasa.gov/gnss/data/campaign/mgex/daily/rinex3/2015/
%   Download in *.p format and convert to .nav using rtklib

%%%%%-------Input
%       fileName = File adress

%%%%%------- Output
%       outputEphemeris = Class containing the ephemeris for each
%       constellation


'Loading ephemeris...'
endOfHeader = 0;

navFile = fopen(filePath);

%Read header
while (~endOfHeader)
    line = fgetl(navFile);
    lineSplit = strsplit(line);
    
    if strfind(line,'RINEX VERSION')
        Version = lineSplit(2);
        if ~strcmp(Version,'3.02')
            error 'Not the correct version, should be 3.02'
        end
        
        
    elseif strfind(line,'DATE')
        date = lineSplit(6);
        year = str2double(date{1,1}(1:4));
        month = str2double(date{1,1}(5:6));
        day = str2double(date{1,1}(7:8));
        %         DOY=Date2DayOfYear(real(year),real(month),real(day));
    elseif strfind(line,'IONOSPHERIC CORR')
        if strcmp(lineSplit(1), 'GPSA')
            ionoAlpha = str2double(lineSplit(2:5));
        elseif strcmp(lineSplit(1), 'GPSB')
            ionoBeta = str2double(lineSplit(2:5));
        end
    elseif strfind (line,'LEAP SECONDS')
        leapSeconds = str2double(lineSplit(2));
    elseif strfind(line,'END OF HEADER')
        endOfHeader = 1;
    end
end

%Pointer line set at the end of the header.
ionosphericParameters = [ionoAlpha; ionoBeta];


%read body

gpsEphemeris =  [];
glonassEphemeris = [];
beidouEphemeris = [];

keplerArray = zeros(22,1); %Vector containing Keplerian elements type ephemeris (GPS, Beidou, Galileo)
cartesianArray = zeros(19,1); %Vector containing Cartesian type ephemeris (GLONASS, SBAS)
while ~feof(navFile)
    line = fgetl(navFile);
    %     lineSplit = strsplit(line);
    
    constellation = line(1);
    if ischar(constellation) %New Ephemeris
        switch constellation
            case {'G', 'C'}                %If the ephemeris is ether for GPS or Beidou, store Keplerian elements
                
                %%Read All of the ephemeris
                svprn = str2double([line(2), line(3)]);
                time = [str2double(line(5:8)), str2double(line(10:11)), str2double(line(13:14)), str2double(line(16:17)), str2double(line(19:20)), str2double(line(22:23))]; %time = [year, month, day, hour, min, sec]
                time=real(time);
                [gpsTime,fctSeconds] = Utc2Gps(time);
                tow = gpsTime(2);
%                 [tow,gpsWeek]=Date2GPSTime(time(1),time(2),time(3),time(4)+time(5)/60+time(6)/3600); %Transform date to seconds of week
                
                af0 = str2double(line(24:42)); %Read from end because of 1 digit prn
                af1 = str2double(line(43:61));
                af2 = str2double(line(62:80));
                
                %                 lineSplit = strsplit(fgetl(navFile));   %
                lineNext = fgetl(navFile);
                IODE = str2double(lineNext(5:23));
                crs = str2double(lineNext(24:42));
                deltan = str2double(lineNext(43:61));
                M0 = str2double(lineNext(62:80));
                
                %                 lineSplit = strsplit(fgetl(navFile));	  %
                lineNext = fgetl(navFile);
                cuc = str2double(lineNext(5:23));
                ecc = str2double(lineNext(24:42));
                cus = str2double(lineNext(43:61));
                roota = str2double(lineNext(62:80));
                
                %                 lineSplit = strsplit(fgetl(navFile));
                lineNext = fgetl(navFile);
                toe = str2double(lineNext(5:23));
                cic = str2double(lineNext(24:42));
                Omega0 = str2double(lineNext(43:61));
                cis = str2double(lineNext(62:80));
                
                %                 lineSplit = strsplit(fgetl(navFile));	    %
                lineNext = fgetl(navFile);
                i0 =  str2double(lineNext(5:23));
                crc = str2double(lineNext(24:42));
                omega = str2double(lineNext(43:61));
                Omegadot = str2double(lineNext(62:80));
                
                %                 lineSplit = strsplit(fgetl(navFile));	    %
                lineNext = fgetl(navFile);
                idot = str2double(lineNext(5:23));
                CodesOnL2 = str2double(lineNext(24:42));
                week_toe = str2double(lineNext(43:61));
                L2Pflag = str2double(lineNext(62:80));
                
                %                 lineSplit = strsplit(fgetl(navFile));	    %
                lineNext = fgetl(navFile);
                SVaccuracy = str2double(lineNext(5:23));   %% unused
                SVhealth = str2double(lineNext(24:42));
                tgd = str2double(lineNext(43:61));
                IODC = str2double(lineNext(62:80));
                
                %                 lineSplit = strsplit(fgetl(navFile));
                lineNext = fgetl(navFile);
                transmissionTime = str2double(lineNext(5:23));
                fitInterval = str2double(lineNext(24:42));
                
                %Conversion to the format required by function
                %sat_coordinates_XYZ
                %                 keplerArray(1)  = svprn;
                %                 keplerArray(2)  = af2;
                %                 keplerArray(3)  = M0;
                %                 keplerArray(4)  = roota;
                %                 keplerArray(5)  = deltan;
                %                 keplerArray(6)  = ecc;
                %                 keplerArray(7)  = omega;
                %                 keplerArray(8)  = cuc;
                %                 keplerArray(9)  = cus;
                %                 keplerArray(10) = crc;
                %                 keplerArray(11) = crs;
                %                 keplerArray(12) = i0;
                %                 keplerArray(13) = idot;
                %                 keplerArray(14) = cic;
                %                 keplerArray(15) = cis;
                %                 keplerArray(16) = Omega0;
                %                 keplerArray(17) = Omegadot;
                %                 keplerArray(18) = toe;
                %                 keplerArray(19) = af0;
                %                 keplerArray(20) = af1;
                %                 keplerArray(21) = toe;
                %                 keplerArray(22) = tgd;
                %                 keplerArray(23) = SVaccuracy;
                %                 keplerArray(24) = IODE;
                %                 keplerArray(25) = tow;
                keplerArray(1) = tow;
                keplerArray(2)  = svprn;
                keplerArray(3) = tow;  %%%%%% toe = toc
                keplerArray(4) = toe;
                keplerArray(5) = af0;
                keplerArray(6) = af1;
                keplerArray(7)  = af2;
                keplerArray(8) = SVaccuracy;
                keplerArray(9)  = ecc;                
                keplerArray(10)  = roota;
                keplerArray(11)  = deltan;
                keplerArray(12)  = M0;
                keplerArray(13)  = omega;
                keplerArray(14) = Omega0;
                keplerArray(15) = i0;
                keplerArray(16) = Omegadot;
                keplerArray(17) = idot;
                keplerArray(18)  = cus;
                keplerArray(19)  = cuc;
                keplerArray(20) = cis;
                keplerArray(21) = cic;
                keplerArray(22) = crs;
                keplerArray(23) = crc;
                keplerArray(24) = IODE;
                
                if constellation == 'G'
                    gpsEphemeris =  [gpsEphemeris; keplerArray'];
                elseif constellation == 'C'
                    beidouEphemeris =  [beidouEphemeris keplerArray];
                else
                    error 'Unknown constellation'
                    %Should never reach this point, as there is a case
                    %above.
                end
                
                %             case 'R' %Also SBAS case
                %                 slot_sv=str2double(line(2:3));
                %                 %Time of Emision
                %                 ToE(1)=str2double(lineSplit(end-8)); %Star from the end to avoid problems with 1 digit prn
                %                 ToE(2)=str2double(lineSplit(end-7));
                %                 ToE(3)=str2double(lineSplit(end-6));
                %                 ToE(4)=str2double(lineSplit(end-5));
                %                 ToE(5)=str2double(lineSplit(end-4));
                %                 ToE(6)=str2double(lineSplit(end-3));
                %                 ToE = real(ToE);
                %                 [toe,week]=Date2GPSTime(ToE(1),ToE(2),ToE(3),ToE(4)+ToE(5)/60+ToE(6)/3600);
                %                 sv_clock_bias=str2double(lineSplit(end-2));
                %                 sv_rel_freq_bias=str2double(lineSplit(end-1));
                %                 m_f_t=str2double(lineSplit(end));
                %
                %                 lineSplit = strsplit(fgetl(navFile));%%%
                %                 X=str2double(lineSplit(2));
                %                 Xdot=str2double(lineSplit(3));
                %                 Xacc=str2double(lineSplit(4));
                %                 health=str2double(lineSplit(5));
                %
                %                 lineSplit = strsplit(fgetl(navFile));%%%
                %                 Y=str2double(lineSplit(2));
                %                 Ydot=str2double(lineSplit(3));
                %                 Yacc=str2double(lineSplit(4));
                %                 freq_num=str2double(lineSplit(5));
                %
                %                 lineSplit = strsplit(fgetl(navFile));%%%
                %                 Z=str2double(lineSplit(2));
                %                 Zdot=str2double(lineSplit(3));
                %                 Zacc=str2double(lineSplit(4));
                %                 age_oper_info=str2double(lineSplit(5));
                %
                %                 cartesianArray(1)=slot_sv;
                %                 cartesianArray(2)=toe;
                %                 cartesianArray(3)=sv_clock_bias;
                %                 cartesianArray(4)=sv_rel_freq_bias;
                %                 cartesianArray(5)=m_f_t;
                %                 cartesianArray(6)=X;
                %                 cartesianArray(7)=Xdot;
                %                 cartesianArray(8)=Xacc;
                %                 cartesianArray(9)=health;
                %                 cartesianArray(10)=Y;
                %                 cartesianArray(11)=Ydot;
                %                 cartesianArray(12)=Yacc;
                %                 cartesianArray(13)=freq_num;
                %                 cartesianArray(14)=Z;
                %                 cartesianArray(15)=Zdot;
                %                 cartesianArray(16)=Zacc;
                %                 cartesianArray(17)=age_oper_info;
                %                 cartesianArray(18)=1;
                %                 cartesianArray(19)=week;
                %
                %                 if constellation == 'R'
                %                     glonassEphemeris = [glonassEphemeris, cartesianArray];
                %                 elseif constellation == 'S'
                %
                %
                %                 end
                %
                %             otherwise
                %                 %error 'Unknown constellation'
                %
                %
        end
        
    else
        error ('Wrong counting. New ephemeris expected.')
    end
    
end

% Construct output
outputEphemeris.glonassEphemeris        = glonassEphemeris;
outputEphemeris.gpsEphemeris            = gpsEphemeris;
outputEphemeris.beidouEphemeris         = beidouEphemeris;
outputEphemeris.ionosphericParameters   = ionosphericParameters;
% outputEphemeris.DOY                     = real(DOY);
outputEphemeris.leapSeconds             = leapSeconds;


fclose(navFile);
'Ephemeris loaded correctly'


end
