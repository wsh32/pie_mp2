dist = [5:5:60]';
read = [560, 435, 316, 235, 189, 154, 132, 116, 100, 93, 80, 72]';

plot(dist, read, '-rx')
hold on

f = fit(dist, read,'exp1')

a = 89.88;
b = -0.006513;

x = 5:0.05:60;
p = polyfit(dist, read, 3)
f1 = polyval(p, x);

[ones(size(dist)),log(dist)]\read;
c = 872.2273;
d = -203.1713;


% plot(read, a*exp(b*dist), 'blue')
plot(x, f1, 'green')
% plot(x, c+d*log(x), 'black')
hold off

syms x
f = p(1,1) * x^3 + p(1,2) * x^2 + p(1,3) * x + p(1,4);
g = finverse(f)
