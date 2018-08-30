function [tow, gps_week] = Date2GPSTime(year,month,day,hour)
% =========================================================================
%> @brief This function converts calendar date/time to GPS week/time.
%> @date      December 7, 2015
%> @author    Damian Miralles. damian.miralles@colorado.edu
%> @version   0.1 Initial release
%>
%> @param calDate datetime value containing the date.
%>
%> @retval gps_week value containing the GPS week number
%> @retval gps_sec  value containing the GPS seconds number
%>
%>
%>  <b>References</b>
%>  - <a href="http://www.gpstextbook.com/">
%> P. Misra and P. Enge, Global Positioning System: Signals, Measurements,
%> and Performance, Revised Se. 2010..</a>
% =========================================================================
%--- Define seconds in one week
secs_per_week = 604800;

%--- Converts the two digit year to a four digit year. Two digit year
% represents a year in the range 1980-2079.
if (year >= 80 && year <= 99)
    year = 1900 + year;
end
if (year >= 0 && year <= 79)
    year = 2000 + year;
end


%--- Calculates the 'm' term used below from the given calendar month.
if (month <= 2)
    y = year - 1;
    m = month + 12;
end
if (month > 2)
    y = year;
    m = month;
end

%--- Computes the Julian date corresponding to the given calendar date.
JD = floor( (365.25 * y) ) + floor( (30.6001 * (m+1)) ) + ...
    day + ( (hour) / 24 ) + 1720981.5;

%--- Computes the GPS week corresponding to the given calendar date.
gps_week = floor( (JD - 2444244.5) / 7 );

%         %--- Computes the GPS seconds corresponding to the given calendar date.
tow=round(((((JD-2444244.5)/7)-gps_week)*secs_per_week)/0.5)*0.5;

end
