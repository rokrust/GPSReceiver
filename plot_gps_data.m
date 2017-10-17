data = csvread('log\satdump.txt', 2, 0);
data = data(all(data, 2), :);
[~, index] = sort(data(:, 2));
data = data(index, :);

n_measure_var = 6;
n = size(data, 1);

time = 1;
sat_num = 2;
x = 3; y = 4; z = 5;
vx = 6; vy = 7; vz = 8;

NO_POS = zeros(1, 3);
t = [];
pos = [];
prev_sat = data(1, sat_num);

for i = 1:n
    current_sat = data(i, sat_num);
    
    if prev_sat ~= current_sat || i == n;
       plot(t, pos);
       t = [];
       pos = [];
       figure;
       
    end

    t = [t; data(i, time)];
    pos = [pos; data(i, x:z)];
        
end

plot(t, pos);