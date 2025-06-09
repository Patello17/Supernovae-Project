import matplotlib.pyplot as plt

data = "combinedPC.pi"
arf = "combinedPC_exp.arf" # same for source and background
rmf = "swxpc0to12s6_20210101v016.rmf" # same for source and background
bkg_data = "combinedPCback.pi"

# Load Data
print("Loading Data...")
load_pha(data)
load_bkg(bkg_data)
print("Data Loaded.")

print(get_arf())
print(get_rmf())
print(get_bkg_arf())
print(get_bkg_rmf())
print(get_dep())

print("Configuring...")
notice(0.3,8)
group_counts(1)
set_xsxset("APECROOT", "/home/prayag/Software/ciao-4.17/spectral/modelData/apec_v3.0.9") # Use correct APECROOT
set_source(xstbabs.abs1*xsvapec.v1) # Fit APEC Model
set_bkg_model(powlaw1d.p1)
set_par("abs1.nH", min=0.0115)
set_stat("cash")

# set_source(xstbabs.abs1*xsvmekal.v1)
# g1.Sigma=0.2 # (No Gaussian Necessary)
set_xsabund("wilm")
# thaw(v1.Si)
print("Configured.")

print("Fitting...")
fit()
fres = get_fit_results()
print("Fitted.")

print("Getting Confidence...")
conf()
# set_ylog()
print("Got Confidence.")

# Format Plot
print("Formatting Plot(s)...")
# plot("bkg")
plot_fit(color="royalblue")
# plot_bkg_fit(overplot=True)
plt.xlim(0.3, 4)
plt.ylim(0, 0.015)

fig = plt.gcf()
ax1 = fig.axes[0]
ax2 = fig.axes[0]

plt.sca(ax1)
plt.ylabel("Counts s$^{-1}$ keV$^{-1}$", fontsize=14)
plt.yticks(fontsize=11)
ax1.lines[0].set_linewidth(4)
ax1.lines[2].set_color("sandybrown")
ax1.lines[2].set_linewidth(3)
plt.title("Combined Swift Data Plot (Sept. 29, 2024 - Oct. 14, 2024)")
# plt.setp(ax1.spines.values(), linewidth=3)

plt.sca(ax2)
plt.ylabel("Counts s$^{-1}$ keV$^{-1}$", fontsize=14)
plt.yticks(fontsize=12)
plt.xticks(fontsize=12)
plt.xlabel("Energy (keV)", fontsize=14)
plt.setp(ax2.lines, linewidth=4)
# ax2.lines[0].set_linewidth(2)
plt.setp(ax2.spines.values(), linewidth=2)
print("Plot Formatted.")

# Get Flux
print("Calculating Flux...")
s1=sample_flux(v1, 0.3, 8, num=1000) # Calculate Uncertainty for Flux
print("Calculated Flux.")

# Save Plot
print("Saving Plot...")
plt.savefig("2023ixf_plot.pdf")
print("Plot Saved.")
