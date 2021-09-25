dist = [5:5:60]';
read = [560, 435, 316, 235, 189, 154, 132, 116, 100, 93, 80, 72]';


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

% plot(x, c+d*log(x), 'black')

syms x
f = p(1,1) * x^3 + p(1,2) * x^2 + p(1,3) * x + p(1,4);
yay = finverse(f)
g = ((((96525*x)/1088 - 9008)^2 + 654710)^(1/2) - (96525*x)/1088 + 9008)^(1/3) - 16287/(187*((((96525*x)/1088 - 9008)^2 + 654710)^(1/2) - (96525*x)/1088 + 9008)^(1/3)) + 20779/448

boo = simplify(yay)

dummy = 5:0.05:600;
plot(dummy, subs(g, x, dummy), '-b')
hold on
plot(read, dist, '-r')
hold off