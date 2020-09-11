from cmath import sqrt

V_in = 200e-3       # data-file
I_in = 5e-3         # data-file
I_leak = 0          # model-parameter
dt = 1 / 1e3      # parameter
C = 1000e-6         # model-parameter
V_cap = 3           # start-parameter -> DAC-write
V_cap_max = 4.2     # model-parameter
V_cap_min = 0       # model-parameter
V_upper_thres = 3.5 # model-parameter
V_lower_thres = 3.2 # model-parameter
eta_in = 0.8        # LUT-parameter, f(V_in,I_in)
eta_out = 0.9       # LUT-parameter, f(V_out,I_out)
V_out = 2.3         # parameter
I_out = 0e-3        # ADC-measurement

for i in range(20):
    P_in = V_in * I_in
    I_cIn = eta_in * P_in / V_cap
    P_out = V_out * I_out
    I_cOut = P_out / (V_cap * eta_out)
    dI = I_cIn - I_cOut - I_leak
    dV_cap = (dI * dt) / C
    V_cap = V_cap + dV_cap
    if V_cap > V_cap_max:
        V_cap = V_cap_max
    if V_cap < V_cap_min:
        V_cap = V_cap_min
    print(f"V = {V_cap} incl \t dV = {dV_cap}")

# switching on supply with output capacitor -> try to model a more correct approach
# E = C*V^2 / 2
# E_new = E_old - E_output
# C_cap * V_cap_new^2 / 2 = C_cap * V_cap_old^2 / 2 - C_out * V_out^2 / 2
# V_cap_new^2 = V_cap_old^2 - (C_out / C_cap) * V_out^2

C_cap = 200e-6
C_out = 22e-6
V_upper_thres = 3.5
V_out = 2.3
V_cCode = V_upper_thres * sqrt((C_cap - C_out) / C_cap)     # = 3.302 V
V_thesis = V_upper_thres * sqrt(C_cap / (C_cap + C_out))    # = 3.322 V
V_ingmar = sqrt(pow(V_upper_thres, 2) - C_out * pow(V_out, 2) / C_cap)  # = 3.416 V
print(V_cCode)
print(V_thesis)
print(V_ingmar)

# TODO: ask Boris about it
# maxima-code:
'''
CC: C_cap * V_cap_new^2 / 2 = C_cap * V_cap_old^2 / 2 - C_out * V_out^2 / 2;
ft : solve(CC, V_cap_new)[2];
'''
