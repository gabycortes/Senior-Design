clear;
clc;

% use importfile function to import .csv file into table, starting from the
% second row
T = importfile("BajaTest_02-24-20_15-54-53.csv", [2, Inf]);
% sort the table by sensor name
T = sortrows(T,'sensor');
% count how many of each sensor there is using countcats() and save into
% vector
type_count = countcats(T.sensor);

% create a vector for each type and store the values
dist = T.value(1:type_count(1));
% convert hour and minute to second, add them with second for only sensor
dist_time = T.hour(1:type_count(1))*3600 + T.min(1:type_count(1))*60 +T.sec(1:type_count(1));

he1_end = type_count(1)+1+type_count(2);
he1 = T.value(type_count(1)+1:he1_end);
he1_time = T.hour(type_count(1)+1:he1_end)*3600 + T.min(type_count(1)+1:he1_end)*60 +T.sec(type_count(1)+1:he1_end);

he2 = T.value(he1_end+1:end);
he2_time = T.hour(he1_end+1:end)*3600 + T.min(he1_end+1:end)*60 +T.sec(he1_end+1:end);

% free memory used by table
clear T;

% show original RPMs
%twoPlots(he1_time, he1, he2_time, he2, 6000, 'Unfiltered Primary and Secondary RPM', 'Secondary RPM', 'Primary RPM');

% run secondary through data filter
[he1_filtered, he1_time_filtered] = filter(he1, he1_time);
he1_filtered = movmean(he1_filtered, 5);
%twoPlots(he1_time, he1, he1_time_filtered, he1_filtered, 6000, 'Secondary Filtered vs Unfiltered RPM', 'Unfiltered', 'Filtered');

% run primary through  data filter
[he2_filtered, he2_time_filtered] = filter(he2, he2_time);
[he2_filtered, he2_time_filtered] = filter(he2_filtered, he2_time_filtered);
%twoPlots(he2_time, he2, he2_time_filtered, he2_filtered, 6000, 'Primary Filtered vs Unfiltered RPM', 'Unfiltered', 'Filtered');

% create an equal number of data points for both RPMs
time = combine(he1_time_filtered, he2_time_filtered);
he2_filtered = fill(he2_time_filtered, he2_filtered, time);
he1_filtered = fill(he1_time_filtered, he1_filtered, time);


% generate a plot of filtered RPMs
twoPlots(time, he1_filtered, time, he2_filtered, 6000, 'Primary vs Secondary RPM', 'Secondary', 'Primary')

% shows distance sensor data with and without filter 
%twoPlots(dist_time, dist, dist_time, sgolayfilt(dist,1,17), 2, 'Distance Sensor Filtered vs Unfiltered', 'Unfiltered Distance (in)', 'Filtered Distance (in)');

% calculate ratio
ratio = he1_filtered./he2_filtered;
onePlot(time, ratio, 1.5, 'Ratio of Primary and Secondary', 'Ratio')

function Y2 = fill(X1, Y1, X2)

% X1 and Y1 is the original data
% X2 is the new x-axis (with more values than X1)
% Y2 (and temporarily y) is a new y-axis generated by drawing a line
% between pairs of X1, Y1 points with input X2 and output Y2 along the line

	y = 1:length(X2);
	lower = 1;
	upper = lower + 1;
    i =1;
    while(i <= length(X2))
        if (X2(i) <= X1(lower))
            y(i) = Y1(lower);
            i = i +1;
        elseif(X2(i) > X1(lower))
            if(upper <= length(X1) && X2(i) < X1(upper))
                m = (Y1(upper)-Y1(lower))/(X1(upper)-X1(lower));
                y(i) = m * (X2(i)-X1(upper)) + Y1(upper);
                i = i + 1;
            elseif(upper < length(X1))
                lower = lower + 1;
                upper = upper + 1;
            else
                y(i) = Y1(upper);
                i = i + 1;
            end
        end
    end
	Y2 = y;
end

function x = combine(X1, X2)

% takes ordered vectors Y1 and Y2 of different sizes, and combines them
% together in order

    x1 = 1:(length(X1)+ length(X2));
    i = 1;
    m = 1;
    n = 1;
    for i = 1:length(x1)
        if(m <= length(X1) && X1(m) < X2(n))
            x1(i) = X1(m);
            m = m+1;
        else
            x1(i) = X2(n);
            n = n+1;
        end        
    end
    x = x1;
end

function [x,y] = filter(X1, Y1)

% remove outliers from X1 using the rmoutliers function

% rmoutliers takes a vector and applies an outlier removal strategy on the 
% specified window size at a time

% movmedian determines outliers as more than 3 local scaled MAD away from 
% the local median

% remove the values in Y1 corresponding to the removed outliers

% repeat the process, each time reducing the window size

    window = 7;
    for i = (1:6)
        [X1,b] = rmoutliers(X1,'movmedian',window);
        Y1 = Y1(~b);
        window = window - 1;
    end
    x = X1;
    y = Y1;
end

function importTable = importfile(filename, dataLines)
%IMPORTFILE Import data from a text file
%  IMPORTTABLE = IMPORTFILE(FILENAME) reads data from text file
%  FILENAME for the default selection.  Returns the data as a table.
%
%  IMPORTTABLE = IMPORTFILE(FILE, DATALINES) reads data for the
%  specified row interval(s) of text file FILENAME. Specify DATALINES as
%  a positive scalar integer or a N-by-2 array of positive scalar
%  integers for dis-contiguous row intervals.
%
%  Example:
%  T = importfile("BajaTest_02-12-20_16-45-32.csv", [2, Inf]);
%
%  See also READTABLE.
%
% Auto-generated by MATLAB on 19-Feb-2020 19:16:00

% Input handling

% If dataLines is not specified, define defaults
if nargin < 2
    dataLines = [2, Inf];
end

% Setup the Import Options and import the data
opts = delimitedTextImportOptions("NumVariables", 5);

% Specify range and delimiter
opts.DataLines = dataLines;
opts.Delimiter = [",", ":"];

% Specify column names and types
opts.VariableNames = ["sensor", "value", "hour", "min", "sec"];
opts.VariableTypes = ["categorical", "double", "double", "double", "double"];

% Specify file level properties
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";

% Specify variable properties
opts = setvaropts(opts, "sensor", "EmptyFieldRule", "auto");

% Import the data
importTable = readtable(filename, opts);

end

function onePlot(X1, Y1, max, graph_title, label_y)

% combines graphs of X1, Y1 and X2, Y2 in the same plot

% create a container for the plots in a maximized window
figure('WindowState','maximized');

% use to include more than one plot
hold('on');

grid minor;

plot(X1,Y1,'Marker','.',...
    'LineStyle','none')

% Create left y axis label
ylabel(label_y);
ylim([0 max])

% Create x axis label - only need one since the same data is represented
xlabel('Time (s)');

% Create title - change queue size here
title(graph_title);

end

function twoPlots(X1, Y1, X2, Y2, max, graph_title, label_y1, label_y2)

% combines graphs of X1, Y1 and X2, Y2 in the same plot

% create a container for the plots in a maximized window
figure1 = figure('WindowState','maximized');
axes1 = axes('Parent',figure1);

% use to include more than one plot
hold(axes1,'on');

grid minor;

% left plot will generate y axis on left side
yyaxis(axes1,'left');
plot(X1,Y1,'Marker','.',...
    'LineStyle','none')

% Create left y axis label
ylabel(label_y1);
ylim([0 max])

% Create x axis label - only need one since the same data is represented
xlabel('Time (s)');

% right plot will generate y axis on right side
yyaxis(axes1,'right');
plot(X2,Y2,'Marker','.',...
    'LineStyle','none')

% Create right y axis label
ylabel(label_y2);
ylim([0 max])

% Create title - change queue size here
title(graph_title);

end